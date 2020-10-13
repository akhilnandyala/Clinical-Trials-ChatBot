import time
import streamlit as st


def user_info():
    question = 'let me get some basic info before I can help you with your query'
    display_output(question)
    question = 'Can you let me know your location ?'
    display_output(question)
    user_location = take_input()
    question = 'Thank you'
    display_output(question)

def display_output(question):
    st.text_area("Bot:", value=question, height=200, max_chars=None, key=None)

def take_input():
    answer = st.text_input("You: ")
    return answer


