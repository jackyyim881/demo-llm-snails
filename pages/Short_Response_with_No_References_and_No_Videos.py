# pages/Short_Response_with_No_References_and_No_Videos.py

import streamlit as st
from common import RESPONSE_TYPES, get_prompt, generate_response, handle_feedback

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

            st.markdown(
                "<h4 style='font-size: 14px;'>How helpful was this response?</h4>", unsafe_allow_html=True)
            feedback = streamlit_feedback(feedback_type="thumbs", optional_text_label="[Optional] Please provide an explanation",
                                          )

            # Capture feedback and store it in Langsmith (and locally)
            if feedback:
                # Generate a unique run_id for traceability
                run_id = str(uuid.uuid4())

                try:
                    handle_feedback(response_type, user_input,
                                    bot_response, feedback, run_id)
                    logger.info(
                        f"Feedback logged successfully for run_id: {run_id}")

                    st.success("Thank you for your feedback!")
                except Exception as e:
                    st.error(f"Error logging feedback: {e}")


def main():
    response_type = "Short Response with No References and No Videos"

    st.header(f"{response_type}")

    display_chat_interface(response_type)


if __name__ == "__main__":
    main()
