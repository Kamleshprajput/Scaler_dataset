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
    # Use real tag names, cycling if needed
    for i in range(num_tags):
        tag_id = uuid4()
        name = TAG_NAMES[i % len(TAG_NAMES)]
        tag_ids.append(tag_id)
        cur.execute("INSERT INTO tags VALUES (?, ?)", (tag_id, name))

    conn.commit()
    return tag_ids


def assign_task_tags(conn, snapshot_id, tasks, tag_ids, attach_prob=0.4):
    """
    Attach 0-3 tags to each task with a given probability.
    """
    cur = conn.cursor()

    for task_id in tasks:
        if random.random() < attach_prob:
            num = random.randint(1, 3)
            chosen = random.sample(tag_ids, k=min(num, len(tag_ids)))
            for tag_id in chosen:
                cur.execute(
                    "INSERT OR IGNORE INTO task_tags VALUES (?, ?, ?)",
                    (task_id, tag_id, snapshot_id),
                )

    conn.commit()

