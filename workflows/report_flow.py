"""
REPORT Workflow
Generates summaries and analytical reports from logged data.
Uses RAG pattern to analyze all user logs and create formatted reports.
"""
import json
from langchain_config import get_llm_instance
from json_storage import read_logs

def report_flow(text: str, user_id: str) -> str:
    """
    Generates formatted reports from user's farm data.
    
    Args:
        text: User's report request (e.g., "sales report for this month")
        user_id: User identifier for data retrieval
        
    Returns:
        Formatted report with sections, totals, and summaries
    """
    # Retrieve all user's logs
    logs = read_logs(user_id=user_id)
    if not logs:
        return "⚠️ No logs found. Please log some data first."

    # 2. Create a much more robust RAG prompt for reporting
    logs_json_string = json.dumps(logs, indent=2)
    prompt_template = """You are a helpful farm assistant. Your task is to generate a report based on the user's request, using *only* the provided data logs.
- First, think step-by-step to analyze the logs and find the relevant information.
- Then, create a well-formatted report with a clear title, sections, and totals where appropriate.
- If the logs don't contain relevant information, state that clearly in the report.

Here are the data logs:
{logs_json_string}

Here is the user's request: {request}

Based on the logs, here is the report:"""
    prompt = prompt_template.format(logs_json_string=logs_json_string, request=text)

    # 3. Get report from LLM
    llm = get_llm_instance()
    report = llm.invoke(prompt)
    return report


