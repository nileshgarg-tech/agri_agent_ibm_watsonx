"""
JSON Storage Layer
Handles user-specific data persistence to JSON files.
Each user gets their own file in data/ directory.
"""
import json
import os

def get_data_file_path(user_id: str) -> str:
    """
    Generates a safe filename for the user's data from their user ID.
    Example: "testuser@gmail.com" -> "data/testuser_data.json"
    """
    safe_filename = user_id.split('@')[0].replace('.', '_') + "_data.json"
    return os.path.join("data", safe_filename)

def read_logs(user_id: str):
    """Reads all logs for a specific user from their JSON file."""
    data_file = get_data_file_path(user_id)
    if not os.path.exists(data_file):
        return []
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def write_log(entry: dict, user_id: str):
    """Appends a new log entry to a specific user's JSON file."""
    data_file = get_data_file_path(user_id)
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    logs = read_logs(user_id)
    logs.append(entry)
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False) 