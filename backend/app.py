import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

app = FastAPI(title="Gemini AI RAG Data Agent")

api_key = os.environ.get("GEMINI_API_KEY")

# Define the absolute path to our data file inside the container environment
DATA_FILE_PATH = "data/campaigns.csv"

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Data Agent Backend is online and reading the file!"}

@app.post("/chat")
def ask_data_agent(request: ChatRequest):
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set.")
    
    # 1. Read the local database file using Pandas
    try:
        if os.path.exists(DATA_FILE_PATH):
            df = pd.read_csv(DATA_FILE_PATH)
            # Convert the entire table into a clean text string format for the AI
            data_context = df.to_string(index=False)
        else:
            data_context = "No database file found."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read data file: {str(e)}")

    # 2. Build the "Augmented" prompt to ground the AI in reality
    system_instruction = (
        "You are an expert marketing data analytics agent. You have access to the following data table.\n"
        "Use ONLY this data to answer the user's question accurately. If the answer cannot be found, "
        "say 'I cannot find that information in the provided database.'\n\n"
        f"--- DATA START ---\n{data_context}\n--- DATA END ---\n"
    )

    try:
        client = genai.Client(api_key=api_key)
        
        # Combine instructions, data context, and user question
        full_prompt = f"{system_instruction}\nUser Question: {request.message}"
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )
        return {"response": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")