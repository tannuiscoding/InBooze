import os
from mindsdb_sdk import connect
from datetime import datetime

MINDSDB_URL = os.getenv("MINDSDB_URL", "http://127.0.0.1:47334")
KB_NAME = "inbooze_kb"

conn = connect(MINDSDB_URL)

def query_kb(query, sender_filter=None):
    """Run a semantic query + optional metadata filter."""
    where_clause = f"content LIKE '{query}'"
    if sender_filter:
        where_clause += f" AND metadata.sender = '{sender_filter}'"

    sql = f"""
        SELECT * FROM {KB_NAME}
        WHERE {where_clause}
        LIMIT 10;
    """
    try:
        results = conn.sql(sql).rows
        return results
    except Exception as e:
        print(f"[query_kb] Error: {e}")
        return []
