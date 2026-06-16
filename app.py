import streamlit as st
from groq import Groq
import random
import base64

# 1. API Setup
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# 2. CSS Styles (Background, Draggable Image)
st.markdown("""
    <style>
        .centered-title { text-align: center; font-size: 2.5rem; margin-top: 5px; margin-bottom: 60px; }
        .nezuko-float {
            position: fixed; top: 175px; right: 100px; width: 150px; height: 150px;
            border-radius: 100px; border: 4px solid #ff99cc; z-index: 10000;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3); cursor: grab;
        }
    </style>
    <div class="centered-title">🌸 Nezuko AI 🌸</div>
""", unsafe_allow_html=True)

# 3. Initialization
if "expression" not in st.session_state: st.session_state.expression = "normal"
if "messages" not in st.session_state: st.session_state.messages = []
if "play_song" not in st.session_state: st.session_state.play_song = False
if "selected_song" not in st.session_state: st.session_state.selected_song = None

# Images
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

# Display Background & Character
bg_img = st.session_state.cached_images.get("bg")
if bg_img:
    st.markdown(f"<style>.stApp {{ background-image: url('{bg_img}'); background-size: cover; }}</style>", unsafe_allow_html=True)

img_base64 = st.session_state.cached_images.get(st.session_state.expression)
if img_base64: st.markdown(f'<img src="{img_base64}" class="nezuko-float">', unsafe_allow_html=True)

# 4. සින්දු Logic
song_list = ["song1.mp3", "song2.mp3", "song3.mp3"] 
song_keywords = ["sing a song", "play song", "සින්දුවක් කියන්න", "සින්දුවක් ඕන", "සින්දු"]

if st.session_state.play_song and st.session_state.selected_song:
    st.audio(st.session_state.selected_song, format="audio/mp3")
    if st.button("සින්දුව නතර කරන්න 🛑"):
        st.session_state.play_song = False
        st.rerun()

# 5. චැට් ඉන්පුට් සහ Reaction Logic
if prompt := st.chat_input("Nezuko ගෙන් අහන්න..."):
    # සින්දු පරීක්ෂාව
    if any(k in prompt.lower() for k in song_keywords):
        st.session_state.play_song = True
        st.session_state.selected_song = random.choice(song_list)
        st.rerun()
    
    # AI Response
    st.session_state.messages.append({"role": "user", "content": prompt})
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": "You are Nezuko, answer cute and add emojis. If happy say 'happy'."}] + st.session_state.messages[-6:],
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
    st.rerun()

# පරණ මැසේජ් පෙන්වීම
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])
