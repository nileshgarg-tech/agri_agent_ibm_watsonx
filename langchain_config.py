"""
IBM WatsonX LLM Configuration
Initializes the Granite-13B language model for use across all workflows.
Supports both local .env and Streamlit Cloud secrets.
"""
import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM

# Load environment variables from .env (local) or use Streamlit secrets (cloud)
load_dotenv()

# Try to get Streamlit secrets first (for cloud deployment), fall back to env vars
try:
    import streamlit as st
    watsonx_url = st.secrets.get("WATSONX_URL", os.getenv("WATSONX_URL"))
    project_id = st.secrets.get("PROJECT_ID", os.getenv("PROJECT_ID"))
    apikey = st.secrets.get("WATSONX_APIKEY", os.getenv("WATSONX_APIKEY"))
except (ImportError, FileNotFoundError, AttributeError):
    # Streamlit not available or secrets not configured, use env vars
    watsonx_url = os.getenv("WATSONX_URL")
    project_id = os.getenv("PROJECT_ID")
    apikey = os.getenv("WATSONX_APIKEY")

# Initialize IBM Granite-13B LLM
# Using temperature=0.0 for deterministic, focused responses
llm = WatsonxLLM(
    model_id="ibm/granite-13b-instruct-v2",
    url=watsonx_url,
    project_id=project_id,
    apikey=apikey,
    params={
        "max_new_tokens": 256,  # Response length limit
        "temperature": 0.0       # Deterministic output
    }
)
