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
    schema_path = Path(__file__).resolve().parent.parent / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def seed_snapshots(conn, snapshot_ids):
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
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    db_path = Path(DB_PATH)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    init_db(conn)

    snapshot_ids = [uuid4() for _ in range(NUM_SNAPSHOTS)]
    seed_snapshots(conn, snapshot_ids)

    # Global tag pool
    tag_ids = create_tags(conn)

    # ======================================================
    # SNAPSHOT 0 — INITIAL SEED
    # ======================================================
    print("> Seeding initial snapshot")

    generate_users(conn, snapshot_ids[0], NUM_USERS)

    cur = conn.cursor()
    cur.execute(
        "SELECT user_id FROM users WHERE snapshot_id = ?",
        (snapshot_ids[0],),
    )
    users = [r[0] for r in cur.fetchall()]

    generate_teams(conn, snapshot_ids[0], users)

    cur.execute(
        "SELECT team_id FROM teams WHERE snapshot_id = ?",
        (snapshot_ids[0],),
    )
    teams = [r[0] for r in cur.fetchall()]

    projects = generate_projects(conn, snapshot_ids[0], teams)
    sections = generate_sections(conn, snapshot_ids[0], projects)

    cur.execute(
        "SELECT section_id, project_id FROM sections WHERE snapshot_id = ?",
        (snapshot_ids[0],),
    )
    section_map = {}
    for section_id, project_id in cur.fetchall():
        section_map.setdefault(project_id, []).append(section_id)

    tasks = generate_tasks(conn, snapshot_ids[0], projects, users, section_map)

    generate_custom_fields(conn, snapshot_ids[0], projects, tasks)
    generate_user_comments(conn, snapshot_ids[0], tasks, users)
    generate_attachments(conn, snapshot_ids[0], tasks)

    assign_task_tags(conn, snapshot_ids[0], tasks, tag_ids)

    generate_automation_rules(conn, num_rules=25)
    generate_api_traces(conn, snapshot_ids[0], limit=100)
    generate_mcp_calls(conn, snapshot_ids[0], limit=30)

    # ======================================================
    # SNAPSHOT EVOLUTION
    # ======================================================
    for i in range(1, NUM_SNAPSHOTS):
        print(f"> Evolving snapshot {i}")

        evolve_tasks(conn, snapshot_ids[i - 1], snapshot_ids[i])
        conn.commit()  # 🔑 ensure durability before downstream writes

        cur.execute(
            "SELECT task_id FROM tasks WHERE snapshot_id = ?",
            (snapshot_ids[i],),
        )
        snapshot_tasks = [r[0] for r in cur.fetchall()]

        cur.execute(
            "SELECT user_id FROM users WHERE snapshot_id = ?",
            (snapshot_ids[i],),
        )
        snapshot_users = [r[0] for r in cur.fetchall()]

        generate_user_comments(conn, snapshot_ids[i], snapshot_tasks, snapshot_users)
        generate_attachments(conn, snapshot_ids[i], snapshot_tasks)
        apply_automation_artifacts(conn, snapshot_ids[i])
        assign_task_tags(conn, snapshot_ids[i], snapshot_tasks, tag_ids)
        generate_api_traces(conn, snapshot_ids[i], limit=30)

        validate_temporal_consistency(conn, snapshot_ids[i])

    conn.close()
    print("Simulation complete")


if __name__ == "__main__":
    main()
