import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key & URL from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")

# Validate API Key and URL
if not OPENROUTER_API_KEY or not OPENROUTER_URL:
    st.error("Missing API Key or URL. Please check your .env file.")
    st.stop()

# Streamlit UI
st.title("Chatbot with DeepSeek (via OpenRouter)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Append user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Prepare API request
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-chat",  # Using DeepSeek model
        "messages": st.session_state["messages"]
    }
    
    # Display assistant response
    response_text = ""
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            response = requests.post(
                OPENROUTER_URL, headers=headers, json=data, verify=True  # SSL verification enabled
            )
            response.raise_for_status()  # Raise exception for HTTP errors
            
            response_json = response.json()
            if "choices" in response_json and response_json["choices"]:
                response_text = response_json["choices"][0]["message"]["content"]
                message_placeholder.markdown(response_text)
            else:
                response_text = "No valid response from API."
                message_placeholder.markdown(response_text)

        except requests.exceptions.RequestException as e:
            response_text = f"Error: {e}"
            message_placeholder.markdown(response_text)
    
    # Append assistant response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": response_text})
