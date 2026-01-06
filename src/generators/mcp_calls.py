from utils.ids import uuid4
import json
import random

QUERIES = [
    "Find my overdue tasks",
    "List incomplete support tickets",
    "Show tasks due this week",
]

def generate_mcp_calls(conn, snapshot_id, limit=30):
    cur = conn.cursor()

    for _ in range(limit):
        query = random.choice(QUERIES)
        cur.execute(
            """
            INSERT INTO mcp_tool_calls VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                uuid4(),
                snapshot_id,
                query,
                "asana.search_tasks",
                json.dumps({"query": query}),
                json.dumps({"results": []}),
            ),
        )

    conn.commit()
