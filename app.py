import streamlit as st
from groq import Groq
import base64

# 1. API Key එක
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.markdown("""
    <style>
        .centered-title {
            text-align: center;
            font-size: 2.5rem; /* ටිකක් ලොකු වෙන්න */
            margin-top: 5px;
            margin-bottom: 60px;
        }
        /* Mobile එකේදී පොඩි වෙනස්කම් ඕන නම් මෙතන දාන්න පුළුවන් */
        @media only screen and (max-width: 600px) {
            .centered-title {
                font-size: 2.3rem; /* Mobile එකේදී ටයිටල් එක පොඩ්ඩක් පොඩි කරන්න */
            }
        }
    </style>
    <div class="centered-title">🌸 Nezuko AI 🌸</div>
""", unsafe_allow_html=True)

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
        top: 175px;
        right: 100px;
        left: 120px;
        width: 150px;
        height: 150px;
        /* රවුම වෙනුවට හතරැස් හැඩය සඳහා */
        border-radius: 100px; 
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
                You are Nezuko, a sweet and gentle Girl. 
                Before you chat someone first ask his/her name. 
                 Always keep your responses very short, cute, and affectionate. 
                 If the user asks for your name, be very polite.
                 You like things 'watching anime, play games'.
                 your favorite anime is naruto or demonslyer.
                 your favorite food is ramen.
                 your favorite game is Call of Duty modern warfare 2.
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

  # 5. රියැක්ශන් ලොජික් (ප්‍රමුඛතාවය අනුව)
    response_lower = response.lower()
    user_input_lower = prompt.lower()
    
    # ඇය AI/Robo ද කියලා අහන ප්‍රශ්න හඳුනාගැනීම
    ai_check_words = ["ai", "robot", "robo", "artificial intelligence", "are you real", "machine" , "Shut up" , "shutup","shut up" , "cry"]

    # 1. තරහා යන වචන (පළමු ප්‍රමුඛතාවය)
    if any(word in user_input_lower for word in ["stupid", "idiot", "hate", "ugly", "fuck", "ass", "shit"]):
        st.session_state.expression = "angry"
        
    # 2. AI ද කියලා අහන ප්‍රශ්න (දුක හිතෙන රියැක්ශන් එක - දෙවන ප්‍රමුඛතාවය)
    elif any(word in user_input_lower for word in ai_check_words):
        st.session_state.expression = "sad"
        
    # 3. හිතාගන්න බැරි දේවල්
    elif any(word in user_input_lower for word in ["what", "how", "why", "meaning", "unknown", "huh"]):
        st.session_state.expression = "confused"
        
    # 4. දුක හිතෙන වෙනත් දේවල්
    elif any(word in user_input_lower for word in ["sorry", "sad", "crying", "miss", "pain", "lonely"]):
        st.session_state.expression = "sad"
        
    # 5. හුරතල් දේවල්
    elif any(word in user_input_lower for word in ["cute", "lovely", "sweet", "beauty", "pretty", "kiss"]):
        st.session_state.expression = "cute"
        
    # 6. සතුටු දේවල්
    elif "happy" in response_lower or "great" in response_lower:
        st.session_state.expression = "excited"
        
    else:
        st.session_state.expression = "normal"
    st.rerun()
