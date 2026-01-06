from utils.ids import uuid4
from utils.time import random_past_datetime
import random

# Human-like system comment messages
SYSTEM_COMMENTS = [
    "This task was automatically assigned based on workload",
    "Reminder: This task is approaching its due date",
    "Auto-assigned to team member with matching skills",
    "SLA reminder: Please update status within 24 hours",
    "This task was created from an integration",
    "Automated assignment based on project workload",
    "Reminder: Task has been in progress for 5+ days",
    "Auto-assigned via workflow rule",
    "This task was moved to your project automatically",
    "System notification: Task requires attention",
]

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
                    random.choice(SYSTEM_COMMENTS),
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
                    random.choice(SYSTEM_COMMENTS),
                    random_past_datetime(),
                ),
            )

    conn.commit()
