from utils.ids import uuid4
import random

# Common section names that humans would use
SECTION_NAMES = [
    "To Do",
    "In Progress",
    "Review",
    "Done",
    "Backlog",
    "Blocked",
    "This Week",
    "Next Week",
    "Planning",
    "Design",
    "Development",
    "Testing",
    "Deployment",
    "Follow-up",
    "Ideas",
    "Priority",
    "Urgent",
    "Waiting",
    "On Hold",
]

def generate_sections(conn, snapshot_id, projects):
    """
    Generate sections for projects. Most projects have 3-6 sections.
    """
    cur = conn.cursor()
    sections = []

    for project_id in projects:
        # Most projects have sections, but not all
        if random.random() < 0.85:
            num_sections = random.randint(3, 6)
            chosen_names = random.sample(SECTION_NAMES, min(num_sections, len(SECTION_NAMES)))
            
            for position, name in enumerate(chosen_names):
                section_id = uuid4()
                sections.append((section_id, project_id))
                cur.execute(
                    "INSERT INTO sections VALUES (?, ?, ?, ?, ?)",
                    (section_id, project_id, snapshot_id, name, position),
                )

    conn.commit()
    return sections


