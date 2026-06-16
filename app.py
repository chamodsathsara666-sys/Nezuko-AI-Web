import streamlit as st
from groq import Groq
import base64
import time
import random # 1. මෙය උඩින්ම එකතු කරන්න

# API Setup
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)
is_developer = True

# --- CSS & UI සැකසුම් ---
st.markdown("""
    <style>
        .centered-title { text-align: center; font-size: 2.5rem; margin-top: 5px; margin-bottom: 60px; }
        .nezuko-float {
            position: fixed; top: 175px; right: 100px; left: 120px; width: 150px; height: 150px;
            border-radius: 100px; border: 4px solid #ff99cc; z-index: 10000;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3); cursor: grab;
        }
        .stApp { background-size: cover !important; background-position: center center !important; }
    </style>
    <div class="centered-title">🌸 Nezuko AI 🌸</div>
""", unsafe_allow_html=True)

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    except: return ""

if "cached_images" not in st.session_state:
    st.session_state.cached_images = {k: get_image_base64(v) for k, v in {
        "normal": "normal.png", "sad": "sad.png", "cute": "cute.png", 
        "excited": "happy.png", "angry": "angry.png", "confused": "confused.png", "bg": "background.png"
    }.items()}

# --- Initialization ---
if "expression" not in st.session_state: st.session_state.expression = "normal"
if "messages" not in st.session_state: st.session_state.messages = []
if "play_song" not in st.session_state: st.session_state.play_song = False

# Background Image
bg_img = st.session_state.cached_images.get("bg")
if bg_img:
    st.markdown(f"<style>.stApp {{ background-image: url('{bg_img}'); }}</style>", unsafe_allow_html=True)

# Character Display
img_base64 = st.session_state.cached_images.get(st.session_state.expression)
if img_base64: st.markdown(f'<img src="{img_base64}" class="nezuko-float">', unsafe_allow_html=True)

# Chat Display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="nezuko.png" if msg["role"] == "assistant" else None):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input(" Ask from Nezuko ..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    # Song Logic
    if st.session_state.get("ask_song") and any(w in prompt.lower() for w in ["yes", "ok", "sure"]):
        st.session_state.play_song = True
        st.session_state.ask_song = False
    
    # API Call
    with st.spinner("Nezuko හිතමින් ඉන්නේ... 🌸"):
        time.sleep(1)
        history = st.session_state.messages[-6:]
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are Nezuko. Keep answers short, cute, and end with an emoji 🌸. If user is sad, ask to sing a song."}] + history,
            model="llama-3.1-8b-instant"
        )
        response = chat_completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Reaction Logic
    r = response.lower()
    if "sad" in r or "sorry" in r: st.session_state.expression = "sad"
    elif "happy" in r: st.session_state.expression = "excited"
    elif "cute" in r: st.session_state.expression = "cute"
    else: st.session_state.expression = "normal"
    
    if "sing a sweet song" in r: st.session_state.ask_song = True
    
    st.rerun()

  # 4. සින්දු Logic
song_list = ["song1.mp3", "song2.mp3", "song3.mp3"] 
song_keywords = ["sing a song", "play song", "සින්දුවක් කියන්න", "සින්දුවක් ඕන", "සින්දු","song", "i need song", "play a song" , "play song"]

if st.session_state.play_song and st.session_state.selected_song:
    st.audio(st.session_state.selected_song, format="audio/mp3")
    if st.button("සින්දුව නතර කරන්න 🛑"):
        st.session_state.play_song = False
        st.rerun()
