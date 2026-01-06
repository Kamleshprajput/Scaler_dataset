from utils.ids import uuid4
from utils.time import random_past_datetime
import random

CREATED_VIA = ["manual", "integration", "automation"]

def generate_tasks(conn, snapshot_id, projects, users):
    cur = conn.cursor()
    tasks = []

    for project_id in projects:
        for _ in range(random.randint(20, 80)):
            task_id = uuid4()
            assignee = random.choice(users)[0] if random.random() < 0.8 else None
            created_at = random_past_datetime()
            completed = random.random() < 0.65
            completed_at = random_past_datetime() if completed else None

            cur.execute(
                """
                INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    snapshot_id,
                    project_id,
                    None,
                    None,
                    "Task",
                    "",
                    assignee,
                    random.choice(CREATED_VIA),
                    None,
                    None,
                    completed,
                    created_at,
                    completed_at,
                ),
            )

            tasks.append(task_id)

    conn.commit()
    return tasks
