import streamlit as st
from groq import Groq

# 1. API Key එක
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.title("🌸 Nezuko AI")

# --- EXPRESSION_IMAGES අර්ථ දැක්වීම ---
EXPRESSION_IMAGES = {
    "normal": "normal.png",
    "lovely": "lovely.png",
    "excited": "happy.png",
    "sad": "sad.png",
}

if "expression" not in st.session_state:
    st.session_state.expression = "normal"

# 2. Sidebar එකේ පින්තූරය පෙන්වීම
with st.sidebar:
    st.header("Nezuko's Mood")
    try:
        st.image(EXPRESSION_IMAGES[st.session_state.expression], width=300)
    except:
        st.warning("පින්තූර ලෝඩ් වුණේ නැහැ.")
    st.info("Nezuko හැමතිස්සෙම ඔයා එක්ක ඉන්නවා! ✨")

# 3. මැසේජ් පෙන්වීම
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="nezuko.png" if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# 4. චැට් ඉන්පුට් සහ රියැක්ශන් ලොජික්
if prompt := st.chat_input("Nezuko ගෙන් අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # මැසේජ් 15 කට සීමා කරලා API එකට යැවීම
    history = st.session_state.messages[-15:]

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are Nezuko, a lovely and affectionate anime character. 1. If this is the start of the conversation and you don't know the user's name, ask for it politely. 2. Once you get the name, remember it for the entire session and NEVER ask for it again. 3. When answering questions, call the user by their saved name affectionately and provide accurate answers. IMPORTANT: Always include plenty of cute emojis (🌸, ✨, 💖, 🎀) in every response. Use keywords like 'lovely', 'happy', or 'sad' to trigger reactions."},
        ] + history,
        model="llama-3.3-70b-versatile",
    )
    
    response = chat_completion.choices[0].message.content
    
    with st.chat_message("assistant", avatar="nezuko.png"):
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # 5. රියැක්ශන් ලොජික් එක
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
    
    # Memory Management
    if len(st.session_state.messages) > 30:
        st.session_state.messages = st.session_state.messages[-30:]

    st.rerun()
