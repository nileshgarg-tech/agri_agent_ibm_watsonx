"""
LOG Workflow
Extracts structured data from natural language and saves to user's log file.
Example: "I sold 50 pounds of tomatoes for $75" → structured JSON entry
"""
import json
import re
import datetime as dt
from langchain_config import get_llm_instance
from db_storage import write_log

def extract_json_from_llm_response(raw_response: str) -> dict:
    """
    Robustly extracts JSON from LLM response that may include markdown blocks or commentary.
    
    Args:
        raw_response: Raw LLM output (may contain markdown, extra text, etc.)
    
    Returns:
        Parsed JSON dictionary
    
    Raises:
        ValueError: If no valid JSON found in response
    """
    # Strategy 1: Look for JSON inside markdown code block
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Strategy 2: Look for raw JSON object anywhere in response
    match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', raw_response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    # Strategy 3: Try the entire response (in case it's clean JSON)
    try:
        return json.loads(raw_response.strip())
    except json.JSONDecodeError:
        pass
    
    raise ValueError("No valid JSON found in LLM response")


def log_flow(text: str, user_id: str) -> str:
    """
    Extracts structured farm activity data from natural language input.
    
    Args:
        text: User's natural language description of farm activity
        user_id: User identifier for data isolation
        
    Returns:
        Confirmation message with logged activity details
    """
    # 1. Prompt LLM to extract structured fields from natural language
    prompt_template = '''You are a data entry assistant. From the user's statement, extract the key details into a structured JSON object.

Required fields:
- "action": What did the user do? Must be one of: 'sale', 'harvest', 'purchase', 'expense'
- "item": What is the subject of the log? (e.g., 'tomatoes', 'tractor fuel')

Optional fields:
- "quantity": A numerical quantity, if mentioned.
- "unit": The unit for the quantity (e.g., 'pounds', 'gallons', 'bags').
- "value_usd": The monetary value in USD, if mentioned.
- "note": Any other relevant details from the statement.

User statement: {text}

Return ONLY the JSON object, nothing else:'''
    prompt = prompt_template.format(text=text)

    # 2. Invoke LLM and parse with robust extraction
    llm = get_llm_instance()
    try:
        raw_json = llm.invoke(prompt)
        data = extract_json_from_llm_response(raw_json)
    except ValueError as e:
        return f"⚠️ Could not extract data from your statement. Please try being more specific.\n\nExample: 'I sold 50 lbs of tomatoes for $75'"
    except json.JSONDecodeError as e:
        return f"⚠️ Error parsing data. Please rephrase your activity.\n\nExample: 'Harvested 100 pounds of potatoes from west field'"

    # 3. Validate required fields
    if not data.get('action'):
        return f"⚠️ Please specify what you did (sale, harvest, purchase, or expense).\n\nExample: 'I sold 30 lbs of carrots for $50'"
    
    if not data.get('item'):
        return f"⚠️ Please specify what item this log is about.\n\nExample: 'Bought 5 bags of fertilizer for $120'"
    
    # Normalize action to lowercase for consistency
    data['action'] = data['action'].lower()
    
    # 4. Add timestamp and persist to SQLite
    data['timestamp'] = dt.datetime.now(dt.UTC).isoformat()
    
    try:
        write_log(data, user_id=user_id)
    except Exception as e:
        return f"⚠️ Database error: {str(e)}\n\nPlease try again or contact support."

    # 5. Return detailed confirmation
    item = data.get('item', 'item')
    action = data.get('action', 'activity')
    quantity = data.get('quantity')
    unit = data.get('unit', '')
    value = data.get('value_usd')
    
    # Build a nice confirmation message
    confirmation = f"✅ Logged: {action.capitalize()} of {item}"
    
    if quantity and unit:
        confirmation += f" ({quantity} {unit})"
    elif quantity:
        confirmation += f" ({quantity})"
    
    if value:
        confirmation += f" for ${value:.2f}"
    
    return confirmation + "."
