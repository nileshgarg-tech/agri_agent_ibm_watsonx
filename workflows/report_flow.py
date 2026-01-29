"""
REPORT Workflow
Generates summaries and analytical reports from logged data.
Uses RAG pattern to analyze all user logs and create formatted reports.
Uses granite-13b-chat-v2 for detailed, well-formatted reports.
"""
import json
from langchain_config import get_llm_instance
from db_storage import read_logs, get_summary_stats, get_item_summary

def report_flow(text: str, user_id: str) -> str:
    """
    Generates formatted reports from user's farm data.
    Uses granite-13b-chat-v2 for detailed, comprehensive reports.
    
    Args:
        text: User's report request (e.g., "sales report for this month")
        user_id: User identifier for data retrieval
        
    Returns:
        Formatted report with sections, totals, and summaries
    """
    # 1. Retrieve user's logs
    logs = read_logs(user_id=user_id, limit=200)  # Get more logs for comprehensive reports
    if not logs:
        return "👋 You don't have any logged data yet. Try logging some activities first!\n\nExample: 'I sold 50 lbs of tomatoes for $75'"

    # 2. Get pre-computed statistics and aggregations
    stats = get_summary_stats(user_id)
    item_summary = get_item_summary(user_id)
    
    # 3. Create enhanced RAG prompt with structured data
    logs_json_string = json.dumps(logs, indent=2)
    
    # Format item summary for better readability
    item_breakdown = []
    for row in item_summary:
        item_breakdown.append({
            "item": row[0],
            "action": row[1],
            "count": row[2],
            "total_quantity": row[3],
            "total_value_usd": row[4]
        })
    
    prompt_template = """You are a professional farm business analyst. Generate a comprehensive, well-formatted report based on the user's request using the provided farm data.

SUMMARY STATISTICS:
- Total Sales Revenue: ${total_sales:.2f}
- Total Expenses: ${total_expenses:.2f}
- Net Income: ${net_income:.2f}
- Total Activities Logged: {total_entries}

ACTION BREAKDOWN:
{action_breakdown}

ITEM-LEVEL BREAKDOWN:
{item_breakdown}

ALL ACTIVITY LOGS:
{logs_json_string}

USER'S REPORT REQUEST: {request}

INSTRUCTIONS:
- Create a professional, well-structured report with clear sections
- Use the pre-computed statistics (they are accurate SQL aggregations)
- Include relevant insights and trends from the data
- Format numbers clearly with dollar signs and units
- Add a summary section at the end
- Use markdown formatting (headers, bullet points, etc.) for readability

REPORT:"""
    
    prompt = prompt_template.format(
        total_sales=stats['total_sales'],
        total_expenses=stats['total_expenses'],
        net_income=stats['total_sales'] - stats['total_expenses'],
        total_entries=stats['total_entries'],
        action_breakdown=json.dumps(stats['by_action'], indent=2),
        item_breakdown=json.dumps(item_breakdown[:15], indent=2),  # Top 15 items
        logs_json_string=logs_json_string,
        request=text
    )

    # 4. Get report from LARGE model (granite-13b-chat-v2) for detailed output
    llm = get_llm_instance("large")
    report = llm.invoke(prompt)
    return report


