import streamlit as st
import time

st.title("Chatbot - Long Version 3")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Ask me about snail sleep"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = """
    Snails’ sleep habits are quite different from those of other animals. They don’t have a fixed sleep schedule and can sleep at any time of day or night. Typically, snails sleep in short bursts, totaling around 15 hours a day. However, when conditions are unfavorable, such as during drought, they can enter a state of dormancy and sleep for up to three years. This ability to sleep for extended periods is a survival mechanism that helps them wait out challenging environmental conditions. During this time, they seal their shells with a layer of mucus to retain moisture.  
    **References:**  
    - Dr. Snailius, T. (2023). ‘Mollusk Mysteries Unveiled,’ Snail Science Review  
    - Evans, R. (2017). ‘Sleep in Nature,’ Wildlife Weekly  
    - Patel, S. (2020). ‘Snail Secrets,’ Earth Studies Digest
    """

    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed_response = ""
        for word in response.split():
            streamed_response += word + " "
            placeholder.markdown(streamed_response.strip(),
                                 unsafe_allow_html=True)
            time.sleep(0.01)

    st.session_state.messages.append(
        {"role": "assistant", "content": response})
    st.rerun()
