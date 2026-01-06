from utils.ids import uuid4
from utils.random import weighted_choice
from utils.time import random_past_datetime
from config import INDUSTRY_WEIGHTS
import random

# Expanded project types based on reference files
PROJECT_TYPES = {
    "product": 0.25,
    "marketing": 0.15,
    "it_automation": 0.12,
    "operations": 0.12,
    "support": 0.08,
    "knowledge": 0.07,
    "ai": 0.04,
    "program_management": 0.06,
    "work_requests": 0.05,
    "goal_tracking": 0.04,
    "campaign_management": 0.02,
}

# Industry-specific project names based on companiesnumber.txt workflows
INDUSTRY_PROJECTS = {
    "Technology": {
        "product": [
            "Product Launch Q1", "API Development", "Platform Migration", 
            "Feature Development", "Bug Tracking System", "Sprint Planning",
            "Product Roadmap", "Technical Debt Reduction", "Performance Optimization"
        ],
        "program_management": [
            "Program Management Dashboard", "Cross-team Coordination", 
            "Release Planning", "Technical Program Management"
        ],
        "work_requests": [
            "IT Request Portal", "Engineering Requests", "Infrastructure Requests",
            "DevOps Work Requests"
        ],
        "campaign_management": [
            "Product Launch Campaign", "Feature Announcement Campaign"
        ],
    },
    "Nonprofit": {
        "campaign_management": [
            "Fundraising Campaign", "Awareness Campaign", "Donor Campaign",
            "Volunteer Recruitment Campaign", "Annual Campaign"
        ],
        "program_management": [
            "Program Management", "Community Programs", "Outreach Programs",
            "Grant Management"
        ],
        "work_requests": [
            "Volunteer Requests", "Resource Requests", "Event Requests"
        ],
        "goal_tracking": [
            "Goal Tracking & OKRs", "Impact Measurement", "Strategic Goals"
        ],
    },
    "Retail and consumer": {
        "campaign_management": [
            "Marketing Campaign", "Product Launch Campaign", "Seasonal Campaign",
            "Promotional Campaign", "Social Media Campaign"
        ],
        "product": [
            "Product Launch", "Product Development", "Inventory Management",
            "Supply Chain Management"
        ],
        "marketing": [
            "Brand Campaign", "Customer Acquisition", "Retail Marketing"
        ],
    },
    "Media and entertainment": {
        "campaign_management": [
            "Creative Campaign", "Content Campaign", "Editorial Calendar",
            "Social Media Calendar", "Publishing Campaign"
        ],
        "product": [
            "Content Production", "Creative Production", "Media Production",
            "Video Production"
        ],
        "work_requests": [
            "Content Requests", "Creative Requests", "Editorial Requests"
        ],
    },
    "Education": {
        "goal_tracking": [
            "Goal Tracking & OKRs", "Student Outcomes", "Academic Goals",
            "Annual Planning"
        ],
        "program_management": [
            "Curriculum Development", "Program Management", "Academic Programs"
        ],
        "work_requests": [
            "IT Requests", "Facilities Requests", "Resource Requests"
        ],
    },
    "Finance": {
        "program_management": [
            "Program Management", "Compliance Programs", "Risk Management",
            "Financial Planning"
        ],
        "work_requests": [
            "IT Requests", "Compliance Requests", "Audit Requests"
        ],
        "product": [
            "Product Launches", "Financial Product Development", "Compliance Projects"
        ],
    },
    "Food and Hospitality": {
        "product": [
            "Product Development", "Menu Planning", "Recipe Development"
        ],
        "program_management": [
            "Program Management", "Software Deployments", "Operations Management"
        ],
        "campaign_management": [
            "Marketing Campaign", "Promotional Campaign", "Event Campaign"
        ],
    },
    "Marketing and Creative service": {
        "campaign_management": [
            "Creative Campaign", "Client Campaign", "Brand Campaign"
        ],
        "product": [
            "Creative Production", "Client Projects", "Design Projects"
        ],
        "work_requests": [
            "Creative Requests", "Client Requests", "Design Requests"
        ],
    },
    "Manufacturing": {
        "goal_tracking": [
            "Goal Tracking & OKRs", "Production Goals", "Quality Goals"
        ],
        "product": [
            "Product Development", "Product Roadmaps", "Manufacturing Projects"
        ],
        "program_management": [
            "Program Management", "Production Programs", "Quality Programs"
        ],
        "work_requests": [
            "IT Requests", "Maintenance Requests", "Supply Chain Requests"
        ],
    },
    "Healthcare": {
        "campaign_management": [
            "Health Campaign", "Awareness Campaign", "Patient Campaign"
        ],
        "program_management": [
            "Program Management", "Patient Care Programs", "Clinical Programs"
        ],
        "work_requests": [
            "IT Requests", "Facilities Requests", "Clinical Requests"
        ],
    },
    "Telecommunications": {
        "campaign_management": [
            "Marketing Campaign", "Customer Campaign", "Product Campaign"
        ],
        "work_requests": [
            "IT Requests", "Network Requests", "Infrastructure Requests"
        ],
    },
    "Automotive": {
        "product": [
            "Product Launches", "Vehicle Development", "Component Development"
        ],
        "goal_tracking": [
            "Goal Tracking & OKRs", "Production Goals", "Quality Goals"
        ],
    },
    "Energy": {
        "program_management": [
            "Program Management", "Energy Programs", "Infrastructure Programs"
        ],
        "work_requests": [
            "Work Requests", "Maintenance Requests", "Safety Requests"
        ],
    },
    "Government": {
        "program_management": [
            "Program Management", "Public Programs", "Policy Programs"
        ],
        "work_requests": [
            "Work Requests", "Service Requests", "Compliance Requests"
        ],
    },
    "Travel and transport": {
        "program_management": [
            "Program Management", "Route Planning", "Operations Management"
        ],
        "work_requests": [
            "Work Requests", "Maintenance Requests", "Scheduling Requests"
        ],
    },
}

# Generic project names by type (fallback)
GENERIC_PROJECT_NAMES = {
    "product": [
        "Mobile App Redesign", "New Feature Launch", "Platform Migration",
        "User Dashboard Update", "API v2 Development", "Performance Optimization",
        "Security Audit", "Product Roadmap Q1",
    ],
    "marketing": [
        "Q1 Campaign Launch", "Social Media Strategy", "Content Calendar 2024",
        "Brand Refresh Initiative", "SEO Optimization", "Email Campaign Series",
        "Product Launch Marketing", "Customer Acquisition",
    ],
    "it_automation": [
        "CI/CD Pipeline Setup", "Infrastructure Automation", "Monitoring & Alerts",
        "Backup Automation", "Deployment Automation", "Security Scanning",
        "Database Migration", "Cloud Migration",
    ],
    "operations": [
        "Process Improvement", "Vendor Management", "Budget Planning",
        "Resource Allocation", "Compliance Review", "Risk Assessment",
        "Operational Excellence", "Team Onboarding",
    ],
    "support": [
        "Customer Support Tickets", "Knowledge Base Updates", "Support Team Training",
        "Ticket Triage Process", "Customer Feedback Review", "Support Metrics Dashboard",
        "Escalation Procedures", "FAQ Updates",
    ],
    "knowledge": [
        "Documentation Project", "Internal Wiki Updates", "Training Materials",
        "Best Practices Guide", "Onboarding Documentation", "Process Documentation",
        "Technical Specifications", "Knowledge Sharing Sessions",
    ],
    "ai": [
        "AI Model Training", "ML Pipeline Development", "Data Collection",
        "Model Evaluation", "AI Feature Integration", "Predictive Analytics",
        "Recommendation Engine", "Natural Language Processing",
    ],
    "program_management": [
        "Program Management Dashboard", "Cross-team Coordination", "Release Planning",
        "Strategic Planning", "Portfolio Management",
    ],
    "work_requests": [
        "Work Request Portal", "IT Request System", "Service Request Management",
        "Request Triage Process", "Request Fulfillment",
    ],
    "goal_tracking": [
        "Goal Tracking & OKRs", "Annual Planning", "Strategic Goals",
        "Quarterly Objectives", "Performance Goals",
    ],
    "campaign_management": [
        "Marketing Campaign", "Product Campaign", "Brand Campaign",
        "Digital Campaign", "Multi-channel Campaign",
    ],
}

def generate_projects(conn, snapshot_id, teams):
    cur = conn.cursor()
    projects = []
    used_names = set()

    # Generate projects based on industry distribution
    num_projects = len(teams) * 3
    
    for _ in range(num_projects):
        project_id = uuid4()
        project_type = weighted_choice(PROJECT_TYPES)
        team_id = random.choice(teams)
        
        # Select industry based on weights from config (all projects get an industry)
        industry = weighted_choice(INDUSTRY_WEIGHTS)
        
        # Get industry-specific project name or fallback to generic
        project_name = None
        if industry in INDUSTRY_PROJECTS and project_type in INDUSTRY_PROJECTS[industry]:
            available_names = INDUSTRY_PROJECTS[industry][project_type]
            project_name = random.choice(available_names)
        else:
            # Fallback to generic names
            available_names = GENERIC_PROJECT_NAMES.get(project_type, ["Project"])
            project_name = random.choice(available_names)
        
        # Add suffix if name already used to ensure uniqueness
        if project_name in used_names:
            suffix_options = ["2024", "Q1", "Q2", "Q3", "Q4", "Phase 1", "Phase 2", "v2", "Updated", "H2"]
            project_name = f"{project_name} - {random.choice(suffix_options)}"
        
        used_names.add(project_name)
        
        # Some projects created via integration/automation (based on reference files)
        created_via = random.choices(
            ["manual", "integration", "automation"],
            weights=[0.65, 0.25, 0.10],  # More integration based on reference
            k=1
        )[0]
        
        # Project status distribution
        status = random.choices(
            ["active", "on_hold", "completed", "archived"],
            weights=[0.60, 0.10, 0.25, 0.05],
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
