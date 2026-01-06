from utils.ids import uuid4
import random

FIELD_TYPES = ["enum", "number", "text"]

def generate_custom_fields(conn, snapshot_id, projects, tasks):
    cur = conn.cursor()

    # ---- Workspace-level fields ----
    workspace_fields = []
    for name, ftype in [("Priority", "enum"), ("Effort", "number"), ("Notes", "text")]:
        field_id = uuid4()
        workspace_fields.append(field_id)
        cur.execute(
            """
            INSERT INTO custom_field_definitions VALUES (?, ?, ?, ?, ?)
            """,
            (field_id, name, ftype, "workspace", True),
        )

    # ---- Project-level fields ----
    project_fields = {}
    for project_id in projects:
        if random.random() < 0.6:
            field_id = uuid4()
            project_fields[project_id] = field_id
            cur.execute(
                "INSERT INTO custom_field_definitions VALUES (?, ?, ?, ?, ?)",
                (field_id, "Project Status", "enum", "project", True),
            )
            cur.execute(
                "INSERT INTO custom_field_settings VALUES (?, ?, ?, ?)",
                (field_id, project_id, snapshot_id, True),
            )

    # ---- Assign values to tasks ----
    for task_id in tasks:
        if random.random() < 0.7:
            field_id = random.choice(workspace_fields)
            value = random.choice(["P0", "P1", "P2"]) if random.random() < 0.8 else None
            enabled = random.random() > 0.1  # disabled edge case
            cur.execute(
                """
                INSERT INTO custom_field_values VALUES (?, ?, ?, ?, ?)
                """,
                (task_id, field_id, snapshot_id, value, enabled),
            )

    conn.commit()
