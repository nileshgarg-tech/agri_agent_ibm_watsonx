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
    except (ImportError, FileNotFoundError, AttributeError, RuntimeError, KeyError):
        # Streamlit not available or secrets not configured, use env vars
        watsonx_url = os.getenv("WATSONX_URL")
        project_id = os.getenv("PROJECT_ID")
        apikey = os.getenv("WATSONX_APIKEY")
    
    return watsonx_url, project_id, apikey

# Initialize IBM Granite LLMs
# Supports two model types: "small" (fast) and "large" (detailed reports)
def get_llm(model_type="small"):
    """
    Get or create the LLM instance with credentials.
    
    Args:
        model_type: "small" for granite-4-h-small (fast, focused)
                   "large" for granite-13b-chat-v2 (detailed, reports)
    """
    watsonx_url, project_id, apikey = get_credentials()
    
    if model_type == "large":
        # For REPORT workflow - detailed summaries and analysis
        return WatsonxLLM(
            model_id="ibm/granite-13b-chat-v2",
            url=watsonx_url,
            project_id=project_id,
            apikey=apikey,
            params={
                "max_new_tokens": 2048,  # Higher limit for comprehensive reports
                "temperature": 0.3       # Slightly creative for better formatting
            }
        )
    else:
        # For LOG, QUERY, GENERAL - fast, deterministic
        return WatsonxLLM(
            model_id="ibm/granite-4-h-small",
            url=watsonx_url,
            project_id=project_id,
            apikey=apikey,
            params={
                "max_new_tokens": 512,   # Adequate for focused tasks
                "temperature": 0.0       # Deterministic output
            }
        )

# Lazy initialization - cache instances for both models
llm_small = None
llm_large = None

def get_llm_instance(model_type="small"):
    """
    Get LLM instance, creating it if needed.
    
    Args:
        model_type: "small" (default) or "large"
    """
    global llm_small, llm_large
    
    if model_type == "large":
        if llm_large is None:
            llm_large = get_llm("large")
        return llm_large
    else:
        if llm_small is None:
            llm_small = get_llm("small")
        return llm_small
