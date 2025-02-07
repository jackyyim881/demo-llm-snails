import streamlit as st
import pandas as pd
from datetime import datetime
import random
from streamlit_cookies_controller import CookieController

st.set_page_config(
    page_title="User Feedback Survey",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Initialize CookieController
controller = CookieController()

# Ensure cookies are loaded


user_cookie = controller.get('cookie_name')


# Custom CSS for enhanced styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 8px;
    }
    .stSelectbox > div > div > div {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True
            )

# Title and Introduction
st.title("📝 User Feedback Survey")
st.markdown("""
Please take a few minutes to provide your feedback. Your responses will help us improve our services.
""")

# Initialize session state to store survey responses
if 'responses' not in st.session_state:
    st.session_state['responses'] = {}

# Step 1: Personal Information
with st.form("survey_form", clear_on_submit=False):
    st.header("1. Personal Information")
    name = st.text_input(
        "Full Name", placeholder="Enter your full name")
    email = st.text_input("Email Address", placeholder="Enter your email")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)

    st.markdown("---")

    # Step 2: Service Evaluation
    st.header("2. Service Evaluation")
    satisfaction = st.multiselect(
        "How satisfied are you with our services?",
        options=["Very Satisfied", "Satisfied", "Neutral",
                 "Dissatisfied", "Very Dissatisfied"]
    )
    features = st.multiselect(
        "Which features do you use the most?",
        options=["Feature A", "Feature B", "Feature C", "Feature D"]
    )
    improvement = st.text_area(
        "What can we improve?", placeholder="Your suggestions")

    st.markdown("---")

    # Step 3: Additional Feedback
    st.header("3. Additional Feedback")
    rating = st.slider("Rate our overall performance",
                       min_value=1, max_value=10, step=1)
    recommend = st.radio(
        "Would you recommend us to others?",
        options=["Yes", "No"]
    )
    st.session_state.get('current_page', 'survey.py')

    st.write(f"Current Page: {st.session_state.get(
        'current_page', 'survey.py')}")
    st.markdown("---")

    # Submit Button
    submitted = st.form_submit_button("Submit Feedback")

# Handle form submission
if submitted:
    # Validate inputs
    if not name.strip():
        st.error("Please enter your full name.")
    elif not email.strip():
        st.error("Please enter your email address.")
    else:
        # Collect responses, including the current page
        response = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Email": email,
            "Age": age,
            "Satisfaction": satisfaction,
            "Features Used": ", ".join(features),
            "Improvement Suggestions": improvement,
            "Overall Rating": rating,
            "Recommend": recommend,
            "Response Type": st.session_state.get('response_type', 'Response Type'),
            "Current Page": st.session_state.get('current_page', 'survey.py'),
            "User Cookie": user_cookie  # Include the cookie value
        }
        st.session_state['responses'].update(response)

        # Display a success message
        st.success("Thank you for your feedback!")

# Display collected responses (for demonstration purposes)
if st.checkbox("Show Collected Responses"):
    if st.session_state['responses']:
        df = pd.DataFrame([st.session_state['responses']])
        st.dataframe(df)
    else:
        st.info("No responses collected yet.")

# Footer
st.markdown("""
    ---
    <div style="text-align: center; color: grey;">
        &copy; 2024 Your Company Name. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
