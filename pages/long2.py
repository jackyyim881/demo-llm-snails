import streamlit as st
import time

st.title("Chatbot - Long Version 2")

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
    Snails are fascinating creatures when it comes to sleep. They can sleep for several hours each day, but under certain conditions, like during hibernation or estivation, they might sleep for weeks or even months. This extended sleep helps them survive in harsh environments, such as extreme heat or cold. During these periods, their metabolic rate slows down significantly, allowing them to conserve water and energy. However, it’s important to note that not all snails sleep for such long durations—some species are more active and sleep less.  
    **References:**  
    - Smith, L. (2018). ‘All About Animals,’ Nature Publishing  
    - Carter, J. (2019). ‘Snail Life,’ Garden Research Press  
    - Wong, M. (2021). ‘Hibernation Habits,’ BioFacts Journal
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
