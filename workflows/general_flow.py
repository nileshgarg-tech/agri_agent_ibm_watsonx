"""
GENERAL Workflow
Handles conversational queries and general farming advice.
No data access - uses LLM's base knowledge.
"""
from langchain_config import get_llm_instance

def general_flow(text: str) -> str:
    """
    Answers general farming questions using LLM's base knowledge.
    
    Args:
        text: User's general question or conversational input
        
    Returns:
        Helpful response for general queries, advice, or chitchat
    """
    prompt_template = """You are a helpful farm assistant. Provide a clear and concise answer to the user's question.

User Question: {question}

Answer:"""
    prompt = prompt_template.format(question=text)
    llm = get_llm_instance()
    return llm.invoke(prompt)
