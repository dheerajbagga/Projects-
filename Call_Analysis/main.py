import streamlit as st
from Frontend.ui import get_user_input
from langchain_ollama import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Page title
st.title("🧠 Call Insight - Smart Transcript Analyzer")

# Get user input
user_prompt = get_user_input()

# Initialize LLM
llm = OllamaLLM(model="llama3.2")  # Ensure it's pulled

# Text splitter setup
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Size of each chunk in characters
    chunk_overlap=100,    # Overlap for better context retention
    separators=["\n\n", "\n", ".", " "]  # Smart split on sentences
)

# Submit button
if st.button("Submit"):
    if user_prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Transcript Generation & Analysis in Progress..."):
            # Step 1: Split into chunks
            chunks = splitter.split_text(user_prompt)

            # Step 2: Process each chunk
            responses = []
            for i, chunk in enumerate(chunks):
                st.write(f"🔍 Processing chunk {i+1} of {len(chunks)}")
                partial_response = llm.invoke(chunk)
                responses.append(partial_response)

            # Step 3: Combine results
            final_response = "\n\n".join(responses)

        # Display output
        st.subheader("📤 Response:")
        st.success(final_response)
