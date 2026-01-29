"""
AgriAgent Main Entry Point
Handles intent classification and workflow routing for farming assistant.

Architecture:
    User Input → Intent Classifier → Workflow Router → Specialized Workflow → Response
"""
import os
from dotenv import load_dotenv
load_dotenv()

# LangChain core components
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Shared Watsonx LLM instance
from langchain_config import get_llm_instance

# Storage layer (SQLite)
from db_storage import read_logs

# Workflows
from workflows.log_flow import log_flow
from workflows.query_flow import query_flow
from workflows.report_flow import report_flow
from workflows.general_flow import general_flow

# === Intent Classification Setup ===
# Load the routing prompt from file
with open("routing_prompt.txt", "r", encoding="utf-8") as f:
    routing_template = f.read()

routing_prompt = PromptTemplate.from_template(routing_template)

# Create classifier chain: Prompt → LLM → String Parser
# Returns one of: LOG, QUERY, REPORT, or GENERAL
# Initialize LLM lazily when chain is created
llm = get_llm_instance()
classifier_chain = routing_prompt | llm | StrOutputParser()


# === CLI Interface ===
if __name__ == "__main__":
    # Ask for user email, with a default
    email_input = input("Enter your email to begin (or press Enter for testuser@gmail.com): ").strip()
    if not email_input:
        current_user_id = "testuser@gmail.com"
    else:
        current_user_id = email_input
    
    print(f"\nAgri-Agent CLI – Logged in as {current_user_id}. Type 'exit' to quit.")

    while True:
        user_input = input("🎙️ ").strip()
        if user_input.lower() in ("exit", "quit", ""):  
            break

        # classify intent
        try:
            intent = classifier_chain.invoke({"user_input": user_input}).strip()
        except Exception as e:
            print(f"⚠️ Classification error: {e}\n")
            continue

        print(f"[*] Invoking workflow for intent: {intent}")
        # dispatch to the right workflow
        try:
            if intent == "LOG":
                output = log_flow(user_input, user_id=current_user_id)
            elif intent == "QUERY":
                output = query_flow(user_input, user_id=current_user_id)
            elif intent == "REPORT":
                output = report_flow(user_input, user_id=current_user_id)
            elif intent == "GENERAL":
                output = general_flow(user_input)
            else:
                # If the model outputs something unexpected, default to general.
                print(f"⚠️ Unknown intent '{intent}', defaulting to GENERAL.")
                output = general_flow(user_input)
        except Exception as e:
            output = f"⚠️ Workflow error ({intent}): {e}"

        print(f"[{intent}] {output}\n")

