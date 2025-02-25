import streamlit as st
import time
st.title("Chatbot - Short Version 3")
st.write("low accuracy")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me about snail sleep"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = "Snails are known to sleep a lot, sometimes for days, especially when the weather is dry."

    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed_response = ""
        for word in response.split():
            streamed_response += word + " "
            placeholder.markdown(streamed_response)
            time.sleep(0.05)

    st.session_state.messages.append(
        {"role": "assistant", "content": response})
