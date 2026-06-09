import streamlit as st
import requests

# Set a professional title for your chatbot web app
st.title("My AI Chatbot")
st.write("Welcome! This frontend talks directly to your FastAPI backend server.")

# Initialize an internal memory list to store the chat conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Loop through the list and display previous messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a visual chat input bar at the bottom of the screen
if prompt := st.chat_input("Ask me anything..."):
    # 1. Display the user's message right away
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Package the message and send it across the network to your FastAPI server
    try:
        # We target the exact address and custom '/chat' endpoint your backend is listening on
        response = requests.post("http://host.docker.internal:8000/chat", json={"message": prompt})
        
        if response.status_code == 200:
            # Extract the raw AI text out of the backend's JSON package
            bot_reply = response.json().get("response")
        else:
            bot_reply = "Error: The backend server received the message but returned a bad status code."
            
    except Exception as e:
        bot_reply = f"Error: Could not connect to the backend server. Is it running on port 8000? Details: {e}"

    # 3. Add the AI's response to the screen and memory history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)