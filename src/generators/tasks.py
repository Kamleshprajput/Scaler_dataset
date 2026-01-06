from utils.ids import uuid4
from utils.time import random_past_datetime
from datetime import timedelta
import random

CREATED_VIA = ["manual", "integration", "automation"]

# Human-like task names
TASK_TEMPLATES = [
    "Review {item} proposal",
    "Update {item} documentation",
    "Fix bug in {item} module",
    "Design {item} feature",
    "Implement {item} functionality",
    "Test {item} integration",
    "Deploy {item} to production",
    "Create {item} report",
    "Schedule {item} meeting",
    "Follow up on {item}",
    "Prepare {item} presentation",
    "Refactor {item} code",
    "Optimize {item} performance",
    "Add {item} validation",
    "Update {item} dependencies",
    "Configure {item} settings",
    "Troubleshoot {item} issue",
    "Plan {item} sprint",
    "Review {item} pull request",
    "Write {item} tests",
    "Update {item} API",
    "Create {item} dashboard",
    "Analyze {item} metrics",
    "Set up {item} monitoring",
    "Migrate {item} database",
]

TASK_ITEMS = [
    "user authentication",
    "payment processing",
    "email notifications",
    "search functionality",
    "data export",
    "reporting system",
    "API endpoints",
    "frontend components",
    "database schema",
    "deployment pipeline",
    "monitoring tools",
    "security features",
    "user interface",
    "mobile app",
    "web dashboard",
]

TASK_DESCRIPTIONS = [
    "Need to complete this by end of week",
    "This is a high priority item",
    "Blocked waiting on external dependency",
    "Requires approval from manager",
    "Part of Q1 roadmap",
    "Customer requested feature",
    "Technical debt cleanup",
    "Performance improvement",
    "Security enhancement",
    "",
    "",
    "",
]

def generate_tasks(conn, snapshot_id, projects, users, section_map=None):
    cur = conn.cursor()
    tasks = []
    
    if section_map is None:
        section_map = {}

    for project_id in projects:
        # Get sections for this project
        project_sections = section_map.get(project_id, [])
        
        for _ in range(random.randint(20, 80)):
            task_id = uuid4()
            assignee = random.choice(users)[0] if random.random() < 0.8 else None
            created_at = random_past_datetime()
            completed = random.random() < 0.65
            # Ensure completed_at is always after created_at
            if completed:
                days_after_creation = random.randint(1, 60)
                completed_at = created_at + timedelta(days=days_after_creation)
            else:
                completed_at = None

            # Generate human-like task name
            template = random.choice(TASK_TEMPLATES)
            item = random.choice(TASK_ITEMS)
            task_name = template.format(item=item)
            
            # Generate description (sometimes empty)
            description = random.choice(TASK_DESCRIPTIONS)
            
            # Random due date for some tasks
            due_date = None
            if random.random() < 0.4:
                days_ahead = random.randint(1, 90)
                due_date = (created_at + timedelta(days=days_ahead)).date()
            
            # Assign to section if project has sections (70% of tasks)
            section_id = None
            if project_sections and random.random() < 0.7:
                section_id = random.choice(project_sections)

            cur.execute(
                """
                INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    snapshot_id,
                    project_id,
                    section_id,
                    None,
                    task_name,
                    description,
                    assignee,
                    random.choice(CREATED_VIA),
                    None,
                    due_date,
                    completed,
                    created_at,
                    completed_at,
                ),
            )

            tasks.append(task_id)

    conn.commit()
    return tasks
