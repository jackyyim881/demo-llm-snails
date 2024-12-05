# pages/Short_Response_with_References_and_Videos.py

import streamlit as st
from common import RESPONSE_TYPES, get_prompt, generate_response, handle_feedback


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

        # Check if videos should be included based on response_type
        options = RESPONSE_TYPES.get(response_type)
        if options and options["videos"]:
            video_links = [
                "https://www.youtube.com/watch?v=kKZNdhNyYnc",
                "https://www.youtube.com/watch?v=fLsnySWPVbw"
            ]
            for link in video_links:
                st.video(link)

        # Append bot response to the conversation
        if bot_response:
            st.session_state[chat_history_key].append(
                {"role": "assistant", "content": bot_response})

            # Feedback Section
            col1, col2 = st.columns([2, 1])

            with col2:
                st.markdown(
                    "<h4 style='font-size: 14px;'>How helpful was this response?</h4>", unsafe_allow_html=True)
                feedback = st_feedback()

            if feedback:
                handle_feedback(response_type, user_input,
                                bot_response, feedback)


def st_feedback():
    from streamlit_feedback import streamlit_feedback
    return streamlit_feedback(feedback_type="thumbs", optional_text_label="[Optional] Please provide an explanation")


def main():
    response_type = "Short Response with References and Videos"

    st.header(f"{response_type}")
    st.title("How Long Do Snails Sleep? 🐌")
    display_chat_interface(response_type)


if __name__ == "__main__":
    main()
