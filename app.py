import streamlit as st
from groq import Groq

st.title("🌸 Nezuko AI (Powered by Groq)")

api_key = st.text_input("Groq API Key එක මෙතැනට දෙන්න:", type="password")

if api_key:
    client = Groq(api_key=api_key)
    
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
            messages=[{"role": "user", "content": f"You are Nezuko. Answer: {prompt}"}],
            model="llama-3.3-70b-versatile",
        )
        
        response = chat_completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
