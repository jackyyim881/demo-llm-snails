import streamlit as st
import importlib


def load_page_content(page_name):
    """Dynamically load and execute the main function of the selected page."""
    page_module = f"pages.{page_name.replace('.py', '')}"

    try:
        # Dynamically import the selected page's module
        module = importlib.import_module(page_module)

        # Run the main function from the module
        module.main()
    except ModuleNotFoundError as e:
        st.error(f"Page '{page_name}' could not be found. Error: {e}")


def main():
    st.set_page_config(
        page_title="How Long Do Snails Sleep? 🐌",
        page_icon="💬",
        layout="wide",  # Make the layout wide for a cleaner design
        initial_sidebar_state="expanded",  # Sidebar open by default
    )

    # Title and intro text
    if 'page_loaded' not in st.session_state or not st.session_state.page_loaded:
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
    page_mapping = {
        "Long_Response_with_References_and_Videos.py": "Long Response with References & Videos 📖🎥",
        "Long_Response_with_References_and_No_Videos.py": "Long Response with References (No Videos) 📖🚫",
        "Long_Response_with_No_References_and_Videos.py": "Long Response (No References) & Videos 🚫🎥",
        "Long_Response_with_No_References_and_No_Videos.py": "Long Response (No References, No Videos) 🚫🚫",
        "Short_Response_with_References_and_Videos.py": "Short Response with References & Videos 📑🎥",
        "Short_Response_with_References_and_No_Videos.py": "Short Response with References (No Videos) 📑🚫",
        "Short_Response_with_No_References_and_Videos.py": "Short Response (No References) & Videos 🚫🎥",
        "Short_Response_with_No_References_and_No_Videos.py": "Short Response (No References, No Videos) 🚫🚫",
    }

    # Dictionary to map response types to their respective pages
    categories = {
        "Long Responses 📝": [
            "Long_Response_with_References_and_Videos.py",
            "Long_Response_with_References_and_No_Videos.py",
            "Long_Response_with_No_References_and_Videos.py",
            "Long_Response_with_No_References_and_No_Videos.py",
        ],
        "Short Responses 🗨️": [
            "Short_Response_with_References_and_Videos.py",
            "Short_Response_with_References_and_No_Videos.py",
            "Short_Response_with_No_References_and_Videos.py",
            "Short_Response_with_No_References_and_No_Videos.py",
        ]
    }

    # Sidebar: Select the category of responses (Long vs Short)
    category = st.sidebar.radio(
        "Select Response Type:",
        options=list(categories.keys()),
        help="Select whether you want a long or short response type"
    )

    # Sidebar: Select the specific response page from the selected category
    selected_page = st.sidebar.selectbox(
        "Choose the response configuration:",
        options=[page_mapping[page] for page in categories[category]],
        help="Choose the specific response format for the chatbot"
    )

    # Get the actual file name for the selected friendly name with emoji
    selected_file = [key for key, value in page_mapping.items()
                     if value == selected_page][0]

    # When a page is selected, mark it as loaded and hide the main content
    if selected_page and ('page_loaded' not in st.session_state or not st.session_state.page_loaded):
        st.session_state.page_loaded = True

    # Load the content dynamically based on the selected page
    load_page_content(selected_file)


if __name__ == "__main__":
    main()
