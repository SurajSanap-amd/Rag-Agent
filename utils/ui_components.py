import streamlit as st

def chat_message(role: str, text: str):
    if role == "user":
        st.markdown(f"🧑 **You:** {text}")
    else:
        st.markdown(f"🤖 **Agent:** {text}")
