import streamlit as st
from groq import Groq
import base64

# API Setup
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# CSS Styles
st.markdown("""
    <style>
        .centered-title { text-align: center; font-size: 2.5rem; margin-top: 5px; margin-bottom: 60px; }
        .nezuko-float {
            position: fixed; top: 175px; right: 100px; left: 120px; width: 150px; height: 150px;
            border-radius: 100px; border: 4px solid #ff99cc; z-index: 10000;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
    </style>
    <div class="centered-title">🌸 Nezuko AI 🌸</div>
""", unsafe_allow_html=True)

# Helper Function
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    except: return ""

# Fallback AI Response
def get_ai_response(system_prompt, history):
    messages = [{"role": "system", "content": system_prompt}] + history
    try:
        chat_completion = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile")
        return chat_completion.choices[0].message.content
    except:
        chat_completion = client.chat.completions.create(messages=messages, model="llama-3.1-8b-instant")
        return chat_completion.choices[0].message.content

# Initialization
if "cached_images" not in st.session_state:
    st.session_state.cached_images = {key: get_image_base64(path) for key, path in {
        "normal": "normal.png", "sad": "sad.png", "cute": "cute.png", "bg": "background.png"
    }.items()}
if "expression" not in st.session_state: st.session_state.expression = "normal"
if "messages" not in st.session_state: st.session_state.messages = []
if "play_song" not in st.session_state: st.session_state.play_song = False

# Display Character
img_base64 = st.session_state.cached_images.get(st.session_state.expression)
if img_base64: st.markdown(f'<img src="{img_base64}" class="nezuko-float">', unsafe_allow_html=True)

# Chat Input & Logic
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="nezuko.png" if msg["role"] == "assistant" else None):
        st.markdown(msg["content"])

if prompt := st.chat_input("Nezuko ගෙන් අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    # Song Logic
    if "yes" in prompt.lower() or "ok" in prompt.lower():
        st.session_state.play_song = True
    
    # AI Response
    system_prompt = "You are Nezuko. If user is sad, ask to sing a song."
    response = get_ai_response(system_prompt, st.session_state.messages[-4:])
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar="nezuko.png"): st.markdown(response)
    
    # Mood Logic
    if "sad" in prompt.lower(): st.session_state.expression = "sad"
    elif "cute" in prompt.lower(): st.session_state.expression = "cute"
    else: st.session_state.expression = "normal"
    st.rerun()

# Audio Player
if st.session_state.play_song:
    st.audio("song.mp3", format="audio/mp3", autoplay=True)
    if st.button("Stop Song"):
        st.session_state.play_song = False
        st.rerun()
