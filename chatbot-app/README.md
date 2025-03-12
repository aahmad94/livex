# Chatbot Application

![Chatbot Application Screenshot](../image.png)

A full-stack chatbot application with React frontend and FastAPI backend, integrating OpenAI function calling and Cal.com API.

## Quick Start Guide

### Running the Application

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Ensure the `.env` file contains:
   ```
   OPENAI_API_KEY=your_openai_api_key
   CALCOM_API_KEY=your_calcom_api_key
   ```
   - Note: If you don't have a Cal.com API key, the application will use a mock implementation

5. Run the backend server:
```bash
python -m uvicorn main:app --reload --port 8000
```

6. Verify the backend is running by visiting http://localhost:8000 in your browser. You should see a message: `{"message":"Chatbot API is running"}`

#### Frontend Setup

1. Open a new terminal window and navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Access the application at http://localhost:5173 (or the port shown in the terminal)

## Testing the Application

### Using the Chatbot

1. Open the application in your browser
2. Click on the chat icon in the bottom right corner
3. Enter your email address to start chatting
4. The chatbot will display a welcome message with available capabilities

### Testing Cal.com API Functions

The application uses a mock implementation for Cal.com API functions. You can test these functions by asking the chatbot:

#### 1. Check Available Time Slots
Try asking:
- "What time slots are available tomorrow?"
- "Show me available slots for next Monday"
- "I need to see available times for July 15th"

#### 2. Book an Event
Try asking:
- "Book a meeting for tomorrow at 10:00 AM"
- "Schedule a call on Friday at 2:30 PM for project discussion"
- "I want to book a meeting on 2023-12-15 at 11:00 AM for team review"

#### 3. List Events
Try asking:
- "Show me my scheduled meetings"
- "What events do I have coming up?"
- "List all my appointments"

#### 4. Cancel an Event
First book an event, then try asking:
- "Cancel my meeting at 10:00 AM tomorrow"
- "I need to cancel my event with ID mock_event_1"
- "Delete my appointment on Friday"

#### 5. Reschedule an Event
First book an event, then try asking:
- "Reschedule my 10:00 AM meeting to 2:00 PM"
- "Move my appointment on Friday to Monday at 11:30 AM"
- "Change my event with ID mock_event_1 to next Tuesday at 3:00 PM"

### Debugging

If you encounter issues:

1. Check the backend console for error messages
2. Verify both frontend and backend are running
3. Ensure your OpenAI API key is valid
4. Remember that the Cal.com API is mocked, so no real Cal.com account is needed

## Features

- **Interactive UI**: Responsive design with navbar, side menu, and content area
- **Search Functionality**: Filter and highlight content based on search terms
- **Chatbot Integration**: AI-powered chatbot with OpenAI function calling
- **Cal.com API Integration**: Book, list, cancel, and reschedule events
- **Mock Cal.com API**: Simulated Cal.com API for testing without a real account

## Tech Stack

### Frontend
- React (with Vite)
- CSS for styling
- Axios for API requests

### Backend
- FastAPI
- OpenAI API for function calling
- Cal.com API for event management
- Mock implementation for Cal.com API

## API Endpoints

- `GET /`: Root endpoint, returns a simple message
- `POST /chat`: Chat endpoint that processes user messages and interacts with OpenAI and Cal.com APIs

## Chatbot Capabilities

The chatbot can:
- Check available time slots for meetings
- Book new events on Cal.com
- List all scheduled events for a user
- Cancel existing events
- Reschedule events to new dates/times

## Cal.com API Integration

The application integrates with the Cal.com API to manage calendar events. If you don't have a Cal.com API key, the application will use a mock implementation that simulates the Cal.com API behavior:

- **Mock Available Slots**: Generates time slots from 9 AM to 5 PM in 30-minute intervals
- **Mock Booking**: Creates a simulated booking with a unique ID
- **Mock Listing**: Returns all bookings associated with the user's email
- **Mock Cancellation**: Removes a booking from the simulated database
- **Mock Rescheduling**: Updates the booking time in the simulated database

This allows you to test the full functionality of the application without a real Cal.com account.

## Development Notes

- The frontend is built with React and uses CSS for styling
- The backend uses FastAPI and OpenAI's function calling feature
- The application is designed to be responsive and works on both desktop and mobile devices
- The chatbot interface includes a timer that tracks the duration of the conversation
- The mock implementation for Cal.com API is defined in the `main.py` file
- Session data is stored in memory and will be lost when the server restarts 