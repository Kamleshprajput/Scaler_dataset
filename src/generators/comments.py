from utils.ids import uuid4
from utils.time import random_past_datetime
import random

# Human-like comment messages
USER_COMMENTS = [
    "Working on this now",
    "Blocked waiting on API response",
    "This looks good, ready for review",
    "Need more information before proceeding",
    "Can someone help with this?",
    "Almost done, should be finished by EOD",
    "Found an issue, investigating",
    "This is complete and ready for testing",
    "Waiting for approval from stakeholders",
    "Updated the requirements, please review",
    "Moving this to next sprint",
    "This is a duplicate of another task",
    "Great progress! Keep it up",
    "Let's discuss this in the next standup",
    "I've added more details in the description",
    "This is ready for deployment",
    "Need clarification on the acceptance criteria",
    "Completed! Moving to done",
    "This is taking longer than expected",
    "Can we prioritize this?",
    "Thanks for the update!",
    "I'll take a look at this",
    "This is blocked by another task",
    "Let me know if you need any help",
    "Following up on this",
]

def generate_user_comments(conn, snapshot_id, tasks, users):
    """
    Generate user comments on tasks. About 10-15% of tasks have user comments.
    """
    cur = conn.cursor()
    
    for task_id in tasks:
        # 10-15% of tasks have user comments, with 1-4 comments per task
        if random.random() < 0.12:
            num_comments = random.randint(1, 4)
            
            for _ in range(num_comments):
                comment_id = uuid4()
                author = random.choice(users)[0]  # User who created the comment
                comment_text = random.choice(USER_COMMENTS)
                
                cur.execute(
                    """
                    INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        comment_id,
                        snapshot_id,
                        task_id,
                        author,
                        "user",
                        comment_text,
                        random_past_datetime(),
                    ),
                )

    conn.commit()

