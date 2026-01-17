import streamlit as st
import brain
import database
import re

st.set_page_config(page_title="Jarvis Architect", page_icon="🧠")
st.title("🤖 Jarvis: Senior Architect")

# 1. Initialize DB (Runs once)
database.init_db()

# 2. Display History (From Database, not just Session State)
# We load the last 5 exchanges to show on screen
history = database.load_last_n_messages(10)
for msg in history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Input Handling
if prompt := st.chat_input("Write your task (Georgian or English)..."):
    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Reply
    with st.chat_message("assistant"):
        with st.spinner("Analyzing & Coding..."):
            response, english_text = brain.ask_jarvis_bilingual(prompt)
            st.markdown(response)

            # --- 📥 FILE DOWNLOAD FEATURE ---
            # If Jarvis wrote Python code, make a button to download it
            code_match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
            if code_match:
                code_content = code_match.group(1)
                st.download_button(
                    label="📥 Download Code (.py)",
                    data=code_content,
                    file_name="jarvis_script.py",
                    mime="text/x-python"
                )
            # -------------------------------