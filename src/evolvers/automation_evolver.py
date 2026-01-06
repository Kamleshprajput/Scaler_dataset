from utils.ids import uuid4
from utils.time import random_past_datetime
import random

def apply_automation_artifacts(conn, snapshot_id):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT task_id FROM tasks
        WHERE snapshot_id = ?
        AND completed = 0
        AND due_date IS NULL
        ORDER BY RANDOM()
        LIMIT 200
        """,
        (snapshot_id,),
    )

    tasks = cur.fetchall()

    for (task_id,) in tasks:
        if random.random() < 0.4:
            cur.execute(
                """
                INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    uuid4(),
                    snapshot_id,
                    task_id,
                    None,
                    "system",
                    "Auto-assigned by rule",
                    random_past_datetime(),
                ),
            )

        if random.random() < 0.3:
            cur.execute(
                """
                INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    uuid4(),
                    snapshot_id,
                    task_id,
                    None,
                    "system",
                    "SLA reminder: task approaching deadline",
                    random_past_datetime(),
                ),
            )

    conn.commit()
