from utils.ids import uuid4
import random

TEAM_SUFFIXES = [
    "Team",
    "Squad",
    "Group",
    "Unit",
    "Pod",
    "Crew",
]

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
    """
    users: list of user_id (NOT tuples)
    """
    cur = conn.cursor()

    # --------------------------------
    # Fetch user → department mapping
    # --------------------------------
    cur.execute(
        """
        SELECT user_id, department
        FROM users
        WHERE snapshot_id = ?
        """,
        (snapshot_id,),
    )

    user_dept = {user_id: dept for user_id, dept in cur.fetchall()}

    # --------------------------------
    # Create teams per department
    # --------------------------------
    teams_by_dept = {}
    all_teams = []

    for dept in set(user_dept.values()):
        teams_by_dept[dept] = []
        num_teams = random.randint(3, 8)

        dept_team_names = TEAM_NAMES_BY_DEPT.get(
            dept, [f"{dept} {suffix}" for suffix in TEAM_SUFFIXES]
        )

        for i in range(num_teams):
            team_id = uuid4()
            teams_by_dept[dept].append(team_id)
            all_teams.append(team_id)

            if i < len(dept_team_names):
                team_name = dept_team_names[i]
            else:
                team_name = f"{dept} {random.choice(TEAM_SUFFIXES)} {i+1}"

            cur.execute(
                """
                INSERT INTO teams (team_id, snapshot_id, name, department)
                VALUES (?, ?, ?, ?)
                """,
                (team_id, snapshot_id, team_name, dept),
            )

    # --------------------------------
    # Assign users to teams (UNIQUE)
    # --------------------------------
    role_choices = ["member", "admin", "viewer"]
    role_weights = [0.8, 0.15, 0.05]

    assigned = set()  # (team_id, user_id)

    for user_id, dept in user_dept.items():
        if random.random() < 0.85:
            team_id = random.choice(teams_by_dept[dept])
            key = (team_id, user_id)

            if key in assigned:
                continue

            assigned.add(key)
            role = random.choices(role_choices, weights=role_weights, k=1)[0]

            cur.execute(
                """
                INSERT INTO team_memberships
                (team_id, user_id, snapshot_id, role)
                VALUES (?, ?, ?, ?)
                """,
                (team_id, user_id, snapshot_id, role),
            )

    conn.commit()
    return all_teams
