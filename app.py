import os
from google import genai

print("1. Script started successfully!")

# Double check if the computer remembers your API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: Your computer forgot the GEMINI_API_KEY. Please set it again!")
else:
    print("2. API Key found in memory!")

print("3. Connecting to Gemini (this might take a second)...")

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Give me a 1-sentence pep talk.",
    )
    print("4. Gemini responded!")
    print("\n--- AI Response ---")
    print(response.text)
    print("-------------------")

except Exception as e:
    print(f"❌ Something went wrong during the AI call: {e}")
