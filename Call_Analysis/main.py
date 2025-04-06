import streamlit as st
from Frontend.ui import get_user_input
from langchain_ollama import OllamaLLM


# Page title
st.title("🧠 Call Insight - Smart Transcript Analyzer")

# Get user prompt from the frontend module
user_prompt = get_user_input()

# Initialize the Ollama model
llm = OllamaLLM(model="llama3.2")  # Make sure it's pulled with: ollama pull llama3.2

# On submit button click
if st.button("Submit"):
    if user_prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("LLaMA is thinking..."):
            response = llm.invoke(user_prompt)

        st.subheader("📤 Response:")
        st.success(response)
