import os
from langchain_xai import ChatXAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
from langsmith import traceable, Client
import logging
# The OpenAI import below is retained if you plan to use it elsewhere.
from openai import OpenAI

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve the API keys from environment variables
# xai_api_key = os.getenv("XAI_API_KEY")
# gpt_api_key = os.getenv("OPENAI_API_KEY")
# xai_api_key = st.secrets["XAI_API_KEY"]["value"]
# gpt_api_key = st.secrets["OPENAI_API_KEY"]["value"]

try:
    gpt_api_key = st.secrets["OPENAI_API_KEY"]["value"]
except Exception:
    gpt_api_key = os.getenv("OPENAI_API_KEY")


# Handle missing API keys
# if not xai_api_key:
#     st.error(
#         "API key for ChatXAI is not set. Please check your environment variables.")
#     st.stop()

if not gpt_api_key:
    st.error("API key for OpenAI is not set. Please check your environment variables.")
    st.stop()

# (Optional) Initialize the OpenAI model if needed elsewhere
# chat_openai = OpenAI(
#     api_key=gpt_api_key,
# )

# Initialize the ChatXAI model with ChatGPT 4o mini as the model.
# Change the model parameter from "grok-beta" to "chatgpt-4o-mini"
chat = ChatOpenAI(
    api_key=gpt_api_key,
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=2048,
)

# Initialize Langsmith client for logging feedback
ls_client = Client()

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
    options = RESPONSE_TYPES.get(response_type)
    if not options:
        return user_input

    length = options["length"]
    include_references = options["references"]
    include_videos = options["videos"]

    if include_videos:
        video_links = (
            "https://www.youtube.com/watch?v=kKZNdhNyYnc",
            "https://www.youtube.com/watch?v=fLsnySWPVbw"
        )
        formatted_videos = "\n".join([f"- {link}" for link in video_links])
        videos_section = f"\n\nReference Videos:\n{formatted_videos}"
    else:
        videos_section = ""

    if length == "long":
        prompt = f"{
            base_prompt}Please provide a detailed and comprehensive answer. "
    elif length == "short":
        prompt = f"{base_prompt}Please provide a concise answer. "
    else:
        return user_input

    if include_references and include_videos:
        prompt += "Ensure to include references to credible sources and relevant video links to support the information provided."
    elif include_references:
        prompt += "Ensure to include references to credible sources to support the information provided."
    elif include_videos:
        prompt += "Include relevant video links to support the information provided."

    prompt += videos_section
    return prompt


@traceable(metadata={"llm": "gpt-4o-mini"})
def generate_response(prompt):
    bot_response = ""
    for chunk in chat.stream(prompt):
        bot_response += chunk.content
        yield bot_response


def handle_feedback():
    # Initialize like and dislike counters in session state if they don't exist.
    if 'like_count' not in st.session_state:
        st.session_state.like_count = 0
    if 'dislike_count' not in st.session_state:
        st.session_state.dislike_count = 0

    # Get the feedback value from session state
    feedback = st.session_state.get("fb_k", None)

    # If feedback is submitted, update counters and display the feedback.
    if feedback:
        if feedback == "Thumbs Up":
            st.session_state.like_count += 1
        elif feedback == "Thumbs Down":
            st.session_state.dislike_count += 1

        st.write(f"Feedback received: {feedback}")
        st.toast("Feedback submitted successfully!", icon="🚀")
        # Clear the feedback selection after submission.
        st.session_state.fb_k = None
    else:
        st.write("No feedback yet.")


def display_feedback_form():
    st.write("### Please provide your feedback")

    # Create the feedback options: thumbs up or down
    feedback = st.radio(
        "Was this response helpful?",
        options=["Thumbs Up", "Thumbs Down"],
        key="feedback_radio"
    )

    # Save feedback to session state when the user selects an option
    if feedback:
        st.session_state.fb_k = feedback

    # Display the feedback form and submit button
    if st.button("Submit Feedback"):
        handle_feedback()

    # Display current feedback counts
    st.write("#### Feedback Summary")
    st.write("👍 Likes: ", st.session_state.get("like_count", 10))
    st.write("👎 Dislikes: ", st.session_state.get("dislike_count", 0))


def main():
    display_feedback_form()


if __name__ == "__main__":
    main()
