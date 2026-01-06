from utils.ids import uuid4
import random

# Human-like team name suffixes
TEAM_SUFFIXES = [
    "Team",
    "Squad",
    "Group",
    "Unit",
    "Pod",
    "Crew",
]

# Specialized team names by department
TEAM_NAMES_BY_DEPT = {
    "Engineering": [
        "Platform",
        "Backend",
        "Frontend",
        "Mobile",
        "DevOps",
        "QA",
        "Infrastructure",
        "Security",
    ],
    "Marketing": [
        "Content",
        "Social Media",
        "Brand",
        "Growth",
        "Product Marketing",
        "Digital",
        "Events",
        "Communications",
    ],
    "Operations": [
        "Business Operations",
        "People Ops",
        "Finance",
        "Legal",
        "Facilities",
        "Procurement",
        "Vendor Management",
    ],
    "IT": [
        "IT Support",
        "Systems",
        "Network",
        "Help Desk",
        "Infrastructure",
        "Security",
    ],
    "Support": [
        "Customer Success",
        "Technical Support",
        "Account Management",
        "Customer Care",
    ],
}

def generate_teams(conn, snapshot_id, users):
    cur = conn.cursor()

    teams = []
    for dept in set(u[3] for u in users):
        num_teams = random.randint(3, 8)
        
        # Get department-specific team names or use generic ones
        dept_teams = TEAM_NAMES_BY_DEPT.get(dept, [f"{dept} {suffix}" for suffix in TEAM_SUFFIXES])
        
        for i in range(num_teams):
            team_id = uuid4()
            teams.append(team_id)
            
            # Use department-specific name or create one
            if i < len(dept_teams):
                team_name = dept_teams[i]
            else:
                suffix = random.choice(TEAM_SUFFIXES)
                team_name = f"{dept} {suffix} {i+1}"

            cur.execute(
                "INSERT INTO teams VALUES (?, ?, ?, ?)",
                (team_id, snapshot_id, team_name, dept),
            )

    role_choices = ["member", "admin", "viewer"]
    role_weights = [0.8, 0.15, 0.05]

    for user_id, _, _, dept, *_ in users:
        if random.random() < 0.85:
            team_id = random.choice(teams)
            role = random.choices(role_choices, weights=role_weights, k=1)[0]
            cur.execute(
                "INSERT INTO team_memberships VALUES (?, ?, ?, ?)",
                (team_id, user_id, snapshot_id, role),
            )

    conn.commit()
