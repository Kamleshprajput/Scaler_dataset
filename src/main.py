import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

from config import DB_PATH, NUM_USERS, NUM_SNAPSHOTS

from utils.ids import uuid4
from utils.time import random_past_datetime

from generators.users import generate_users
from generators.teams import generate_teams
from generators.projects import generate_projects
from generators.sections import generate_sections
from generators.tasks import generate_tasks
from generators.custom_fields import generate_custom_fields
from generators.comments import generate_user_comments
from generators.attachments import generate_attachments
from generators.automation_rules import generate_automation_rules
from generators.api_traces import generate_api_traces
from generators.mcp_calls import generate_mcp_calls
from generators.tags import create_tags, assign_task_tags

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


def seed_snapshots(conn, snapshot_ids):
    """
    Populate organizations and snapshots tables for reporting completeness.
    """
    cur = conn.cursor()
    organization_id = uuid4()
    now = datetime.utcnow()

    cur.execute(
        "INSERT INTO organizations VALUES (?, ?, ?, ?)",
        (organization_id, "Acme Corp", "acme.example.com", now),
    )

    base_time = random_past_datetime(days_back=365)
    for idx, snapshot_id in enumerate(snapshot_ids):
        snapshot_time = base_time + timedelta(days=idx * 7)
        cur.execute(
            "INSERT INTO snapshots VALUES (?, ?, ?, ?, ?)",
            (
                snapshot_id,
                organization_id,
                snapshot_time,
                f"Snapshot {idx}",
                now,
            ),
        )

    conn.commit()


# ----------------------------
# MAIN PIPELINE
# ----------------------------
def main():
    # Ensure output directory exists
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    # Remove existing database if it exists
    db_path = Path(DB_PATH)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    # Apply schema
    init_db(conn)

    # Create snapshot IDs
    snapshot_ids = [uuid4() for _ in range(NUM_SNAPSHOTS)]

    # Seed metadata tables
    seed_snapshots(conn, snapshot_ids)

    # Create tag pool (global)
    tag_ids = create_tags(conn)

    # ======================================================
    # SNAPSHOT 0 — INITIAL SEED
    # ======================================================
    print("> Seeding initial snapshot")

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

    # Sections for projects
    sections = generate_sections(conn, snapshot_ids[0], projects)
    
    # Get section mapping for task assignment
    cur.execute(
        """
        SELECT section_id, project_id FROM sections WHERE snapshot_id = ?
        """,
        (snapshot_ids[0],),
    )
    section_map = {}
    for section_id, project_id in cur.fetchall():
        if project_id not in section_map:
            section_map[project_id] = []
        section_map[project_id].append(section_id)

    # Tasks
    tasks = generate_tasks(conn, snapshot_ids[0], projects, users, section_map)

    # Custom Fields
    generate_custom_fields(conn, snapshot_ids[0], projects, tasks)

    # User comments
    generate_user_comments(conn, snapshot_ids[0], tasks, users)

    # Attachments
    generate_attachments(conn, snapshot_ids[0], tasks)

    # Tags
    assign_task_tags(conn, snapshot_ids[0], tasks, tag_ids)

    # Automation rules (global, not snapshot-specific)
    generate_automation_rules(conn, num_rules=25)

    # API + MCP traces (seed snapshot)
    generate_api_traces(conn, snapshot_ids[0], limit=100)
    generate_mcp_calls(conn, snapshot_ids[0], limit=30)

    # ======================================================
    # SNAPSHOT EVOLUTION
    # ======================================================
    for i in range(1, NUM_SNAPSHOTS):
        print(f"> Evolving snapshot {i}")

        # Task evolution
        evolve_tasks(conn, snapshot_ids[i - 1], snapshot_ids[i])

        # Get tasks for this snapshot
        cur.execute(
            "SELECT task_id FROM tasks WHERE snapshot_id = ?",
            (snapshot_ids[i],),
        )
        snapshot_tasks = [row[0] for row in cur.fetchall()]

        # User comments for evolved snapshot
        generate_user_comments(conn, snapshot_ids[i], snapshot_tasks, users)

        # Attachments for evolved snapshot
        generate_attachments(conn, snapshot_ids[i], snapshot_tasks)

        # Automation artifacts (system comments, SLA reminders)
        apply_automation_artifacts(conn, snapshot_ids[i])

        # API traces for evolved state
        generate_api_traces(conn, snapshot_ids[i], limit=30)

        # Tags for evolved snapshot
        assign_task_tags(conn, snapshot_ids[i], snapshot_tasks, tag_ids)

        # Validate temporal consistency
        validate_temporal_consistency(conn, snapshot_ids[i])

    conn.close()
    print("Simulation complete")


# ----------------------------
# ENTRYPOINT
# ----------------------------
if __name__ == "__main__":
    main()
