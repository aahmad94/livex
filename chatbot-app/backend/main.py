from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
calcom_api_key = os.getenv("CALCOM_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    email: str
    messages: list

# Cal.com API Functions
def get_available_slots(date: str):
    response = requests.get(
        "https://api.cal.com/v1/slots",
        params={"date": date, "apiKey": calcom_api_key}
    )
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch slots"}

def book_event(email: str, date: str, time: str, reason: str):
    response = requests.post(
        "https://api.cal.com/v1/bookings",
        headers={"Authorization": f"Bearer {calcom_api_key}"},
        json={"email": email, "start": f"{date}T{time}", "title": reason}
    )
    return response.json() if response.status_code == 201 else {"error": "Booking failed"}

def list_events(email: str):
    response = requests.get(
        "https://api.cal.com/v1/bookings",
        headers={"Authorization": f"Bearer {calcom_api_key}"},
        params={"email": email}
    )
    return response.json() if response.status_code == 200 else {"error": "Failed to list events"}

def cancel_event(event_id: str):
    response = requests.delete(
        f"https://api.cal.com/v1/bookings/{event_id}",
        headers={"Authorization": f"Bearer {calcom_api_key}"}
    )
    return {"success": True} if response.status_code == 204 else {"error": "Cancellation failed"}

def reschedule_event(event_id: str, new_date: str, new_time: str):
    response = requests.patch(
        f"https://api.cal.com/v1/bookings/{event_id}",
        headers={"Authorization": f"Bearer {calcom_api_key}"},
        json={"start": f"{new_date}T{new_time}"}
    )
    return {"success": True} if response.status_code == 200 else {"error": "Reschedule failed"}

# OpenAI Function Schemas
functions = [
    {
        "name": "get_available_slots",
        "description": "Get available time slots for a date",
        "parameters": {
            "type": "object",
            "properties": {"date": {"type": "string", "description": "Date in YYYY-MM-DD"}},
            "required": ["date"]
        }
    },
    {
        "name": "book_event",
        "description": "Book a new event",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "User's email"},
                "date": {"type": "string", "description": "Date in YYYY-MM-DD"},
                "time": {"type": "string", "description": "Time in HH:MM"},
                "reason": {"type": "string", "description": "Reason for the event"}
            },
            "required": ["email", "date", "time", "reason"]
        }
    },
    {
        "name": "list_events",
        "description": "List user's scheduled events",
        "parameters": {
            "type": "object",
            "properties": {"email": {"type": "string", "description": "User's email"}},
            "required": ["email"]
        }
    },
    {
        "name": "cancel_event",
        "description": "Cancel an event",
        "parameters": {
            "type": "object",
            "properties": {"event_id": {"type": "string", "description": "Event ID"}},
            "required": ["event_id"]
        }
    },
    {
        "name": "reschedule_event",
        "description": "Reschedule an event",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "Event ID"},
                "new_date": {"type": "string", "description": "New date in YYYY-MM-DD"},
                "new_time": {"type": "string", "description": "New time in HH:MM"}
            },
            "required": ["event_id", "new_date", "new_time"]
        }
    }
]

@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [{"role": "system", "content": f"You are a chatbot assisting {request.email} with Cal.com events"}] + request.messages
    
    try:
        while True:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                functions=functions,
                function_call="auto"
            )
            
            message = response.choices[0].message
            
            # If no function call, return the message content
            if not hasattr(message, 'function_call') or message.function_call is None:
                return {"response": message.content}
            
            # Process function call
            func_name = message.function_call.name
            args = json.loads(message.function_call.arguments)
            
            # Execute the appropriate function
            if func_name == "get_available_slots":
                result = get_available_slots(args["date"])
            elif func_name == "book_event":
                result = book_event(args["email"], args["date"], args["time"], args["reason"])
            elif func_name == "list_events":
                result = list_events(args["email"])
            elif func_name == "cancel_event":
                result = cancel_event(args["event_id"])
            elif func_name == "reschedule_event":
                result = reschedule_event(args["event_id"], args["new_date"], args["new_time"])
            
            # Add the function result to messages
            messages.append({"role": "function", "name": func_name, "content": json.dumps(result)})
    
    except Exception as e:
        return {"response": f"An error occurred: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "Chatbot API is running"} 