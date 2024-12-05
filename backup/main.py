import streamlit as st
from langchain_xai import ChatXAI
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()


# Retrieve the API key from environment variables
# xai_api_key = os.getenv("XAI_API_KEY")

xai_api_key = st.secrets["XAI_API_KEY"]["value"]

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
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    user_input = st.chat_input("You:")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append(
            {"role": "user", "content": user_input})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)

        # Add assistant response to chat history with placeholder
        with st.chat_message("assistant"):
            placeholder = st.empty()
            bot_response = ""
            prompt = get_prompt(user_input, response_mode)
            try:
                for partial_response in generate_response(prompt):
                    placeholder.markdown(f"**Bot:** {partial_response}")
                bot_response = partial_response
            except Exception as e:
                placeholder.error(f"An error occurred: {e}")

        # Append bot response to the conversation
        if bot_response:
            st.session_state.messages.append(
                {"role": "assistant", "content": bot_response})


if __name__ == "__main__":
    main()
