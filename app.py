import streamlit as st
from groq import Groq

# 1. API Key එක
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.title("🌸 Nezuko AI")

# 2. පින්තූර සහ Expressions Logic
EXPRESSION_IMAGES = {
    "normal": "normal.png",
    "lovely": "lovely.png",
    "excited": "happy.png",
    "sad": "sad.png",
}

if "expression" not in st.session_state:
    st.session_state.expression = "normal"

# 3. ප්‍රධාන පින්තූරය පෙන්වීම
try:
    st.image(EXPRESSION_IMAGES[st.session_state.expression], width=400)
except:
    st.warning("පින්තූර ලෝඩ් වෙලා නැහැ, GitHub එකේ ෆයිල්ස් තියෙනවද බලන්න.")

# 4. මැසේජ් පෙන්වීම
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="nezuko.png"):
            st.markdown(message["content"])

# 5. චැට් ඉන්පුට් සහ රියැක්ශන් ලොජික්
if prompt := st.chat_input("Nezuko ගෙන් අහන්න..."):
    # User ගේ පණිවිඩය පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Groq API එක හරහා පිළිතුරු ලබාගැනීම
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are Nezuko. You are lovely, energetic, happy, and affectionate. If the user is Chamod, be extra sweet. Always ask for their name first. Based on your reply, use keywords like 'lovely', 'happy', or 'sad' to trigger reactions."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )
    
    response = chat_completion.choices[0].message.content
    
    # Assistant ගේ පිළිතුර පෙන්වීම
    with st.chat_message("assistant", avatar="nezuko.png"):
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # 6. අලුත් රියැක්ශන් ලොජික් එක (අසභ්‍ය වචනත් එක්ක)
    response_lower = response.lower()
    user_input_lower = prompt.lower()
    
    # මෙතනට ඔයාගේ අසභ්‍ය වචන ටික එකතු කරන්න
    bad_words = ["fuck", "ass", "shit","mad"] 
    
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
    
    # ඇප් එක අලුත් කරලා පින්තූරය මාරු කරන්න
    st.rerun()
