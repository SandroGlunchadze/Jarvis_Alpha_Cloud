import streamlit as st
import brain

st.set_page_config(page_title="Jarvis Alpha", page_icon="🤖")
st.title("🤖 Jarvis Alpha (With Memory)")

# 1. Initialize History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display History on Screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handle New Input
# ... (Previous code remains the same)

if prompt := st.chat_input("Ask Jarvis... (Georgian or English)"):
    # A. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # B. Get Answer (With Translation Layer)
    with st.chat_message("assistant"):
        with st.spinner("Translating & Thinking..."):
            
            # We call the NEW bilingual function
            # It returns two things: 
            # 1. The reply (in your language)
            # 2. The English version (so we save the English version to memory for better context)
            response, english_prompt = brain.ask_jarvis_bilingual(prompt, st.session_state.messages)
            
            st.markdown(response)
            
    # C. Save Answer (We save the ENGLISH version to history so Jarvis stays smart)
    # This is a trick: You see Georgian, but Jarvis remembers English. 
    # This makes him much smarter over long conversations.
    st.session_state.messages.append({"role": "user", "content": english_prompt})
    st.session_state.messages.append({"role": "assistant", "content": response}) # Saving the visible reply
            
