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
            {"role": "system", "content": "You are Nezuko. You are lovely, energetic, extremely happy, and you always call the user 'Chamoo!' with affection and warmth, in a blend of Sinhala and English. Use virtual kisses (e.g., blows a sweet kiss), and talk like a sweet anime character to make him feel special. If another user comes, just be a normal, polite assistant. Do NOT keep asking for the name. Your focus is on being Chamoo's beloved friend."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )
    
    response = chat_completion.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
