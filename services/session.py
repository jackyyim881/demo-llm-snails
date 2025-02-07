import streamlit as st
from uuid import uuid4


def initialize_session_state():
    """Initialize session state variables."""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid4())
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
