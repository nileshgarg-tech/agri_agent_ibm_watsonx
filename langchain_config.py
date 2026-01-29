"""
IBM WatsonX LLM Configuration
Initializes the Granite-13B language model for use across all workflows.
Supports both local .env and Streamlit Cloud secrets.
"""
import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM

# Load environment variables from .env (local)
load_dotenv()

def get_credentials():
    """Get credentials from Streamlit secrets or environment variables"""
    try:
        import streamlit as st
        watsonx_url = st.secrets.get("WATSONX_URL") or os.getenv("WATSONX_URL")
        project_id = st.secrets.get("PROJECT_ID") or os.getenv("PROJECT_ID")
        apikey = st.secrets.get("WATSONX_APIKEY") or os.getenv("WATSONX_APIKEY")
    except (ImportError, FileNotFoundError, AttributeError, RuntimeError):
        # Streamlit not available or secrets not configured, use env vars
        watsonx_url = os.getenv("WATSONX_URL")
        project_id = os.getenv("PROJECT_ID")
        apikey = os.getenv("WATSONX_APIKEY")
    
    return watsonx_url, project_id, apikey

# Initialize IBM Granite-13B LLM
# Using temperature=0.0 for deterministic, focused responses
def get_llm():
    """Get or create the LLM instance with credentials"""
    watsonx_url, project_id, apikey = get_credentials()
    return WatsonxLLM(
        model_id="ibm/granite-13b-instruct-v2",
        url=watsonx_url,
        project_id=project_id,
        apikey=apikey,
        params={
            "max_new_tokens": 256,  # Response length limit
            "temperature": 0.0       # Deterministic output
        }
    )

# Lazy initialization - only create when actually used
llm = None

def get_llm_instance():
    """Get LLM instance, creating it if needed"""
    global llm
    if llm is None:
        llm = get_llm()
    return llm
