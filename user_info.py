import time
import streamlit as st


def user_info():
    question = 'let me get some basic info before I can help you with your query'
    st.text_area("Bot:", value=question, height=200, max_chars=None, key=None)
    question = 'Can you let me know your location ?'
    st.text_area("Bot:", value=question, height=200, max_chars=None, key=None)
    user_location = st.text_input("You: ")
    st.text_area("Bot:", value='Thank you', height=200, max_chars=None, key=None)



