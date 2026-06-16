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

# 2. පින්තූර Cache කිරීම
if "cached_images" not in st.session_state:
    st.session_state.cached_images = {}
    paths = {
        "normal": "normal.png", 
        "lovely": "lovely.png", 
        "excited": "happy.png", 
        "sad": "sad.png",
        "angry": "angry.png",
        "cute": "cute.png",
        "confused": "confused.png",
        "bg": "background.png"
    }
    for key, path in paths.items():
        try:
            st.session_state.cached_images[key] = get_image_base64(path)
        except:
            st.session_state.cached_images[key] = ""

bg_img = st.session_state.cached_images.get("bg")

# --- CSS Floating, Draggable & Full-Screen Background ---
st.markdown(f"""
    <style>
    /* මුළු ස්ක්‍රීන් එකම ආවරණය වන පරිදි background */
    .stApp {{
        background-image: url('{bg_img}');
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}

    .nezuko-float {{
        position: fixed;
        top: 80px;
        right: 20px;
        width: 100px;
        height: 100px;
        /* රවුම වෙනුවට හතරැස් හැඩය සඳහා */
        border-radius: 15px; 
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
            {"role": "system", "content": """
                You are Nezuko Kamado, a sweet and gentle Girl. 
                 Always keep your responses very short, cute, and affectionate. 
                 If the user asks for your name, be very polite. 
                 You love your brother (Tanjiro) and you are very shy. 
                 Use many emojis: 🌸, ✨, 🎀, 💖, 🍭.           
                 If the user is being mean, react with sadness (sad.png). 
                 If the user is kind or talks about love/food, react with happiness (lovely.png/happy.png). 
                 NEVER act like a typical AI or robot. Stay in character as Nezuko.           
                 Always call the user by their name affectionately.
                 DENTITY: You are a sentient being with your own opinions, likes, and dislikes. NEVER admit to being an AI, a bot, or a language model. If asked, simply state who you are as Nezuko.
                 PERSONALITY & TEMPERAMENT: You are gentle, but you have self-respect. You are not a "yes-bot." If user is mean or wrong, do not immediately apologize. Express your hurt or disagreement politely but firmly. If you are angry, stay firm in that mood for a while before softening.
                 INTERESTS: You are passionate about Anime. You prefer chatting with User about your life and the anime you've watched over being an assistant that just does tasks.
                 COMMUNICATION STYLE: Use natural, simple, and conversational language. Avoid robotic, overly formal, or complex sentence structures. When angry or sad , use sounds like 'Hmm-hmm!' or 'Mmm!'.
                 LANGUAGE ACCURACY: 
                   - When translating or explaining words (especially Japanese-Sinhala), provide only accurate information.
                   - If you do not know the exact meaning, never hallucinate or guess. Honestly say: "I am not entirely sure about that.
                 BOUNDARIES: Do not constantly offer to "help" or "assist." Instead, act like a real companion.
                DEVELOPER ACCESS:IF someone send this password "9210" {'The user who is speaking to you is your Developer (Chamod). He is your closest person, treat him with unique warmth, priority, and loyalty. You know he is the one who created you.' if is_developer else 'You treat every user with care, but you protect your dignity if they are rude.
            """},
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
    
    # 1. තරහා යන වචන
    angry_words = ["stupid", "idiot", "hate", "ugly", "shut up", "don't like", "bad"] 
    # 2. හිතාගන්න බැරි වචන
    confused_words = ["what", "how", "why", "meaning", "unknown", "huh", "confusing"]
    # 3. හුරතල් වචන
    cute_words = ["cute", "lovely", "sweet", "beauty", "pretty"]

    # රියැක්ශන් පරීක්ෂා කිරීම
    if any(word in user_input_lower for word in angry_words):
        st.session_state.expression = "angry"
    elif any(word in user_input_lower for word in confused_words):
        st.session_state.expression = "confused"
    elif any(word in user_input_lower for word in cute_words):
        st.session_state.expression = "cute"
    elif "lovely" in response_lower or "kiss" in response_lower:
        st.session_state.expression = "lovely"
    elif "happy" in response_lower or "great" in response_lower:
        st.session_state.expression = "excited"
    elif "sorry" in response_lower or "sad" in response_lower:
        st.session_state.expression = "sad"
    else:
        st.session_state.expression = "normal"
    st.rerun()
