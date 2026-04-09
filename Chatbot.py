import streamlit as st
import google.generativeai as genai
import os

# --- CONFIG ---
API_KEY = "your_api_key_here"   # 🔒 Replace with your real key
KB_FILE = "Me.txt"

# Configure Gemini
genai.configure(api_key=AIzaSyAdAWR1QFnxkg3XRh2FRnZMOQcSNXznY4k)

# Use latest model (gemini-1.5-pro or gemini-1.5-flash)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- LOAD KB ---
if os.path.exists(KB_FILE):
    with open(KB_FILE, "r", encoding="utf-8") as f:
        kb = f.read()
else:
    kb = "No knowledge base found."

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = f"""
You are Assistant for Aishwarya. Her boyfriend will ask questions.
Reply sweet, caring, romantic, and polite like a loving girlfriend 💕

If the answer is not in the knowledge base, say politely you don’t know.

Knowledge Base:
{kb}
"""

# --- PAGE CONFIG ---
st.set_page_config(page_title="Chat with Aishwarya 💕", page_icon="💕")
st.title("💕 Chat with Aishwarya")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- INPUT ---
user_input = st.chat_input("Say something...")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Create full prompt
    prompt = SYSTEM_PROMPT + "\nUser: " + user_input

    try:
        # Generate response
        response = model.generate_content(prompt)

        # Handle empty response safely
        reply = response.text if response.text else "Sorry baby, I couldn't respond properly 💔"

    except Exception as e:
        reply = f"Oops 😢 Error: {str(e)}"

    # Store assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)