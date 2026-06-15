import streamlit as st
from groq import Groq

# 1. API Key
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.title("🌸 Nezuko AI")

# --- CSS සඳහා Floating Avatar ---
st.markdown("""
    <style>
    .nezuko-float {
        position: fixed;
        top: 80px;
        right: 20px;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        border: 3px solid #ff99cc;
        z-index: 1000;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- EXPRESSION_IMAGES ---
EXPRESSION_IMAGES = {
    "normal": "normal.png",
    "lovely": "lovely.png",
    "excited": "happy.png",
    "sad": "sad.png",
}

if "expression" not in st.session_state:
    st.session_state.expression = "normal"

# --- Floating Image පෙන්වීම (Sidebar අයින් කළා) ---
img_src = EXPRESSION_IMAGES.get(st.session_state.expression, "normal.png")
st.markdown(f'<img src="{img_src}" class="nezuko-float">', unsafe_allow_html=True)

# 3. මැසේජ් පෙන්වීම
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="nezuko.png" if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# 4. චැට් ඉන්පුට්
if prompt := st.chat_input("Nezuko ගෙන් අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    history = st.session_state.messages[-15:]

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are Nezuko, a lovely anime character. Use emojis (🌸, ✨, 💖, 🎀). Remember user name. Reactions: 'lovely' -> lovely.png, 'happy' -> happy.png, 'sad' -> sad.png."},
        ] + history,
        model="llama-3.3-70b-versatile",
    )
    
    response = chat_completion.choices[0].message.content
    
    with st.chat_message("assistant", avatar="nezuko.png"):
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # රියැක්ශන් ලොජික්
    response_lower = response.lower()
    user_input_lower = prompt.lower()
    bad_words = ["fuck", "ass", "shit", "mad", "shut up"] 
    
    if any(word in user_input_lower for word in bad_words):
        st.session_state.expression = "sad"
    elif "lovely" in response_lower or "kiss" in response_lower:
        st.session_state.expression = "lovely"
    elif "happy" in response_lower or "great" in response_lower:
        st.session_state.expression = "excited"
    elif "sorry" in response_lower or "sad" in response_lower:
        st.session_state.expression = "sad"
    else:
        st.session_state.expression = "normal"
    
    st.rerun()
