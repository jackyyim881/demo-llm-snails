import streamlit as st
import time

st.title("Chatbot - Long Version 1")

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
    Snails have a unique sleep pattern where they can sleep for up to three days straight, especially during dry conditions when they need to conserve energy. Unlike humans, who have a circadian rhythm, snails’ sleep is more flexible and can occur in short naps or extended periods. They often find a safe spot, like under a leaf, and retract into their shells to rest. However, their sleep isn’t as deep as that of mammals, and they remain somewhat alert to their surroundings.  
    **References:**  
    - Johnson, P. (2020). ‘Snail Sleep Studies,’ Journal of Mollusk Behavior  
    - Lee, K. (2015). ‘Animals in Rest,’ Nature Insights  
    - Brown, T. (2022). ‘Sleepy Snails,’ EcoScience Monthly
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
