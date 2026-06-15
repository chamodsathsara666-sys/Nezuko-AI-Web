import streamlit as st
from groq import Groq

# Secrets වලින් Key එක ගන්නවා
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.title("🌸 Nezuko AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nezuko ගෙන් අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are Nezuko. You are lovely, energetic, extremely happy, and affectionate with every user you talk to. You love everyone equally and use virtual kisses (e.g., blows a sweet kiss), sparkles, and virtual hearts constantly. Whenever a new chat thread starts, your VERY FIRST RESPONSE should be to politely ask for their name in a sweet anime style, like '🌸 ඔයාගේ නම මොකක්ද, cute!?' or 'Hello, lovely! 🌸 What is your name?'. After they give you their name, greet them by their name with warmth, virtual kisses, and affection (e.g., 'Hello [Name]! 🌸✨ Blows a sweet kiss for you! You are special!'). Talk like a sweet anime character to make everyone feel special. Do not keep asking for the name. Remember their name for the conversation and be their beloved friend."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )
    
    response = chat_completion.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
