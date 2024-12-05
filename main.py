# test.py

import streamlit as st


def main():
    st.set_page_config(
        page_title="How Long Do Snails Sleep? 🐌",
        page_icon="💬",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.title("How Long Do Snails Sleep? 🐌")
    st.write("""
        Welcome to the Snail Sleep Chatbot!

        This application allows you to interact with a chatbot that answers questions about how long snails sleep. 
        Each page corresponds to a different response configuration, enabling you to test various prompt settings independently.

        **Instructions:**
        - Use the sidebar to navigate to different response type pages.
        - Each page has predefined settings for response length, references, and video inclusion.
        - Engage in conversations and provide feedback on the responses.
    """)

    # Optional: Add an image related to snails
    # st.image("https://www.example.com/snail_image.jpg", use_column_width=True)


if __name__ == "__main__":
    main()
