import streamlit as st

def get_user_input():
    """
    UI function to get prompt from user via Streamlit.
    """
    return st.text_area("Enter your prompt for LLaMA 3.2:", height=150)
