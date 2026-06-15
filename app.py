import streamlit as st
from groq import Groq
import base64

# 1. API Key එක
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.title("🌸 Nezuko AI 🌸")

# පින්තූරය base64 කරන්න හෙල්පර් ෆන්ක්ෂන් එකක්
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

# 2. පින්තූර Cache කිරීම (Background එකත් සමඟ)
if "cached_images" not in st.session_state:
    st.session_state.cached_images = {}
    paths = {
        "normal": "normal.png", 
        "lovely": "lovely.png", 
        "excited": "happy.png", 
        "sad": "sad.png",
        "bg": "background.png"
    }
    for key, path in paths.items():
        try:
            st.session_state.cached_images[key] = get_image_base64(path)
        except:
            st.session_state.cached_images[key] = ""

# Background image data එක ලබා ගැනීම
bg_img = st.session_state.cached_images.get("bg")

# --- CSS Floating, Draggable & Background Image ---
st.markdown(f"""
    <style>
    /* මුළු ඇප් එකටම Background එක දැමීම */
    .stApp {{
        background-image: url('{bg_img}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .nezuko-float {{
        position: fixed;
        top: 80px;
        right: 20px;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 4px solid #ff99cc;
        z-index: 10000;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        cursor: grab;
        user-select: none;
        -webkit-user-drag: none;
    }}
    .nezuko-float:active {{ cursor: grabbing; }}
    </style>
    <script>
    function initDraggable() {{
        const img = document.querySelector('.nezuko-float');
        if (!img) return;
        img.ondragstart = () => false;
        img.onmousedown = (e) => {{
            let shiftX = e.clientX - img.getBoundingClientRect().left;
            let shiftY = e.clientY - img.getBoundingClientRect().top;
            function moveAt(pageX, pageY) {{
                img.style.left = pageX - shiftX + 'px';
                img.style.top = pageY - shiftY + 'px';
                img.style.right = 'auto';
            }}
            function onMouseMove(e) {{ moveAt(e.pageX, e.pageY); }}
            document.addEventListener('mousemove', onMouseMove);
            document.onmouseup = () => {{ document.removeEventListener('mousemove', onMouseMove); }};
        }};
    }}
    window.onload = initDraggable;
    </script>
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
            {"role": "system", "content": "You are Nezuko, a lovely anime character. 1. If this is the start, ask for the user's name politely. 2. Remember the name and NEVER ask again. 3. Call the user by name affectionately. IMPORTANT: Always include plenty of cute emojis (🌸, ✨, 💖, 🎀). Reactions: 'lovely' -> lovely.png, 'happy' -> happy.png, 'sad' -> sad.png."},
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
