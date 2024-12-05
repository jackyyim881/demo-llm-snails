import streamlit as st


def main():
    st.set_page_config(
        page_title="How Long Do Snails Sleep? 🐌",
        page_icon="💬",
        layout="wide",  # Make the layout wide for a cleaner design
        initial_sidebar_state="expanded",  # Sidebar open by default
    )

    # Title and intro text
    st.title("How Long Do Snails Sleep? 🐌")
    st.write("""
        Welcome to the Snail Sleep Chatbot!

        This application allows you to interact with a chatbot that answers questions about how long snails sleep. 
        Each page corresponds to a different response configuration, enabling you to test various prompt settings independently.

        **Instructions:**
        - Use the sidebar to navigate between different response types.
        - Each page provides unique responses based on response length, references, and video inclusion.
        - Provide feedback after each interaction to improve the system.
    """)

    # Mapping of pages to professional names and emojis


if __name__ == "__main__":
    main()
