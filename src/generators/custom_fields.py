from utils.ids import uuid4
import random

FIELD_TYPES = ["enum", "number", "text"]

# Workspace-level custom fields based on reference files
WORKSPACE_FIELDS = [
    ("Priority", "enum", ["P0", "P1", "P2", "P3", "Low"]),
    ("Effort", "number", None),  # number field
    ("Notes", "text", None),  # text field
    ("Status", "enum", ["Not Started", "In Progress", "Blocked", "Done", "On Hold"]),
    ("Department", "enum", ["Engineering", "Marketing", "Operations", "IT", "Support"]),
    ("Budget", "number", None),
    ("Risk Level", "enum", ["Low", "Medium", "High", "Critical"]),
    ("Sprint", "enum", ["Sprint 1", "Sprint 2", "Sprint 3", "Backlog"]),
]

# Project-level custom fields
PROJECT_FIELDS = [
    ("Project Status", "enum", ["Planning", "Active", "On Hold", "Completed", "Archived"]),
    ("Phase", "enum", ["Discovery", "Design", "Development", "Testing", "Launch", "Maintenance"]),
    ("Budget", "number", None),
    ("Timeline", "enum", ["Q1", "Q2", "Q3", "Q4", "H1", "H2"]),
    ("Owner", "text", None),
    ("Stakeholders", "text", None),
]

def generate_custom_fields(conn, snapshot_id, projects, tasks):
    cur = conn.cursor()

    # ---- Workspace-level fields ----
    workspace_fields = []
    # Create 4-6 workspace fields randomly
    num_workspace_fields = random.randint(4, 6)
    selected_workspace_fields = random.sample(WORKSPACE_FIELDS, min(num_workspace_fields, len(WORKSPACE_FIELDS)))
    
    for name, ftype, enum_options in selected_workspace_fields:
        field_id = uuid4()
        workspace_fields.append((field_id, name, ftype, enum_options))
        cur.execute(
            """
            INSERT INTO custom_field_definitions VALUES (?, ?, ?, ?, ?)
            """,
            (field_id, name, ftype, "workspace", True),
        )

    # ---- Project-level fields ----
    project_fields = {}
    for project_id in projects:
        if random.random() < 0.65:  # 65% of projects have custom fields
            # 1-3 custom fields per project
            num_project_fields = random.randint(1, 3)
            selected_project_fields = random.sample(PROJECT_FIELDS, min(num_project_fields, len(PROJECT_FIELDS)))
            
            for name, ftype, enum_options in selected_project_fields:
                field_id = uuid4()
                if project_id not in project_fields:
                    project_fields[project_id] = []
                project_fields[project_id].append((field_id, name, ftype, enum_options))
                
                cur.execute(
                    "INSERT INTO custom_field_definitions VALUES (?, ?, ?, ?, ?)",
                    (field_id, name, ftype, "project", True),
                )
                cur.execute(
                    "INSERT INTO custom_field_settings VALUES (?, ?, ?, ?)",
                    (field_id, project_id, snapshot_id, True),
                )

    # ---- Assign values to tasks ----
    for task_id in tasks:
        # Assign workspace fields (70% of tasks)
        if random.random() < 0.7:
            field_id, name, ftype, enum_options = random.choice(workspace_fields)
            
            # Generate appropriate value based on field type
            if ftype == "enum" and enum_options:
                value = random.choice(enum_options) if random.random() < 0.85 else None
            elif ftype == "number":
                value = str(random.randint(1, 100)) if random.random() < 0.8 else None
            elif ftype == "text":
                value = random.choice(["Quick note", "Important", "Follow up", "Blocked"]) if random.random() < 0.7 else None
            else:
                value = None
                
            enabled = random.random() > 0.1  # 90% enabled
            cur.execute(
                """
                INSERT INTO custom_field_values VALUES (?, ?, ?, ?, ?)
                """,
                (task_id, field_id, snapshot_id, value, enabled),
            )
        
        # Assign project-level fields (50% of tasks)
        # Get project_id for this task
        cur.execute("SELECT project_id FROM tasks WHERE task_id = ? AND snapshot_id = ?", (task_id, snapshot_id))
        result = cur.fetchone()
        if result and result[0] in project_fields:
            if random.random() < 0.5:
                field_id, name, ftype, enum_options = random.choice(project_fields[result[0]])
                
                if ftype == "enum" and enum_options:
                    value = random.choice(enum_options) if random.random() < 0.85 else None
                elif ftype == "number":
                    value = str(random.randint(1000, 100000)) if random.random() < 0.8 else None
                elif ftype == "text":
                    value = random.choice(["John Doe", "Jane Smith", "Team Lead"]) if random.random() < 0.7 else None
                else:
                    value = None
                    
                enabled = random.random() > 0.1
                cur.execute(
                    """
                    INSERT INTO custom_field_values VALUES (?, ?, ?, ?, ?)
                    """,
                    (task_id, field_id, snapshot_id, value, enabled),
                )

    conn.commit()
