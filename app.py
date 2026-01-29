"""
AgriAgent Streamlit Web Interface
Provides a chat-based UI for the farming operations assistant.
"""
import streamlit as st
import os

# Check if credentials are configured
def check_credentials():
    """Check if IBM WatsonX credentials are available"""
    try:
        watsonx_url = st.secrets.get("WATSONX_URL", os.getenv("WATSONX_URL"))
        project_id = st.secrets.get("PROJECT_ID", os.getenv("PROJECT_ID"))
        apikey = st.secrets.get("WATSONX_APIKEY", os.getenv("WATSONX_APIKEY"))
    except (AttributeError, FileNotFoundError):
        watsonx_url = os.getenv("WATSONX_URL")
        project_id = os.getenv("PROJECT_ID")
        apikey = os.getenv("WATSONX_APIKEY")
    
    if not all([watsonx_url, project_id, apikey]):
        st.error("⚠️ IBM WatsonX credentials not configured!")
        st.info("Please add your credentials to Streamlit Secrets or create a `.env` file. See ENV_SETUP.txt for details.")
        st.stop()

check_credentials()

from main import classifier_chain, log_flow, query_flow, report_flow, general_flow

# --- App Configuration ---
st.set_page_config(
    page_title="Agri-Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("🤖 Agri-Agent")
st.caption("Your AI Farming Partner")

# --- User Authentication ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
    st.session_state.messages = []

# If user is not logged in, show login form
if not st.session_state.user_id:
    with st.form(key='login_form'):
        email_input = st.text_input("Enter your email to begin", key="email")
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
                    st.write(f"_Intent classified as: {intent}_")

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
                    error_message = f"⚠️ An error occurred: {e}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
        st.rerun()
