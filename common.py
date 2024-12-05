import os
from langchain_xai import ChatXAI
from dotenv import load_dotenv
import streamlit as st
import sqlite3
from langsmith.wrappers import wrap_openai
from langsmith import traceable, Client
import uuid
import logging


# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
xai_api_key = os.getenv("XAI_API_KEY")
# xai_api_key = st.secrets["XAI_API_KEY"]["value"]

# Handle missing API key
if not xai_api_key:
    st.error(
        "API key for ChatXAI is not set. Please check your environment variables.")
    st.stop()

# Initialize the ChatXAI model with the API key
chat = ChatXAI(
    xai_api_key=xai_api_key,
    model="grok-beta",
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

# SQLite feedback table initialization
conn = sqlite3.connect('feedback.db', check_same_thread=False)
cursor = conn.cursor()

# Create feedback table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    response_type TEXT,
                    question TEXT,
                    response TEXT,
                    feedback TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()


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


@traceable(metadata={"llm": "grok-beta"})
def generate_response(prompt):
    bot_response = ""
    for chunk in chat.stream(prompt):
        bot_response += chunk.content
        yield bot_response


def store_feedback(response_type, question, response, feedback):
    cursor.execute('''INSERT INTO feedback (response_type, question, response, feedback)
                      VALUES (?, ?, ?, ?)''', (response_type, question, response, feedback))
    conn.commit()


def handle_feedback(response_type, user_input, bot_response, feedback, run_id):
    try:
        # Log feedback to SQLite (local database)
        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO feedback (response_type, question, response, feedback, run_id)
                          VALUES (?, ?, ?, ?, ?)''',
                       (response_type, user_input, bot_response, feedback, run_id))
        conn.commit()
        logger.info(f"Feedback inserted into database with run_id: {run_id}")

        # Send feedback to Langsmith (remote feedback service)
        ls_client.create_feedback(
            response_type=response_type,
            question=user_input,
            key="user-score",
            response=bot_response,
            feedback=feedback,
            run_id=run_id
        )
        logger.info(f"Feedback sent to Langsmith with run_id: {run_id}")

    except Exception as e:
        logger.error(f"Error in handle_feedback: {e}")
        st.error(f"Error logging feedback: {e}")


def display_feedback_form(response_type, question, response, run_id):
    st.write("### Please provide your feedback")
    feedback = st.radio("Was this response helpful?",
                        options=["Thumbs Up", "Thumbs Down"])

    if st.button("Submit Feedback"):
        handle_feedback(response_type, question, response, feedback, run_id)


def main():
    question = "Where do snails sleep?"
    response_type = "Short Response with References and Videos"

    # Generate response with Langchain & Langsmith tracing
    prompt = get_prompt(question, response_type)

    # Initialize the response generation process
    response_generator = generate_response(prompt)
    response = ""

    for chunk in response_generator:
        response = chunk  # Get the response as it's generated
        st.write(response)  # Display the response on Streamlit

    # Generate a unique run ID for traceability
    run_id = str(uuid.uuid4())

    # Display feedback form
    display_feedback_form(response_type, question, response, run_id)


if __name__ == "__main__":
    main()
