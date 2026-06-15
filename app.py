import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nezuko AI", page_icon="🌸")
st.title("🌸 Nezuko AI Assistant")

# මෙතැනට ඔයාගේ Gemini API Key එක දෙන්න
api_key = st.text_input("Gemini API Key එක මෙතැනට දෙන්න:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Nezuko ගෙන් මොනවා හරි අහන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = model.generate_content(f"You are Nezuko from Demon Slayer. Act lovely and supportive. User says: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
