from datetime import timedelta
import random

def evolve_tasks(conn, old_snapshot, new_snapshot):
    cur = conn.cursor()

    # Copy tasks forward with controlled evolution
    cur.execute(
        """
        INSERT INTO tasks (
            task_id, snapshot_id, project_id, section_id, parent_task_id,
            name, description, assignee_id, created_via,
            external_source, due_date,
            completed, created_at, completed_at
        )
        SELECT
            task_id,
            ?,
            project_id,
            section_id,
            parent_task_id,
            name,
            description,
            assignee_id,
            created_via,
            external_source,
            due_date,

            -- Completion may change
            CASE
                WHEN completed = 0 AND abs(random()) % 5 = 0 THEN 1
                ELSE completed
            END,

            created_at,

            -- completed_at must always be AFTER created_at
            CASE
                WHEN completed = 0 AND abs(random()) % 5 = 0
                THEN datetime(created_at, '+' || CAST(1 + abs(random()) % 30 AS TEXT) || ' days')
                WHEN completed = 1 AND completed_at IS NOT NULL AND completed_at < created_at
                THEN datetime(created_at, '+' || CAST(1 + abs(random()) % 30 AS TEXT) || ' days')
                ELSE completed_at
            END
        FROM tasks
        WHERE snapshot_id = ?
        """,
        (new_snapshot, old_snapshot),
    )

    conn.commit()
