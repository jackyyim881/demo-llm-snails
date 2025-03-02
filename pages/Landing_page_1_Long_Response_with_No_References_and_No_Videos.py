import streamlit as st
from streamlit_js_eval import get_page_location
# Set page configuration
st.set_page_config(
    page_title="Snail Sleep Assignment",
    page_icon="🐌",
    layout="wide"
)


def main():
    # Custom CSS for a professional academic look
    st.markdown("""
        <style>
        .title {
            font-size: 40px;
            color: #2E8B57;
            text-align: center;
            font-weight: bold;
        }
        .warning {
            color: #FF4500;
            font-weight: bold;
            text-align: center;
        }
        .content {
            font-size: 18px;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title and intro
    st.markdown('<div class="title">Snail Sleep: A Critical Assignment 🐌</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="warning">Worth 50% of the Course Grade</div>',
                unsafe_allow_html=True)
    st.markdown("---")

    # Description and purpose
    st.markdown("""
    <div class="content">
        <h2>Assignment Overview</h2>
        <p>This project explores the fascinating topic of snail sleep, leveraging AI tools to create an informative and engaging study. As a major assessment contributing 50% to the final grade, this assignment requires a deep dive into the biology, behavior, and ecological significance of how snails rest. The use of AI is permitted, making this an innovative blend of technology and science.</p>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("pages/Long_Response_with_No_References_and_No_Videos.py",
                 label="Start Assignment", icon="🚀")


if __name__ == "__main__":
    main()
