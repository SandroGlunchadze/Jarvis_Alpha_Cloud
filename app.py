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
if prompt := st.chat_input("Ask Jarvis..."):
    # A. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # B. Get Answer (SENDING FULL HISTORY NOW)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # We pass 'st.session_state.messages' which contains the whole chat
            response = brain.ask_jarvis(st.session_state.messages)
            st.markdown(response)
            
    # C. Save Answer
    st.session_state.messages.append({"role": "assistant", "content": response})