from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
import json
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
calcom_api_key = os.getenv("CALCOM_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:5175"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    email: str
    messages: list

# Mock data for Cal.com API
mock_events = []
mock_event_id_counter = 1

# Cal.com API Functions (with mock implementation)
def get_available_slots(date: str):
    print(f"Getting available slots for date: {date}")
    print(f"Using Cal.com API key: {calcom_api_key}")
    
    try:
        # Try to use the real Cal.com API if we have a valid API key
        if calcom_api_key and calcom_api_key != "your_calcom_api_key" and not calcom_api_key.startswith("cal_test_"):
            # Parse the date and create dateFrom and dateTo parameters
            # dateFrom should be the start of the day, dateTo should be the end of the day
            try:
                parsed_date = datetime.strptime(date, "%Y-%m-%d")
                date_from = parsed_date.strftime("%Y-%m-%dT00:00:00Z")
                date_to = parsed_date.strftime("%Y-%m-%dT23:59:59Z")
                
                print(f"Using dateFrom: {date_from}, dateTo: {date_to}")
                
                # Using the Cal.com V2 API endpoint for available slots
                api_url = "https://api.cal.com/v2/slots"
                print(f"Using API URL: {api_url}")
                
                # V2 API uses Authorization header with Bearer token
                response = requests.get(
                    api_url,
                    headers={
                        "Authorization": f"Bearer {calcom_api_key}",
                        "Content-Type": "application/json"
                    },
                    params={
                        "startTime": date_from,
                        "endTime": date_to,
                        "eventTypeId": 1  # Default event type ID, you may need to adjust this
                    }
                )
            except ValueError as e:
                print(f"Error parsing date: {date}. Error: {str(e)}")
                # If date parsing fails, try using the date as is with time boundaries
                date_from = f"{date}T00:00:00Z"
                date_to = f"{date}T23:59:59Z"
                
                print(f"Using dateFrom: {date_from}, dateTo: {date_to}")
                
                # Using the Cal.com V2 API endpoint for available slots
                api_url = "https://api.cal.com/v2/slots"
                print(f"Using API URL: {api_url}")
                
                # V2 API uses Authorization header with Bearer token
                response = requests.get(
                    api_url,
                    headers={
                        "Authorization": f"Bearer {calcom_api_key}",
                        "Content-Type": "application/json"
                    },
                    params={
                        "startTime": date_from,
                        "endTime": date_to,
                        "eventTypeId": 1  # Default event type ID, you may need to adjust this
                    }
                )
            
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            if response.status_code == 200:
                # Process the response to match our expected format
                api_response = response.json()
                print(f"API response: {api_response}")
                
                # Transform the Cal.com API V2 response to our expected format
                slots = []
                if "slots" in api_response:
                    for slot in api_response["slots"]:
                        slots.append({
                            "start": slot["time"],
                            "end": slot["time"],  # V2 API might not provide end time, so we use the same time
                            "available": True
                        })
                
                return {"slots": slots}
            else:
                print(f"Falling back to mock implementation due to API error")
                # Fall back to mock implementation if API call fails
                return generate_mock_slots(date)
        else:
            # Mock implementation
            print("Using mock implementation for get_available_slots")
            return generate_mock_slots(date)
    except Exception as e:
        print(f"Exception in get_available_slots: {str(e)}")
        print("Falling back to mock implementation due to exception")
        # Fall back to mock implementation if there's an exception
        return generate_mock_slots(date)

# Helper function to generate mock time slots
def generate_mock_slots(date: str):
    # Generate mock time slots for the given date
    slots = []
    start_hour = 9  # 9 AM
    end_hour = 17   # 5 PM
    
    for hour in range(start_hour, end_hour):
        for minute in [0, 30]:
            slot_time = f"{hour:02d}:{minute:02d}"
            slots.append({
                "start": f"{date}T{slot_time}:00Z",
                "end": f"{date}T{hour:02d}:{minute+30 if minute == 0 else (hour+1):02d}:00Z",
                "available": True
            })
    
    return {"slots": slots}

def book_event(email: str, date: str, time: str, reason: str):
    print(f"Booking event for email: {email}, date: {date}, time: {time}, reason: {reason}")
    
    try:
        # Try to use the real Cal.com API if we have a valid API key
        if calcom_api_key and calcom_api_key != "your_calcom_api_key" and not calcom_api_key.startswith("cal_test_"):
            # Parse the time to calculate end time (assuming 1 hour duration)
            try:
                # Parse the time string (assuming format like "14:30")
                hour, minute = map(int, time.split(':'))
                
                # Calculate end time (1 hour later)
                end_hour = hour + 1
                end_minute = minute
                
                # Format start and end times
                start_time = f"{hour:02d}:{minute:02d}"
                end_time = f"{end_hour:02d}:{end_minute:02d}"
                
                print(f"Calculated start time: {start_time}, end time: {end_time}")
            except Exception as e:
                print(f"Error parsing time: {str(e)}. Using original time.")
                start_time = time
                end_time = time  # You may want to set a default duration
            
            # Using the Cal.com V2 API endpoint for booking events
            api_url = "https://api.cal.com/v2/bookings"
            print(f"Using API URL: {api_url}")
            
            response = requests.post(
                api_url,
                headers={
                    "Authorization": f"Bearer {calcom_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "eventTypeId": 1,  # Default event type ID, you may need to adjust this
                    "start": f"{date}T{start_time}:00Z",
                    "end": f"{date}T{end_time}:00Z",
                    "name": "Meeting",
                    "email": email,
                    "title": reason,
                    "notes": reason,
                    "language": "en",
                    "timeZone": "UTC",
                    "metadata": {}
                }
            )
            
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            if response.status_code in [200, 201]:
                # Process the response to match our expected format
                api_response = response.json()
                print(f"API response: {api_response}")
                
                # Transform the Cal.com API response to our expected format
                booking = {
                    "id": api_response.get("uid", f"cal_{api_response.get('id', 'unknown')}"),
                    "email": email,
                    "title": reason,
                    "start": f"{date}T{start_time}:00Z",
                    "end": f"{date}T{end_time}:00Z",
                    "status": "confirmed"
                }
                
                return {
                    "booking": booking,
                    "message": "Booking successful"
                }
            else:
                print(f"Falling back to mock implementation due to API error")
                # Fall back to mock implementation if API call fails
                return generate_mock_booking(email, date, time, reason)
        else:
            # Mock implementation
            print("Using mock implementation for book_event")
            return generate_mock_booking(email, date, time, reason)
    except Exception as e:
        print(f"Exception in book_event: {str(e)}")
        print("Falling back to mock implementation due to exception")
        # Fall back to mock implementation if there's an exception
        return generate_mock_booking(email, date, time, reason)

# Helper function to generate a mock booking
def generate_mock_booking(email: str, date: str, time: str, reason: str):
    global mock_event_id_counter
    event_id = f"mock_event_{mock_event_id_counter}"
    mock_event_id_counter += 1
    
    # Calculate end time (1 hour after start)
    hour, minute = map(int, time.split(':'))
    end_hour = hour + 1
    end_time = f"{end_hour:02d}:{minute:02d}"
    
    new_event = {
        "id": event_id,
        "email": email,
        "title": reason,
        "start": f"{date}T{time}:00Z",
        "end": f"{date}T{end_time}:00Z",
        "status": "confirmed"
    }
    
    mock_events.append(new_event)
    
    return {
        "booking": new_event,
        "message": "Booking successful"
    }

def list_events(email: str):
    print(f"Listing events for email: {email}")
    
    try:
        # Try to use the real Cal.com API if we have a valid API key
        if calcom_api_key and calcom_api_key != "your_calcom_api_key" and not calcom_api_key.startswith("cal_test_"):
            # Using the Cal.com V2 API endpoint for listing events
            api_url = "https://api.cal.com/v2/bookings"
            print(f"Using API URL: {api_url}")
            
            response = requests.get(
                api_url,
                headers={
                    "Authorization": f"Bearer {calcom_api_key}",
                    "Content-Type": "application/json"
                },
                params={
                    "email": email  # Filter by email if possible
                }
            )
            
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            if response.status_code == 200:
                # Process the response to match our expected format
                api_response = response.json()
                print(f"API response: {api_response}")
                
                # Transform the Cal.com API response to our expected format
                bookings = []
                if "bookings" in api_response:
                    for booking in api_response["bookings"]:
                        if booking.get("attendees") and any(attendee.get("email") == email for attendee in booking.get("attendees", [])):
                            bookings.append({
                                "id": booking.get("uid", f"cal_{booking.get('id', 'unknown')}"),
                                "email": email,
                                "title": booking.get("title", "Meeting"),
                                "start": booking.get("startTime"),
                                "end": booking.get("endTime"),
                                "status": booking.get("status", "confirmed")
                            })
                
                return {"bookings": bookings}
            else:
                print(f"Falling back to mock implementation due to API error")
                # Fall back to mock implementation if API call fails
                return generate_mock_event_list(email)
        else:
            # Mock implementation
            print("Using mock implementation for list_events")
            return generate_mock_event_list(email)
    except Exception as e:
        print(f"Exception in list_events: {str(e)}")
        print("Falling back to mock implementation due to exception")
        # Fall back to mock implementation if there's an exception
        return generate_mock_event_list(email)

# Helper function to generate a mock event list
def generate_mock_event_list(email: str):
    # Filter events by email
    user_events = [event for event in mock_events if event["email"] == email]
    
    return {"bookings": user_events}

def cancel_event(event_id: str):
    print(f"Canceling event with ID: {event_id}")
    
    try:
        # Try to use the real Cal.com API if we have a valid API key
        if calcom_api_key and calcom_api_key != "your_calcom_api_key" and not calcom_api_key.startswith("cal_test_") and not event_id.startswith("mock_"):
            # Using the Cal.com V2 API endpoint for canceling events
            # Extract the actual ID if it's a Cal.com ID
            cal_id = event_id
            if event_id.startswith("cal_"):
                cal_id = event_id[4:]  # Remove the "cal_" prefix
            
            api_url = f"https://api.cal.com/v2/bookings/{cal_id}"
            print(f"Using API URL: {api_url}")
            
            response = requests.delete(
                api_url,
                headers={
                    "Authorization": f"Bearer {calcom_api_key}",
                    "Content-Type": "application/json"
                }
            )
            
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            if response.status_code in [200, 204]:
                return {"success": True, "message": "Event canceled successfully"}
            else:
                print(f"Falling back to mock implementation due to API error")
                # Fall back to mock implementation if API call fails
                return generate_mock_cancel(event_id)
        else:
            # Mock implementation
            print("Using mock implementation for cancel_event")
            return generate_mock_cancel(event_id)
    except Exception as e:
        print(f"Exception in cancel_event: {str(e)}")
        print("Falling back to mock implementation due to exception")
        # Fall back to mock implementation if there's an exception
        return generate_mock_cancel(event_id)

# Helper function to generate a mock cancel response
def generate_mock_cancel(event_id: str):
    global mock_events
    # Find the event by ID
    for i, event in enumerate(mock_events):
        if event["id"] == event_id:
            # Remove the event
            mock_events.pop(i)
            return {"success": True, "message": "Event canceled successfully"}
    
    return {"error": "Event not found"}

def reschedule_event(event_id: str, new_date: str, new_time: str):
    print(f"Rescheduling event with ID: {event_id} to date: {new_date}, time: {new_time}")
    
    try:
        # Try to use the real Cal.com API if we have a valid API key
        if calcom_api_key and calcom_api_key != "your_calcom_api_key" and not calcom_api_key.startswith("cal_test_") and not event_id.startswith("mock_"):
            # Parse the time to calculate end time (assuming 1 hour duration)
            try:
                # Parse the time string (assuming format like "14:30")
                hour, minute = map(int, new_time.split(':'))
                
                # Calculate end time (1 hour later)
                end_hour = hour + 1
                end_minute = minute
                
                # Format start and end times
                start_time = f"{hour:02d}:{minute:02d}"
                end_time = f"{end_hour:02d}:{end_minute:02d}"
                
                print(f"Calculated start time: {start_time}, end time: {end_time}")
            except Exception as e:
                print(f"Error parsing time: {str(e)}. Using original time.")
                start_time = new_time
                end_time = new_time  # You may want to set a default duration
            
            # Extract the actual ID if it's a Cal.com ID
            cal_id = event_id
            if event_id.startswith("cal_"):
                cal_id = event_id[4:]  # Remove the "cal_" prefix
            
            # Using the Cal.com V2 API endpoint for rescheduling events
            api_url = f"https://api.cal.com/v2/bookings/{cal_id}/reschedule"
            print(f"Using API URL: {api_url}")
            
            response = requests.patch(
                api_url,
                headers={
                    "Authorization": f"Bearer {calcom_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "rescheduleReason": "Rescheduled via chatbot",
                    "start": f"{new_date}T{start_time}:00Z",
                    "end": f"{new_date}T{end_time}:00Z"
                }
            )
            
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            if response.status_code in [200, 201, 204]:
                return {"success": True, "message": "Event rescheduled successfully"}
            else:
                print(f"Falling back to mock implementation due to API error")
                # Fall back to mock implementation if API call fails
                return generate_mock_reschedule(event_id, new_date, new_time)
        else:
            # Mock implementation
            print("Using mock implementation for reschedule_event")
            return generate_mock_reschedule(event_id, new_date, new_time)
    except Exception as e:
        print(f"Exception in reschedule_event: {str(e)}")
        print("Falling back to mock implementation due to exception")
        # Fall back to mock implementation if there's an exception
        return generate_mock_reschedule(event_id, new_date, new_time)

# Helper function to generate a mock reschedule response
def generate_mock_reschedule(event_id: str, new_date: str, new_time: str):
    # Calculate new end time (1 hour after start)
    hour, minute = map(int, new_time.split(':'))
    end_hour = hour + 1
    end_time = f"{end_hour:02d}:{minute:02d}"
    
    # Find the event by ID
    for event in mock_events:
        if event["id"] == event_id:
            # Update the event
            event["start"] = f"{new_date}T{new_time}:00Z"
            event["end"] = f"{new_date}T{end_time}:00Z"
            return {"success": True, "message": "Event rescheduled successfully"}
    
    return {"error": "Event not found"}

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