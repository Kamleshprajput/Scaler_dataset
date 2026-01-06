from utils.ids import uuid4
from utils.random import weighted_choice
from utils.time import random_past_datetime
import random

PROJECT_TYPES = {
    "product": 0.30,
    "marketing": 0.18,
    "it_automation": 0.15,
    "operations": 0.14,
    "support": 0.10,
    "knowledge": 0.08,
    "ai": 0.05,
}

def generate_projects(conn, snapshot_id, teams):
    cur = conn.cursor()
    projects = []

    for _ in range(len(teams) * 3):
        project_id = uuid4()
        project_type = weighted_choice(PROJECT_TYPES)
        team_id = random.choice(teams)

        cur.execute(
            """
            INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project_id,
                snapshot_id,
                team_id,
                f"{project_type.capitalize()} Project",
                project_type,
                None,
                "manual",
                "active",
                random_past_datetime(),
            ),
        )
        projects.append(project_id)

    conn.commit()
    return projects
