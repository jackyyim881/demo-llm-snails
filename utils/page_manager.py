import streamlit as st


class PageManager:
    def __init__(self):
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'

    def navigate_to(self, page):
        st.session_state.current_page = page

    def get_current_page(self):
        return st.session_state.current_page
