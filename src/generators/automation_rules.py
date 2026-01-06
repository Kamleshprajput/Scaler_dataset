from utils.ids import uuid4
import random
import json

# Common automation trigger types
TRIGGER_TYPES = [
    "task_created",
    "task_completed",
    "due_date_approaching",
    "custom_field_changed",
    "task_assigned",
    "comment_added",
    "section_changed",
    "project_added",
]

# Common action types
ACTION_TYPES = [
    "assign_task",
    "add_comment",
    "set_due_date",
    "add_tag",
    "move_to_section",
    "update_custom_field",
    "create_subtask",
    "send_notification",
]

# Implementation methods
IMPLEMENTATION_METHODS = [
    "native_rules",
    "api_script",
    "webhook",
    "zapier",
    "make",
    "custom_app",
]

def generate_automation_rules(conn, num_rules=25):
    """
    Generate automation rules that would be used in an organization.
    """
    cur = conn.cursor()
    
    for _ in range(num_rules):
        rule_id = uuid4()
        trigger_type = random.choice(TRIGGER_TYPES)
        action_type = random.choice(ACTION_TYPES)
        implemented_via = random.choice(IMPLEMENTATION_METHODS)
        
        # Create realistic payloads
        trigger_payload = {
            "condition": random.choice(["equals", "contains", "greater_than", "less_than"]),
            "value": random.choice(["urgent", "high", "medium", "low", "blocked"]),
        }
        
        action_payload = {
            "target": random.choice(["assignee", "section", "custom_field", "tag"]),
            "value": random.choice(["Engineering Team", "Review", "P0", "bug"]),
        }
        
        cur.execute(
            "INSERT INTO automation_rules VALUES (?, ?, ?, ?, ?, ?)",
            (
                rule_id,
                trigger_type,
                json.dumps(trigger_payload),
                action_type,
                json.dumps(action_payload),
                implemented_via,
            ),
        )

    conn.commit()


