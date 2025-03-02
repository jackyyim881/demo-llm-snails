import streamlit as st
import uuid
from common import RESPONSE_TYPES, get_prompt, generate_response, handle_feedback
from streamlit_feedback import streamlit_feedback
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def display_chat_interface(response_type):
    chat_history_key = f"messages_{response_type}"
    toast_key = f"toast_{response_type}"

    # Initialize session state
    if chat_history_key not in st.session_state:
        st.session_state[chat_history_key] = []
    if toast_key not in st.session_state:
        st.session_state[toast_key] = {
            "show": False, "message": "", "icon": ""}

    # Display chat messages from history
    for message in st.session_state[chat_history_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Show toast if it was triggered previously
    if st.session_state[toast_key]["show"]:
        st.toast(st.session_state[toast_key]["message"],
                 icon=st.session_state[toast_key]["icon"])
        # Reset toast state after displaying (to avoid infinite loop)
        st.session_state[toast_key]["show"] = False

    # Accept user input
    user_input = st.chat_input("You:")
    if user_input:
        st.session_state[chat_history_key].append(
            {"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

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

        if bot_response:
            st.session_state[chat_history_key].append(
                {"role": "assistant", "content": bot_response})

            # Improved feedback section
            st.markdown(
                "<h4 style='font-size: 14px;'>How helpful was this response?</h4>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                fake_likes = 100
                if st.button(f"👍 Like ({fake_likes})", key=f"like_{uuid.uuid4()}"):
                    run_id = str(uuid.uuid4())
                    handle_feedback(response_type, user_input, bot_response, {
                                    "score": "positive"}, run_id)
                    st.success("Thanks for your feedback!")
                    # Set toast state
                    st.session_state[toast_key] = {
                        "show": True,
                        "message": "Thanks for your feedback!",
                        "icon": "👍"
                    }

            with col2:
                feedback = streamlit_feedback(
                    feedback_type="thumbs",
                    optional_text_label="[Optional] Tell us more",
                    key=f"fb_{uuid.uuid4()}"
                )
                if feedback:
                    run_id = str(uuid.uuid4())
                    handle_feedback(response_type, user_input,
                                    bot_response, feedback, run_id)
                    st.success("Thanks for your feedback!")
                    # Set toast state
                    st.session_state[toast_key] = {
                        "show": True,
                        "message": "Thanks for your feedback!",
                        "icon": "👍"
                    }


def main():
    st.header("Long Response with No References and No Videos")
    st.title("How Long Do Snails Sleep? 🐌")
    display_chat_interface("Long Response with No References and No Videos")


if __name__ == "__main__":
    main()
