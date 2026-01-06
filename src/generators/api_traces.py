from utils.ids import uuid4
import random
import json

ENDPOINTS = [
    ("/tasks", "POST"),
    ("/tasks", "GET"),
    ("/projects", "GET"),
    ("/custom_fields", "GET"),
]

def generate_api_traces(conn, snapshot_id, limit=100):
    cur = conn.cursor()

    for _ in range(limit):
        endpoint, method = random.choice(ENDPOINTS)
        cur.execute(
            """
            INSERT INTO api_call_traces VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                uuid4(),
                snapshot_id,
                random.choice(["user", "automation", "ai"]),
                method,
                endpoint,
                json.dumps({"sample": "request"}),
                json.dumps({"sample": "response"}),
                True,
                random.randint(20, 500),
            ),
        )

    conn.commit()
