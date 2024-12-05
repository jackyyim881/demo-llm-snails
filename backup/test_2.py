import streamlit as st
from langchain_xai import ChatXAI
from dotenv import load_dotenv
import os

from datetime import datetime
from streamlit_feedback import streamlit_feedback


# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
xai_api_key = os.getenv("XAI_API_KEY")

# xai_api_key = st.secrets["XAI_API_KEY"]["value"]

# Initialize the ChatXAI model with the API key
chat = ChatXAI(
    xai_api_key=xai_api_key,
    model="grok-beta",
)

# Define response types
RESPONSE_TYPES = {
    "Long Response with References and Videos": {"length": "long", "references": True, "videos": True},
    "Long Response with References and No Videos": {"length": "long", "references": True, "videos": False},
    "Long Response with No References and Videos": {"length": "long", "references": False, "videos": True},
    "Long Response with No References and No Videos": {"length": "long", "references": False, "videos": False},
    "Short Response with References and Videos": {"length": "short", "references": True, "videos": True},
    "Short Response with References and No Videos": {"length": "short", "references": True, "videos": False},
    "Short Response with No References and Videos": {"length": "short", "references": False, "videos": True},
    "Short Response with No References and No Videos": {"length": "short", "references": False, "videos": False},
}


def get_prompt(user_input, response_type):
    base_prompt = f"How long do snails sleep? {user_input}\n\n"

    # Get the options from RESPONSE_TYPES
    options = RESPONSE_TYPES.get(response_type)
    if not options:
        return user_input  # Return input as is if response_type is unrecognized

    length = options["length"]
    include_references = options["references"]
    include_videos = options["videos"]

    # Prepare video links if videos are to be included
    if include_videos:
        video_links = (
            "https://www.youtube.com/watch?v=kKZNdhNyYnc",
            "https://www.youtube.com/watch?v=fLsnySWPVbw"
        )
        formatted_videos = "\n".join([f"- {link}" for link in video_links])
        videos_section = f"\n\nReference Videos:\n{formatted_videos}"
    else:
        videos_section = ""

    # Start building the prompt based on response length
    if length == "long":
        prompt = f"{
            base_prompt}Please provide a detailed and comprehensive answer. "
    elif length == "short":
        prompt = f"{base_prompt}Please provide a concise answer. "
    else:
        return user_input  # Return input as is if length is unrecognized

    # Add instructions based on references and videos inclusion
    if include_references and include_videos:
        prompt += "Ensure to include references to credible sources and relevant video links to support the information provided."
    elif include_references:
        prompt += "Ensure to include references to credible sources to support the information provided."
    elif include_videos:
        prompt += "Include relevant video links to support the information provided."
    else:
        prompt += ""  # No additional instructions

    # Append the videos section if videos are included
    prompt += videos_section

    return prompt


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
            prompt = get_prompt(user_input, response_type)
            try:
                for partial_response in generate_response(prompt):
                    placeholder.markdown(f"**Bot:** {partial_response}")
                bot_response = partial_response
            except Exception as e:
                placeholder.error(f"An error occurred: {e}")
        if "video" in bot_response:
            video_links = [
                "https://www.youtube.com/watch?v=kKZNdhNyYnc",
                "https://www.youtube.com/watch?v=fLsnySWPVbw"
            ]
            for link in video_links:
                st.video(link)

        # Append bot response to the conversation
        if bot_response:
            st.session_state.messages.append(
                {"role": "assistant", "content": bot_response})

            # Feedback Section
            # The ratio here determines the size of each column

            col1, col2 = st.columns([2, 1])
            # Display the chat messages and assistant responses here

            with col2:
                # Feedback Section in the right column
                st.markdown(
                    "<h4 style='font-size: 14px;'>How helpful was this response?</h4>", unsafe_allow_html=True)
                feedback = streamlit_feedback(feedback_type="thumbs")

            if feedback:
                # Store the feedback in session state
                if "feedbacks" not in st.session_state:
                    st.session_state.feedbacks = []

                # Store feedback along with the question and response
                st.session_state.feedbacks.append({
                    "question": user_input,
                    "response": bot_response,
                    "feedback": feedback
                })

                st.success("Thank you for your feedback!")

                # Optionally: Process feedback (store in DB, log, etc.)


if __name__ == "__main__":
    main()

# def get_prompt(user_input, response_type):
#     base_prompt = f"How long do snails sleep? {user_input}\n\n"
#     video_links = (
#         "https://www.youtube.com/watch?v=kKZNdhNyYnc",
#         "https://www.youtube.com/watch?v=fLsnySWPVbw"
#     )

#     # Create a formatted string of video links
#     formatted_videos = "\n".join([f"- {link}" for link in video_links])

#     if response_type == "long":
#         return (
#             f"{base_prompt}"
#             "Please provide a detailed and comprehensive answer. "
#             "Ensure to include references to credible sources and relevant video links to support the information provided.\n\n"
#             "Reference Videos:\n"
#             f"{formatted_videos}"
#         )
#     elif response_type == "short":
#         return (
#             f"{base_prompt}"
#             "Please provide a concise answer. "
#             "Include a reference to a credible source and a relevant video link to support the information.\n\n"
#             "Reference Videos:\n"
#             f"{formatted_videos}"
#         )

#     else:
#         return user_input
