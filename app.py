import streamlit as st
from groq import Groq
import base64

# 1. API Setup
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)
is_developer = True

st.markdown("""
    <style>
        .centered-title { text-align: center; font-size: 2.5rem; margin-top: 5px; margin-bottom: 60px; }
        .nezuko-float {
            position: fixed; top: 175px; right: 100px; left: 120px; width: 150px; height: 150px;
            border-radius: 100px; border: 4px solid #ff99cc; z-index: 10000;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3); cursor: grab; user-select: none;
        }
    </style>
    <div class="centered-title">🌸 Nezuko AI 🌸</div>
""", unsafe_allow_html=True)

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    except: return ""

if "cached_images" not in st.session_state:
    st.session_state.cached_images = {key: get_image_base64(path) for key, path in {
        "normal": "normal.png", "lovely": "lovely.png", "excited": "happy.png", 
        "sad": "sad.png", "angry": "angry.png", "cute": "cute.png", 
        "confused": "confused.png", "bg": "background.png"
    }.items()}

# State initialization
if "expression" not in st.session_state: st.session_state.expression = "normal"
if "messages" not in st.session_state: st.session_state.messages = []
if "play_song" not in st.session_state: st.session_state.play_song = False
if "ask_song" not in st.session_state: st.session_state.ask_song = False

# Display Character
img_base64 = st.session_state.cached_images.get(st.session_state.expression)
if img_base64: st.markdown(f'<img src="{img_base64}" class="nezuko-float">', unsafe_allow_html=True)

# Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="nezuko.png" if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Nezuko ගෙන් අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    # 1. Ask Song Logic Check
    if st.session_state.ask_song and any(word in prompt.lower() for word in ["yes", "ok", "fine", "sure"]):
        st.session_state.play_song = True
        st.session_state.ask_song = False
    elif st.session_state.ask_song:
        st.session_state.ask_song = False

    # 2. AI Response
    history = st.session_state.messages[-5:]
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": "You are Nezuko, a sweet anime girl. Always act in character. If the user is sad, ask: 'I'm worried about you... would you like me to sing a sweet song for you?'"}] + history,
        model="llama-3.3-70b-versatile",
    )
    response = chat_completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar="nezuko.png"): st.markdown(response)

    # 3. Trigger Ask Song
    if "sad" in response.lower() or "sorry" in response.lower():
        st.session_state.ask_song = True

    # 4. Reaction Logic
    user_input_lower = prompt.lower()
    if any(word in user_input_lower for word in ["stupid", "idiot", "hate"]): st.session_state.expression = "angry"
    elif any(word in user_input_lower for word in ["ai", "robot", "machine"]): st.session_state.expression = "sad"
    elif any(word in user_input_lower for word in ["sad", "sorry", "cry"]): st.session_state.expression = "sad"
    else: st.session_state.expression = "normal"

# 5. Play Song (Outside input block to ensure it renders)
if st.session_state.play_song:
    st.markdown("🌸 **Nezuko:** Hmm-hmm! 🎶 *Now hush, little baby, don't you cry... Everything's gonna be alright...* 🎀")
    try:
        st.audio("song.mp3", format="audio/mp3", autoplay=True)
    except: st.error("Song file not found.")
    st.session_state.play_song = False
