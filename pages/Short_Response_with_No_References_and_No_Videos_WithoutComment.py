# pages/Short_Response_with_No_References_and_No_Videos.py

import streamlit as st
from common import RESPONSE_TYPES, get_prompt, generate_response, handle_feedback
from streamlit_cookies_controller import CookieController

import uuid
from streamlit_feedback import streamlit_feedback
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def display_chat_interface(response_type):
    # Initialize chat history specific to the response_type
    chat_history_key = f"messages_{response_type}"
    if chat_history_key not in st.session_state:
        st.session_state[chat_history_key] = []

    # Display chat messages from history
    for message in st.session_state[chat_history_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    user_input = st.chat_input("You:")

    if user_input:
        # Add user message to chat history
        st.session_state[chat_history_key].append(
            {"role": "user", "content": user_input})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)

        # Add assistant response to chat history with placeholder
        with st.chat_message("assistant"):
            placeholder = st.empty()
            bot_response = ""
            prompt = get_prompt(user_input, response_type)
            try:
                for partial_response in generate_response(prompt):
                    placeholder.markdown(f"**Bot:** {partial_response}")
                bot_response = partial_response
            except Exception as e:
                placeholder.error(f"An error occurred: {e}")

        # No videos to display for this response type

        # Append bot response to the conversation
        if bot_response:
            st.session_state[chat_history_key].append(
                {"role": "assistant", "content": bot_response})


def main():
    controller = CookieController()

    st.session_state["current_page"] = "Short_Response_with_No_References_and_No_Videos_WithoutComment"

    st.session_state["response_type"] = "Short Response with No References and No Videos"

    controller.set('cookie_name', 'user_cookie')

    response_type = "Short Response with No References and No Videos"

    st.title("How Long Do Snails Sleep? 🐌")
    with st.expander("Chatbot Description"):
        st.markdown(
            """
            **Chatbot Description:**

            This intelligent tool is designed to provide detailed answers to your questions about snail sleep habits. Once you ask a question, the chatbot will respond by streaming its answer word-by-word, creating a dynamic and engaging experience. In addition, where applicable, relevant video references are displayed to offer extra visual context about the topic. Dive in and discover fascinating facts about snails in an interactive way!
            """
        )
    st.header(f"{response_type}")

    display_chat_interface(response_type)


if __name__ == "__main__":
    main()
