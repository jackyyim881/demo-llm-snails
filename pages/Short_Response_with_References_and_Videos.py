from services.langsmith_service import send_feedback
import os
import logging
import streamlit as st
from common import RESPONSE_TYPES, get_prompt, generate_response
from streamlit_feedback import streamlit_feedback
from langsmith import Client  # Import Langsmith Client
from uuid import uuid4
from streamlit_cookies_controller import CookieController
import streamlit_shadcn_ui as ui


# Directory where log files will be saved
ls_client = Client()

log_dir = 'logs'

os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'app.log')

# Configure the logging to output to both console and a log file
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

logger = logging.getLogger(__name__)


def handle_feedback():
    feedback = st.session_state.fb_k
    if feedback:
        feedback_type = feedback.get('type', 'No type')
        score = 1 if feedback.get('score') == '👍' else 0
        feedback_text = feedback.get('text', '')
        run_id = str(uuid4())

        try:
            # Send feedback to LangSmith service
            send_feedback(
                run_id=run_id,
                score=score,
                comment=feedback_text
            )

            logger.info(f"User feedback: {feedback_type} with score: {
                        score}, feedback text: {feedback_text}")
            st.toast("✔️ Feedback submitted successfully!")

        except Exception as e:
            logger.error(f"Error submitting feedback: {e}")
            st.error("Failed to submit feedback. Please try again.")
    else:
        st.write("No feedback was provided.")


def display_chat_interface(response_type):
    # Initialize chat history specific to the response_type
    chat_history_key = f"messages_{response_type}"
    if chat_history_key not in st.session_state:
        st.session_state[chat_history_key] = []

    # Display chat messages from history
    for message in st.session_state[chat_history_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("You:")

    if user_input:
        # Add user message to chat history
        st.session_state[chat_history_key].append(
            {"role": "user", "content": user_input})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)

        # Define the assistant avatar (🦜)
        avatar = "🦜"

        # Add assistant response to chat history with placeholder
        with st.chat_message("assistant", avatar=avatar):
            placeholder = st.empty()  # Create a placeholder for the response
            bot_response = ""
            # Get the prompt for the assistant
            prompt = get_prompt(user_input, response_type)

            try:
                # Generate response from the model incrementally
                for partial_response in generate_response(prompt):
                    placeholder.markdown(f"**Bot:** {partial_response}")
                bot_response = partial_response  # Set the final bot response
            except Exception as e:
                placeholder.error(f"An error occurred: {e}")

        # Check if videos should be included based on response_type
        options = RESPONSE_TYPES.get(response_type)
        if options and options.get("videos"):
            video_links = [
                "https://www.youtube.com/watch?v=kKZNdhNyYnc",
                "https://www.youtube.com/watch?v=fLsnySWPVbw"
            ]
            for link in video_links:
                st.video(link)

        # Append bot response to the conversation history
        if bot_response:
            st.session_state[chat_history_key].append(
                {"role": "assistant", "content": bot_response})

            # Feedback Section
            st.markdown(
                "<h4 style='font-size: 14px;'>How helpful was this response?</h4>", unsafe_allow_html=True)

            # Trigger the feedback interface after response
            display_feedback_form()


def display_feedback_form():
    with st.form('feedback_form', clear_on_submit=True):
        feedback = streamlit_feedback(
            feedback_type="thumbs",
            optional_text_label="[Optional] Please provide additional feedback",
            key="fb_k"
        )

        submit_button = st.form_submit_button(
            'Submit Feedback',
            on_click=handle_feedback,
            type="primary"
        )


def main():
    controller = CookieController()

    st.session_state['current_page'] = "Short_Response_with_References_and_Videos.py"
    st.session_state['response_type'] = "Short Response with References and Videos"
    controller.set('cookie_name', 'user_cookie')

    response_type = "Short Response with References and Videos"
    st.header(f"{response_type}")
    st.title("How Long Do Snails Sleep? 🐌")
    display_chat_interface(response_type)


if __name__ == "__main__":
    main()
