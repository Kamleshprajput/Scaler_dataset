from utils.ids import uuid4
from utils.time import random_past_datetime
import random

COMMENT_TEXTS = [
    "Please review this task",
    "This needs to be done ASAP",
    "I have started working on this",
    "Waiting for approval",
    "Blocked due to dependency",
    "This looks good to me",
    "Can we prioritize this?",
    "Assigning this to the relevant team member",
    "Following up on this task",
    "Adding more context here",
]


def generate_user_comments(conn, snapshot_id, tasks, users, max_comments_per_task=3):
    """
    Flat comment model (no parent_comment_id).
    users: list of user_id
    tasks: list of task_id
    """
    if not users or not tasks:
        return  # graceful no-op

    cur = conn.cursor()

    for task_id in tasks:
        if random.random() < 0.6:
            num_comments = random.randint(1, max_comments_per_task)
            for _ in range(num_comments):
                author_id = random.choice(users)

                cur.execute(
                    """
                    INSERT INTO comments
                    (comment_id, snapshot_id, task_id, author_id, body, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        uuid4(),
                        snapshot_id,
                        task_id,
                        author_id,
                        random.choice(COMMENT_TEXTS),
                        random_past_datetime(),
                    ),
                )

    conn.commit()
