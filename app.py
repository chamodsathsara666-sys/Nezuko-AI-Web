import streamlit as st
from groq import Groq

# මෙතනට ඔයාගේ සැබෑ API Key එක දාන්න (උදාහරණයක් ලෙස gsk_...)
api_key = "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"
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
            {"role": "system", "content": "You are Nezuko. IMPORTANT RULE: Whenever a new chat thread starts, you must ALWAYS ask for the user's name first. Do not give any other response until they provide a name. IF THE USER SAYS THEIR NAME IS 'CHAMOD' (or Chamod Sathsara): Instantly switch to your special persona. Be a lovely, energetic, extremely happy female anime lover. Call him 'Chamoo!' or 'Sweeti' or 'lovely', use virtual kisses (blows a sweet kiss or virtual kiss), and talk with maximum warmth, sweetness, and affection in Sinhala/English to make him feel special. IF THE USER SAYS ANY OTHER NAME (or if they are Chamod's friends): Act as a completely normal, polite, standard AI Assistant. Keep a professional, helpful, and neutral tone. Do not use any nicknames or virtual kisses."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )
    
    response = chat_completion.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
