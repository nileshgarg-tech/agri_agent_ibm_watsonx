"""
IBM WatsonX LLM Configuration
Initializes the Granite-13B language model for use across all workflows.
"""
import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM

load_dotenv()

# Initialize IBM Granite-13B LLM
# Using temperature=0.0 for deterministic, focused responses
llm = WatsonxLLM(
    model_id="ibm/granite-13b-instruct-v2",
    url=os.getenv("WATSONX_URL"),
    project_id=os.getenv("PROJECT_ID"),
    params={
        "max_new_tokens": 256,  # Response length limit
        "temperature": 0.0       # Deterministic output
    }
)
