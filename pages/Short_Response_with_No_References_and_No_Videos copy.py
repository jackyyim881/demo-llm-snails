import streamlit as st
from common import RESPONSE_TYPES, get_prompt, generate_response, handle_feedback, summarize_conversation
from streamlit_cookies_controller import CookieController
import uuid
from streamlit_feedback import streamlit_feedback
import logging
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration for a professional look
st.set_page_config(
    page_title="How Long Do Snails Sleep?",
    page_icon="🐌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Overall page background */
    .reportview-container {
        background: #f9f9f9;
    }
    /* Chat message styling */
    .stChatMessage p {
        font-size: 16px;
        line-height: 1.5;
    }
    /* Header and Title Styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #ffffff;
    }
    /* Button styling */
    div.stButton > button {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 0.5em 1em;
        border-radius: 5px;
        font-size: 14px;
    }
    div.stButton > button:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# Define available chatbot personas
PERSONAS = {
    "Professional": "You are a professional and formal assistant.",
    "Friendly": "You are a warm, friendly, and conversational assistant.",
    "Humorous": "You are witty, humorous, and fun while providing answers.",
}


def init_session_state(response_type):
    """Initialize session state variables if they don't exist."""
    chat_history_key = f"messages_{response_type}"
    if chat_history_key not in st.session_state:
        st.session_state[chat_history_key] = []
    if "chat_start_time" not in st.session_state:
        st.session_state["chat_start_time"] = time.time()
    if "selected_persona" not in st.session_state:
        st.session_state["selected_persona"] = "Professional"


def export_conversation(chat_history):
    """Export the conversation history as a JSON file."""
    export_data = json.dumps(chat_history, indent=2)
    st.download_button(
        label="Download Conversation",
        data=export_data,
        file_name="conversation.json",
        mime="application/json"
    )


def display_analytics(chat_history):
    """Display simple analytics about the conversation."""
    total_messages = len(chat_history)
    duration = time.time() - st.session_state.get("chat_start_time", time.time())
    st.markdown("### Conversation Analytics")
    st.markdown(f"**Total messages exchanged:** {total_messages}")
    st.markdown(f"**Conversation duration:** {int(duration)} seconds")


def display_chat_interface(response_type):
    init_session_state(response_type)
    chat_history_key = f"messages_{response_type}"
    chat_history = st.session_state[chat_history_key]

    # Container for chat messages
    chat_container = st.container()

    # Display chat messages from history
    for message in chat_history:
        with chat_container.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input in a dedicated container
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Append user message to chat history and display it
        chat_history.append({"role": "user", "content": user_input})
        with chat_container.chat_message("user"):
            st.markdown(user_input)

        # Prepare to generate assistant response including the selected persona prompt
        with chat_container.chat_message("assistant"):
            placeholder = st.empty()
            bot_response = ""
            # Combine the base prompt with the selected persona details
            persona_prompt = PERSONAS.get(
                st.session_state["selected_persona"], "")
            prompt = f"{persona_prompt}\n\n{
                get_prompt(user_input, response_type)}"
            try:
                # Stream response for a dynamic experience
                for partial_response in generate_response(prompt):
                    placeholder.markdown(f"**Bot:** {partial_response}")
                bot_response = partial_response
            except Exception as e:
                placeholder.error(f"An error occurred: {e}")

        # Append the bot response to the chat history if available
        if bot_response:
            chat_history.append({"role": "assistant", "content": bot_response})

            st.markdown(
                "<h4 style='font-size: 14px;'>How helpful was this response?</h4>",
                unsafe_allow_html=True
            )
            feedback = streamlit_feedback(
                feedback_type="thumbs",
                optional_text_label="[Optional] Please provide an explanation",
            )

            # Capture and handle feedback if provided
            if feedback:
                run_id = str(uuid.uuid4())
                try:
                    handle_feedback(response_type, user_input,
                                    bot_response, feedback, run_id)
                    logger.info(
                        f"Feedback logged successfully for run_id: {run_id}")
                    st.success("Thank you for your feedback!")
                except Exception as e:
                    st.error(f"Error logging feedback: {e}")

    # Buttons to export conversation and view analytics
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        export_conversation(chat_history)
    with col2:
        display_analytics(chat_history)


def main():
    # Instantiate the cookie controller for managing user sessions
    controller = CookieController()

    # Define session state variables for page and response type
    st.session_state["current_page"] = "Short_Response_with_No_References_and_No_Videos"
    st.session_state["response_type"] = "Short Response with No References and No Videos"
    controller.set('cookie_name', 'user_cookie')

    response_type = st.session_state["response_type"]

    # Sidebar for additional navigation, branding, and new feature controls
    with st.sidebar:
        st.image("https://via.placeholder.com/150", caption="Your Logo Here")
        st.header("Navigation")
        st.markdown("""
        - **Home**
        - **About**
        - **Contact**
        """)
        st.markdown("---")
        st.markdown(
            "This advanced AI assistant provides a professional and engaging experience.")
        st.markdown("### Agent Personality")
        selected_persona = st.radio("Select a Persona:", list(PERSONAS.keys()), index=list(
            PERSONAS.keys()).index(st.session_state["selected_persona"]))
        st.session_state["selected_persona"] = selected_persona
        st.markdown("---")
        st.markdown("### Conversation Summary")
        if st.button("Generate Summary"):
            summary = summarize_conversation(
                st.session_state[f"messages_{response_type}"])
            st.info(summary)

    # Main content area
    st.title("How Long Do Snails Sleep? 🐌")
    st.header(f"{response_type}")

    # Layout: Use columns if you need to split the screen (e.g., for extra info)
    col1, col2 = st.columns([3, 1])
    with col1:
        display_chat_interface(response_type)
    with col2:
        st.markdown("### Quick Info")
        st.markdown("""
        **Did you know?**  
        Snails can sleep for several days at a time under certain conditions.
        """)
        st.markdown("---")
        st.markdown(
            "Enhance your experience by providing feedback on responses.")


if __name__ == "__main__":
    main()
