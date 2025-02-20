import streamlit as st
import time

st.title("Chatbot - Short Version 1")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user prompt
if prompt := st.chat_input("Ask me about snail sleep"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = "Snails can sleep for up to three days at a time. They usually sleep in short bursts throughout the day."

    # Displaying the assistant's response with a word-by-word streaming effect
    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed_response = ""
        for word in response.split():
            streamed_response += word + " "
            placeholder.markdown(streamed_response)
            time.sleep(0.05)

    # Append the final response to session state
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
