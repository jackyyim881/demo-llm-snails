import streamlit as st
from openai import OpenAI
from langsmith.wrappers import wrap_openai
import os


@st.cache_resource
def get_openai_client():
    api_key = os.getenv("XAI_API_KEY")  # Ensure your OpenAI API key is set
    if not api_key:
        st.error("請設置環境變量 XAI_API_KEY")
        st.stop()
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",  # Ensure this is a valid base URL
    )
    return wrap_openai(client)
