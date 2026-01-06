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

# Human-like project names by type
PROJECT_NAMES = {
    "product": [
        "Mobile App Redesign",
        "New Feature Launch",
        "Platform Migration",
        "User Dashboard Update",
        "API v2 Development",
        "Performance Optimization",
        "Security Audit",
        "Product Roadmap Q1",
    ],
    "marketing": [
        "Q1 Campaign Launch",
        "Social Media Strategy",
        "Content Calendar 2024",
        "Brand Refresh Initiative",
        "SEO Optimization",
        "Email Campaign Series",
        "Product Launch Marketing",
        "Customer Acquisition",
    ],
    "it_automation": [
        "CI/CD Pipeline Setup",
        "Infrastructure Automation",
        "Monitoring & Alerts",
        "Backup Automation",
        "Deployment Automation",
        "Security Scanning",
        "Database Migration",
        "Cloud Migration",
    ],
    "operations": [
        "Process Improvement",
        "Vendor Management",
        "Budget Planning",
        "Resource Allocation",
        "Compliance Review",
        "Risk Assessment",
        "Operational Excellence",
        "Team Onboarding",
    ],
    "support": [
        "Customer Support Tickets",
        "Knowledge Base Updates",
        "Support Team Training",
        "Ticket Triage Process",
        "Customer Feedback Review",
        "Support Metrics Dashboard",
        "Escalation Procedures",
        "FAQ Updates",
    ],
    "knowledge": [
        "Documentation Project",
        "Internal Wiki Updates",
        "Training Materials",
        "Best Practices Guide",
        "Onboarding Documentation",
        "Process Documentation",
        "Technical Specifications",
        "Knowledge Sharing Sessions",
    ],
    "ai": [
        "AI Model Training",
        "ML Pipeline Development",
        "Data Collection",
        "Model Evaluation",
        "AI Feature Integration",
        "Predictive Analytics",
        "Recommendation Engine",
        "Natural Language Processing",
    ],
}

INDUSTRIES = [
    "Technology",
    "Nonprofit",
    "Retail",
    "Media",
    "Finance",
    "Education",
    "Manufacturing",
    "Healthcare",
    "Government",
    "Other",
]

def generate_projects(conn, snapshot_id, teams):
    cur = conn.cursor()
    projects = []
    used_names = set()

    for _ in range(len(teams) * 3):
        project_id = uuid4()
        project_type = weighted_choice(PROJECT_TYPES)
        team_id = random.choice(teams)
        
        # Get human-like project name, ensuring uniqueness
        available_names = PROJECT_NAMES.get(project_type, ["Project"])
        project_name = random.choice(available_names)
        
        # Add suffix if name already used to ensure uniqueness
        if project_name in used_names:
            suffix_options = ["2024", "Q1", "Q2", "Q3", "Q4", "Phase 1", "Phase 2", "v2", "Updated"]
            project_name = f"{project_name} - {random.choice(suffix_options)}"
        
        used_names.add(project_name)
        industry = random.choice(INDUSTRIES) if random.random() < 0.7 else None
        
        # Some projects created via integration/automation
        created_via = random.choices(
            ["manual", "integration", "automation"],
            weights=[0.7, 0.2, 0.1],
            k=1
        )[0]
        
        status = random.choices(
            ["active", "on_hold", "completed", "archived"],
            weights=[0.6, 0.1, 0.2, 0.1],
            k=1
        )[0]

        cur.execute(
            """
            INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project_id,
                snapshot_id,
                team_id,
                project_name,
                project_type,
                industry,
                created_via,
                status,
                random_past_datetime(),
            ),
        )
        projects.append(project_id)

    conn.commit()
    return projects
