import sqlite3
from pathlib import Path

from config import DB_PATH, NUM_USERS, NUM_SNAPSHOTS

from utils.ids import uuid4

from generators.users import generate_users
from generators.teams import generate_teams
from generators.projects import generate_projects
from generators.tasks import generate_tasks
from generators.custom_fields import generate_custom_fields
from generators.api_traces import generate_api_traces
from generators.mcp_calls import generate_mcp_calls

from evolvers.task_evolver import evolve_tasks
from evolvers.automation_evolver import apply_automation_artifacts

from validators.temporal import validate_temporal_consistency


# ----------------------------
# DB INITIALIZATION
# ----------------------------
def init_db(conn):
    """
    Apply schema.sql to the database.
    """
    schema_path = Path(__file__).resolve().parent.parent / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


# ----------------------------
# MAIN PIPELINE
# ----------------------------
def main():
    # Ensure output directory exists
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    # Apply schema
    init_db(conn)

    # Create snapshot IDs
    snapshot_ids = [uuid4() for _ in range(NUM_SNAPSHOTS)]

    # ======================================================
    # SNAPSHOT 0 — INITIAL SEED
    # ======================================================
    print("▶ Seeding initial snapshot")

    # Users
    generate_users(conn, snapshot_ids[0], NUM_USERS)

    cur = conn.cursor()
    cur.execute(
        """
        SELECT user_id, snapshot_id, name, department
        FROM users
        WHERE snapshot_id = ?
        """,
        (snapshot_ids[0],),
    )
    users = cur.fetchall()

    # Teams
    generate_teams(conn, snapshot_ids[0], users)

    cur.execute(
        """
        SELECT team_id
        FROM teams
        WHERE snapshot_id = ?
        """,
        (snapshot_ids[0],),
    )
    teams = [row[0] for row in cur.fetchall()]

    # Projects
    projects = generate_projects(conn, snapshot_ids[0], teams)

    # Tasks
    tasks = generate_tasks(conn, snapshot_ids[0], projects, users)

    # Custom Fields
    generate_custom_fields(conn, snapshot_ids[0], projects, tasks)

    # API + MCP traces (seed snapshot)
    generate_api_traces(conn, snapshot_ids[0], limit=100)
    generate_mcp_calls(conn, snapshot_ids[0], limit=30)

    # ======================================================
    # SNAPSHOT EVOLUTION
    # ======================================================
    for i in range(1, NUM_SNAPSHOTS):
        print(f"▶ Evolving snapshot {i}")

        # Task evolution
        evolve_tasks(conn, snapshot_ids[i - 1], snapshot_ids[i])

        # Automation artifacts (system comments, SLA reminders)
        apply_automation_artifacts(conn, snapshot_ids[i])

        # API traces for evolved state
        generate_api_traces(conn, snapshot_ids[i], limit=30)

        # Validate temporal consistency
        validate_temporal_consistency(conn, snapshot_ids[i])

    conn.close()
    print("✅ Simulation complete")


# ----------------------------
# ENTRYPOINT
# ----------------------------
if __name__ == "__main__":
    main()
