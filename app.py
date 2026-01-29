"""
AgriAgent Streamlit Web Interface
Provides a chat-based UI for the farming operations assistant.
"""
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- App Configuration (MUST BE FIRST STREAMLIT COMMAND) ---
st.set_page_config(
    page_title="Agri-Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Check if credentials are configured
def check_credentials():
    """Check if IBM WatsonX credentials are available"""
    # Check .env first (cleaner, no warnings)
    watsonx_url = os.getenv("WATSONX_URL")
    project_id = os.getenv("PROJECT_ID")
    apikey = os.getenv("WATSONX_APIKEY")
    
    # Only try Streamlit secrets if .env doesn't have them (for cloud deployment)
    if not all([watsonx_url, project_id, apikey]):
        try:
            watsonx_url = watsonx_url or st.secrets.get("WATSONX_URL")
            project_id = project_id or st.secrets.get("PROJECT_ID")
            apikey = apikey or st.secrets.get("WATSONX_APIKEY")
        except (AttributeError, FileNotFoundError, KeyError):
            pass
    
    # Show error only if credentials are truly missing
    if not all([watsonx_url, project_id, apikey]):
        st.error("⚠️ IBM WatsonX credentials not configured!")
        st.info("Please create a `.env` file with your credentials. See ENV_SETUP.txt for details.")
        st.stop()

check_credentials()

# Import after credentials check
from main import classifier_chain, log_flow, query_flow, report_flow, general_flow
from db_storage import read_logs

st.title("🤖 Agri-Agent")
st.caption("Your AI Farming Partner")

# --- User Authentication ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
    st.session_state.messages = []

# If user is not logged in, show login form
if not st.session_state.user_id:
    st.markdown("""
    ### Welcome! 👋
    
    AgriAgent helps you manage your farm operations through natural conversation:
    
    **📝 Log Activities** - "I sold 50 lbs of tomatoes for $75"  
    **📊 Query Your Data** - "What are my total sales?"  
    **📈 Generate Reports** - "Give me a weekly summary"  
    **🌱 Get Farming Advice** - "When should I plant garlic?"
    
    ---
    """)
    
    with st.form(key='login_form'):
        email_input = st.text_input("Enter your email to begin", key="email", placeholder="farmer@example.com")
        submit_button = st.form_submit_button(label='Start Session')

        if submit_button:
            if email_input:
                st.session_state.user_id = email_input
                st.rerun()
            else:
                st.warning("Please enter an email to start.")

# --- Main App Logic ---
else:
    st.success(f"Logged in as: **{st.session_state.user_id}**")
    
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to do?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    intent = classifier_chain.invoke({"user_input": prompt}).strip()
                    # Optional: Show intent in sidebar for debugging
                    # st.sidebar.text(f"Intent: {intent}")

                    output = ""
                    if intent == "LOG":
                        output = log_flow(prompt, user_id=st.session_state.user_id)
                    elif intent == "QUERY":
                        output = query_flow(prompt, user_id=st.session_state.user_id)
                    elif intent == "REPORT":
                        output = report_flow(prompt, user_id=st.session_state.user_id)
                    else: # GENERAL
                        output = general_flow(prompt)
                    
                    st.markdown(output)
                    st.session_state.messages.append({"role": "assistant", "content": output})

                except Exception as e:
                    error_message = f"⚠️ An error occurred: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
