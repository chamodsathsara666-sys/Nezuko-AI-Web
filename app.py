import streamlit as st
from groq import Groq
import base64

# 1. API Key එක
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.title("🌸 Nezuko AI")

# පින්තූරය base64 කරන්න හෙල්පර් ෆන්ක්ෂන් එකක්
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

# 2. පින්තූර එකපාරක් ලෝඩ් කර cache කර තබා ගැනීම (වේගය සඳහා)
if "cached_images" not in st.session_state:
    st.session_state.cached_images = {}
    paths = {"normal": "normal.png", "lovely": "lovely.png", "excited": "happy.png", "sad": "sad.png"}
    for key, path in paths.items():
        try:
            st.session_state.cached_images[key] = get_image_base64(path)
        except:
            st.session_state.cached_images[key] = ""

# --- CSS Floating Avatar (ලොකු කරලා සහ Smooth කරලා) ---
st.markdown("""
    <style>
    .nezuko-float {
        position: fixed;
        top: 80px;
        right: 20px;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 4px solid #ff99cc;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.5s ease;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Expressions Logic
if "expression" not in st.session_state:
    st.session_state.expression = "normal"

# Floating Image පෙන්වීම
img_base64 = st.session_state.cached_images.get(st.session_state.expression)
if img_base64:
    st.markdown(f'<img src="{img_base64}" class="nezuko-float">', unsafe_allow_html=True)

# 4. මැසේජ් පෙන්වීම
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="nezuko.png" if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# 5. චැට් ඉන්පුට්
if prompt := st.chat_input("Nezuko ගෙන් අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    history = st.session_state.messages[-15:]

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are Nezuko, a lovely anime character. 1. If this is the start, ask for the user's name politely.
