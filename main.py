import streamlit as st
from utils.page_manager import PageManager


def main():
    st.set_page_config(
        page_title="How Long Do Snails Sleep? 🐌",
        page_icon="💬",
        layout="wide",  # Make the layout wide for a cleaner design
        initial_sidebar_state="expanded",  # Sidebar open by default
    )
    page_manager = PageManager()

    # Title and intro text
    st.title("How Long Do Snails Sleep? 🐌")
    st.text("Welcome to the Snail Sleep Chatbot! Ask me anything about snail sleep.")
    # Description of the chatbot
    st.markdown(
        """
        This chatbot can answer questions related to snail sleep. 
        To start, type your question in the chatbox below and hit Enter.
        """
    )
    st.markdown("---")


if __name__ == "__main__":
    main()
