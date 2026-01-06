from utils.ids import uuid4
import random

def generate_teams(conn, snapshot_id, users):
    cur = conn.cursor()

    teams = []
    for dept in set(u[3] for u in users):
        for _ in range(random.randint(3, 8)):
            team_id = uuid4()
            teams.append(team_id)

            cur.execute(
                "INSERT INTO teams VALUES (?, ?, ?, ?)",
                (team_id, snapshot_id, f"{dept} Team", dept),
            )

    for user_id, _, _, dept, *_ in users:
        if random.random() < 0.85:
            team_id = random.choice(teams)
            cur.execute(
                "INSERT INTO team_memberships VALUES (?, ?, ?, ?)",
                (team_id, user_id, snapshot_id, "member"),
            )

    conn.commit()
