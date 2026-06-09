import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

# 1. Initialize the FastAPI application
app = FastAPI(title="Gemini AI Chatbot Backend")

# 2. Define what a user's message looks like (Data Validation)
class ChatRequest(BaseModel):
    message: str

# 3. Securely look for the Gemini API key in the environment variables
api_key = os.environ.get("GEMINI_API_KEY")

@app.get("/")
def home():
    return {"status": "Backend is running smoothly!"}

@app.post("/chat")
def ask_gemini(request: ChatRequest):
    """
    This endpoint receives a message from the frontend, 
    sends it to Google Gemini, and returns the AI's response.
    """
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set on the server.")
    
    try:
        # Initialize the live Gemini client
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.message,
        )
        return {"response": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")