import streamlit as st
from chatbot import get_response

st.set_page_config(page_title="Groq Chat Assistant", page_icon="icon.svg")
st.title("Chat with AI")

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({
        "role":"user",
        "content": user_input
    })
    
    with st.chat_message("user"):
        st.markdown(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = get_response(user_input)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                
                st.markdown(response)
                
            except Exception as error:
                st.error(f"Error: {error}")