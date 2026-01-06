from utils.ids import uuid4
from utils.time import random_past_datetime
import random

# Common attachment sources
ATTACHMENT_SOURCES = [
    "google_drive",
    "dropbox",
    "box",
    "onedrive",
    "slack",
    "email",
    "asana",
    "figma",
    "github",
    "jira",
]

# Common file types and URLs
FILE_TYPES = [
    ("document", "https://drive.google.com/file/d/{id}/view"),
    ("spreadsheet", "https://docs.google.com/spreadsheets/d/{id}/edit"),
    ("presentation", "https://docs.google.com/presentation/d/{id}/edit"),
    ("image", "https://example.com/files/images/{id}.png"),
    ("pdf", "https://example.com/files/documents/{id}.pdf"),
    ("video", "https://example.com/files/videos/{id}.mp4"),
]

def generate_attachments(conn, snapshot_id, tasks):
    """
    Generate attachments for tasks. About 15-20% of tasks have attachments.
    """
    cur = conn.cursor()
    
    for task_id in tasks:
        # 15-20% of tasks have attachments, with 1-3 attachments per task
        if random.random() < 0.18:
            num_attachments = random.randint(1, 3)
            source = random.choice(ATTACHMENT_SOURCES)
            
            for _ in range(num_attachments):
                attachment_id = uuid4()
                file_type, url_template = random.choice(FILE_TYPES)
                url = url_template.format(id=attachment_id[:8])
                
                cur.execute(
                    "INSERT INTO attachments VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        attachment_id,
                        task_id,
                        snapshot_id,
                        source,
                        url,
                        random_past_datetime(),
                    ),
                )

    conn.commit()


