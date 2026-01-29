"""
SQLite Storage Layer
Handles user-specific data persistence to SQLite databases.
Each user gets their own database file in data/ directory.
Provides robust querying and aggregation capabilities.
"""
import sqlite3
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime


def get_data_file_path(user_id: str) -> str:
    """
    Generates a safe filename for the user's database from their user ID.
    Example: "testuser@gmail.com" -> "data/testuser_data.db"
    """
    safe_filename = user_id.split('@')[0].replace('.', '_') + "_data.db"
    return os.path.join("data", safe_filename)


def get_db_connection(user_id: str) -> sqlite3.Connection:
    """
    Gets a connection to the user's SQLite database.
    Creates the database and schema if it doesn't exist.
    """
    data_file = get_data_file_path(user_id)
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    
    conn = sqlite3.Connection(data_file)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    
    # Create schema if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS farm_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            item TEXT NOT NULL,
            quantity REAL,
            unit TEXT,
            value_usd REAL,
            note TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create index for faster queries
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_timestamp 
        ON farm_logs(user_id, timestamp)
    """)
    
    conn.commit()
    return conn


def read_logs(user_id: str, limit: int = 100, action: Optional[str] = None) -> List[Dict]:
    """
    Reads logs for a specific user from their SQLite database.
    
    Args:
        user_id: User identifier
        limit: Maximum number of logs to return (default 100)
        action: Optional filter by action type ('sale', 'harvest', 'expense', 'purchase')
    
    Returns:
        List of log dictionaries, ordered by timestamp descending
    """
    conn = get_db_connection(user_id)
    
    query = """
        SELECT id, user_id, timestamp, action, item, quantity, unit, value_usd, note
        FROM farm_logs
        WHERE user_id = ?
    """
    params = [user_id]
    
    if action:
        query += " AND action = ?"
        params.append(action)
    
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    
    cursor = conn.execute(query, params)
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return logs


def write_log(entry: dict, user_id: str) -> bool:
    """
    Appends a new log entry to a specific user's SQLite database.
    
    Args:
        entry: Dictionary with keys: action, item, quantity, unit, value_usd, note, timestamp
        user_id: User identifier
    
    Returns:
        True if successful, False otherwise
    """
    # Validate required fields
    required_fields = ['action', 'item']
    if not all(entry.get(f) for f in required_fields):
        raise ValueError(f"Missing required fields: {required_fields}")
    
    conn = get_db_connection(user_id)
    
    # Ensure timestamp exists
    if 'timestamp' not in entry:
        entry['timestamp'] = datetime.now(datetime.UTC).isoformat()
    
    try:
        conn.execute("""
            INSERT INTO farm_logs (user_id, timestamp, action, item, quantity, unit, value_usd, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            entry.get('timestamp'),
            entry.get('action'),
            entry.get('item'),
            entry.get('quantity'),
            entry.get('unit'),
            entry.get('value_usd'),
            entry.get('note')
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        raise e


def get_summary_stats(user_id: str) -> Dict:
    """
    Get pre-computed statistics for a user's farm data.
    Returns totals and counts by action type.
    
    Returns:
        Dictionary with total_sales, total_expenses, total_entries, etc.
    """
    conn = get_db_connection(user_id)
    
    # Total sales revenue
    sales_result = conn.execute("""
        SELECT COALESCE(SUM(value_usd), 0) 
        FROM farm_logs 
        WHERE user_id = ? AND action = 'sale'
    """, (user_id,)).fetchone()
    
    # Total expenses
    expense_result = conn.execute("""
        SELECT COALESCE(SUM(value_usd), 0) 
        FROM farm_logs 
        WHERE user_id = ? AND action IN ('expense', 'purchase')
    """, (user_id,)).fetchone()
    
    # Total entries by action
    action_counts = conn.execute("""
        SELECT action, COUNT(*) as count, COALESCE(SUM(value_usd), 0) as total
        FROM farm_logs 
        WHERE user_id = ?
        GROUP BY action
    """, (user_id,)).fetchall()
    
    # Total entries
    total_count = conn.execute("""
        SELECT COUNT(*) FROM farm_logs WHERE user_id = ?
    """, (user_id,)).fetchone()
    
    conn.close()
    
    stats = {
        'total_sales': float(sales_result[0]),
        'total_expenses': float(expense_result[0]),
        'total_entries': int(total_count[0]),
        'by_action': {row['action']: {'count': row['count'], 'total': float(row['total'])} for row in action_counts}
    }
    
    return stats


def get_item_summary(user_id: str, item_name: Optional[str] = None) -> List[Tuple]:
    """
    Get aggregated data by item (e.g., total tomatoes sold, total carrots harvested).
    
    Args:
        user_id: User identifier
        item_name: Optional specific item to filter by
    
    Returns:
        List of tuples: (item, action, count, total_quantity, total_value)
    """
    conn = get_db_connection(user_id)
    
    query = """
        SELECT 
            item,
            action,
            COUNT(*) as count,
            COALESCE(SUM(quantity), 0) as total_quantity,
            COALESCE(SUM(value_usd), 0) as total_value
        FROM farm_logs
        WHERE user_id = ?
    """
    params = [user_id]
    
    if item_name:
        query += " AND LOWER(item) LIKE ?"
        params.append(f"%{item_name.lower()}%")
    
    query += " GROUP BY item, action ORDER BY total_value DESC"
    
    cursor = conn.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    return results
