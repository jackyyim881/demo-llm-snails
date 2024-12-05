import streamlit as st
from langchain_xai import ChatXAI
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
xai_api_key = os.getenv("XAI_API_KEY")
# Initialize the ChatXAI model with the API key
chat = ChatXAI(
    xai_api_key=xai_api_key,
    model="grok-beta",
)

# Define response types
RESPONSE_TYPES = {
    "Long Response": "long",
    "Short Response": "short",
}


def get_prompt(user_input, response_type):
    base_prompt = f"How long do snails sleep? {user_input}\n\n"
    if response_type == "long":
        return f"{base_prompt}Please provide a detailed and comprehensive answer with references to credible sources."
    elif response_type == "short":
        return f"{base_prompt}Please provide a concise answer with a reference to a credible source."
    else:
        return user_input


def generate_response(prompt):
    bot_response = ""
    # Stream the bot's response
    for chunk in chat.stream(prompt):
        bot_response += chunk.content
        yield bot_response


def display_message(message):
    """Display message with Like and Unlike buttons"""
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Create Like and Unlike buttons for each message
    like_button = st.button("👍 Like", key=f"like_{message['id']}")
    unlike_button = st.button("👎 Unlike", key=f"unlike_{message['id']}")

    # Store like/unlike status in session state (if not already stored)
    if 'liked' not in message:
        message['liked'] = None  # Default state if not set yet

    if like_button:
        st.session_state.messages[message['id']]['liked'] = True
    if unlike_button:
        st.session_state.messages[message['id']]['liked'] = False

    # Show like/unlike status
    status = ""
    if message['liked'] is not None:
        status = "Liked" if message['liked'] else "Unliked"
    st.markdown(f"Status: {status}")


def main():
    st.set_page_config(
        page_title="How long do snails sleep? 🐌",
        page_icon="💬",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.title("How long do snails sleep? 🐌")

    # Sidebar for selecting response type
    st.sidebar.header("Settings")
    response_type = st.sidebar.selectbox(
        "Select Response Type",
        options=list(RESPONSE_TYPES.keys()),
        index=0
    )
    response_mode = RESPONSE_TYPES[response_type]

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for i, message in enumerate(st.session_state.messages):
        message['id'] = i  # Add a unique identifier for each message
        display_message(message)

    # Accept user input
    user_input = st.text_input("You:")

    if user_input:
        # Add user message to chat history
        user_message = {"role": "user", "content": user_input,
                        "id": len(st.session_state.messages)}
        st.session_state.messages.append(user_message)

        # Display user message in chat message container
        display_message(user_message)

        # Assistant response (mockup for now)
        assistant_response = {"role": "assistant", "content": "This is the assistant's response!", "id": len(
            st.session_state.messages)}
        st.session_state.messages.append(assistant_response)

        # Display assistant message with like/unlike buttons
        display_message(assistant_response)


if __name__ == "__main__":
    main()
