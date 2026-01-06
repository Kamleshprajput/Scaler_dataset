from utils.ids import uuid4
import random

# Human-like tag names
TAG_NAMES = [
    "urgent",
    "high-priority",
    "bug",
    "feature",
    "enhancement",
    "blocked",
    "in-review",
    "ready-to-deploy",
    "needs-approval",
    "customer-request",
    "technical-debt",
    "documentation",
    "testing",
    "design",
    "backend",
    "frontend",
    "mobile",
    "api",
    "security",
    "performance",
    "qa",
    "staging",
    "production",
    "hotfix",
    "refactor",
]


def create_tags(conn, num_tags=25):
    """
    Create a reusable pool of tags (global, not snapshot-scoped).
    Returns list of tag_ids.
    """
    cur = conn.cursor()

    cur.execute("SELECT tag_id FROM tags")
    existing = [row[0] for row in cur.fetchall()]
    if existing:
        return existing

    tag_ids = []
    for i in range(num_tags):
        tag_id = uuid4()
        name = TAG_NAMES[i % len(TAG_NAMES)]
        tag_ids.append(tag_id)
        cur.execute(
            "INSERT INTO tags VALUES (?, ?)",
            (tag_id, name),
        )

    conn.commit()
    return tag_ids


def assign_task_tags(conn, snapshot_id, tasks, tag_ids, attach_prob=0.4):
    """
    Attach 0–3 tags to each task for a given snapshot.
    Snapshot-safe: clears old snapshot tags before reassigning.
    """
    cur = conn.cursor()

    # 🔑 CRITICAL: clear existing tags for this snapshot
    cur.execute(
        "DELETE FROM task_tags WHERE snapshot_id = ?",
        (snapshot_id,),
    )

    for task_id in tasks:
        if random.random() < attach_prob:
            num = random.randint(1, 3)
            chosen = random.sample(tag_ids, k=min(num, len(tag_ids)))
            for tag_id in chosen:
                cur.execute(
                    "INSERT INTO task_tags VALUES (?, ?, ?)",
                    (task_id, tag_id, snapshot_id),
                )

    conn.commit()
