import streamlit as st
from uuid import uuid4
from services.retriever import rag
from services.langsmith_service import send_feedback
from utils.response_generator import response_generator
from utils.logger import logger


def display_chat_interface(chat_history_key, openai_client):
    """
    Display the chat interface for the given chat history key and handle input/output.
    """

    # Ensure chat history is initialized in session state for the specific key
    if chat_history_key not in st.session_state:
        st.session_state[chat_history_key] = []

    # Display previous chat history
    for idx, message in enumerate(st.session_state[chat_history_key]):
        if message["role"] == "user":
            # Display user messages
            with st.chat_message("user"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            # Check if it's the latest assistant message
            if idx == len(st.session_state[chat_history_key]) - 1:
                # Display latest assistant message with streaming
                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    for partial_response in response_generator(message["content"]):
                        placeholder.markdown(partial_response)
                    # Add thumbs-up/thumbs-down feedback if not already provided
                    if not message.get("feedback"):
                        with st.container():
                            st.markdown(
                                "<h5 style='font-size: 14px;'>Was this response helpful?</h5>",
                                unsafe_allow_html=True,
                            )
                            # Feedback columns for thumbs-up and thumbs-down buttons
                            feedback_col1, feedback_col2 = st.columns(2)
                            with feedback_col1:
                                if st.button("👍", key=f"{chat_history_key}_thumb_up_{idx}"):
                                    message["feedback"] = {"score": 1}
                                    send_feedback(message.get(
                                        "run_id", str(uuid4())), 1.0)
                                    st.success(
                                        "Thanks for your positive feedback!")
                            with feedback_col2:
                                if st.button("👎", key=f"{chat_history_key}_thumb_down_{idx}"):
                                    message["feedback"] = {"score": 0}
                                    send_feedback(message.get(
                                        "run_id", str(uuid4())), 0.0)
                                    st.error("Thanks for your feedback!")
            else:
                # Display previous assistant messages without streaming
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
                    if not message.get("feedback"):
                        with st.container():
                            st.markdown(
                                "<h5 style='font-size: 14px;'>Was this response helpful?</h5>",
                                unsafe_allow_html=True,
                            )
                            run_id = str(uuid4())
                            feedback_col1, feedback_col2 = st.columns(2)
                            with feedback_col1:
                                if st.button("👍", key=f"{chat_history_key}_thumb_up_{idx}"):
                                    message["feedback"] = {"score": 1}
                                    send_feedback(message.get(
                                        "run_id", run_id), 1.0)
                                    st.success(
                                        "Thanks for your positive feedback!")
                            with feedback_col2:
                                if st.button("👎", key=f"{chat_history_key}_thumb_down_{idx}"):
                                    message["feedback"] = {"score": 0}
                                    send_feedback(message.get(
                                        "run_id", run_id), 0.0)
                                    st.error("Thanks for your feedback!")

    # User input
    user_input = st.chat_input("請輸入您的問題:")

    if user_input:
        # Add user message to chat history
        st.session_state[chat_history_key].append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant response
        run_id = str(uuid4())  # Unique ID for the response
        try:
            bot_response = rag(user_input, openai_client, langsmith_extra={
                "run_id": run_id, "metadata": {"user_id": "jacky"}
            })

            # Display assistant response with streaming
            st.session_state[chat_history_key].append(
                {
                    "role": "assistant",
                    "content": bot_response,
                    "run_id": run_id,
                    "feedback": None
                }
            )
            with st.chat_message("assistant"):
                placeholder = st.empty()
                for partial_response in response_generator(bot_response):
                    placeholder.markdown(partial_response)

            # Immediately show feedback for the latest assistant response
            with st.container():
                st.markdown(
                    "<h5 style='font-size: 14px;'>Was this response helpful?</h5>",
                    unsafe_allow_html=True,
                )
                feedback_col1, feedback_col2 = st.columns(2)
                with feedback_col1:
                    if st.button("👍", key=f"{chat_history_key}_thumb_up_latest"):
                        st.session_state[chat_history_key][-1]["feedback"] = {
                            "score": 1}
                        send_feedback(run_id, 1.0)
                        st.success("Thanks for your positive feedback!")
                with feedback_col2:
                    if st.button("👎", key=f"{chat_history_key}_thumb_down_latest"):
                        st.session_state[chat_history_key][-1]["feedback"] = {
                            "score": 0}
                        send_feedback(run_id, 0.0)
                        st.error("Thanks for your feedback!")
        except Exception as e:
            st.error("生成回應時出錯，請稍後再試。")
            logger.error(f"Error generating response: {e}")

        # Log session details
        logger.info(f"Session ID: {st.session_state.session_id} | User: {
                    user_input} | Bot: {bot_response}")
