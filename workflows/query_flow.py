"""
QUERY Workflow
Answers questions about logged data using RAG (Retrieval-Augmented Generation).
Retrieves user's logs and provides them as context to LLM for accurate answers.
Uses SQLite for efficient data retrieval and pre-computed aggregations.
"""
import json
from langchain_config import get_llm_instance
from db_storage import read_logs, get_summary_stats, get_item_summary

def query_flow(text: str, user_id: str) -> str:
    """
    Answers questions about user's farm data using RAG pattern.
    
    Args:
        text: User's question about their logged data
        user_id: User identifier for data retrieval
        
    Returns:
        Answer based on user's actual logged data
    """
    # 1. Retrieve user's logs (most recent 100 entries)
    logs = read_logs(user_id=user_id, limit=100)
    if not logs:
        return "👋 You don't have any logged data yet. Try logging an activity first!\n\nExample: 'I sold 50 lbs of tomatoes for $75'"

    # 2. Get pre-computed statistics for accurate aggregations
    stats = get_summary_stats(user_id)
    item_summary = get_item_summary(user_id)
    
    # 3. Create enhanced RAG prompt with both raw logs and computed stats
    logs_json_string = json.dumps(logs[:20], indent=2)  # Show recent 20 for context
    
    # Format statistics nicely
    stats_summary = f"""
SUMMARY STATISTICS:
- Total Sales Revenue: ${stats['total_sales']:.2f}
- Total Expenses: ${stats['total_expenses']:.2f}
- Total Log Entries: {stats['total_entries']}

Breakdown by Action:
{json.dumps(stats['by_action'], indent=2)}

Top Items:
{json.dumps([{"item": r[0], "action": r[1], "count": r[2], "total_value": r[4]} for r in item_summary[:10]], indent=2)}
"""
    
    prompt_template = """You are a helpful farm assistant. Answer the user's question based *only* on the provided data.

You have access to:
1. Pre-computed statistics (use these for totals, sums, counts - they are accurate!)
2. Recent activity logs (for specific details and context)

{stats_summary}

RECENT ACTIVITY LOGS (last 20 entries):
{logs_json_string}

INSTRUCTIONS:
- Use the pre-computed statistics for any calculations (they're accurate SQL aggregations)
- Reference specific log entries for details when relevant
- If the answer isn't in the data, say so clearly
- Be conversational and friendly

USER'S QUESTION: {question}

ANSWER:"""
    
    prompt = prompt_template.format(
        stats_summary=stats_summary,
        logs_json_string=logs_json_string,
        question=text
    )

    # 4. Get answer from LLM
    llm = get_llm_instance("small")  # Use fast model for queries
    answer = llm.invoke(prompt)
    return answer


