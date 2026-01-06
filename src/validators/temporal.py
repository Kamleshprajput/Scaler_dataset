def validate_temporal_consistency(conn, snapshot_id):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT task_id, created_at, completed_at
        FROM tasks
        WHERE snapshot_id = ?
        AND completed = 1
        AND completed_at < created_at
        LIMIT 5
        """,
        (snapshot_id,),
    )

    rows = cur.fetchall()
    if rows:
        print("❌ Temporal violations detected:")
        for r in rows:
            print(r)
        raise ValueError("Temporal validation failed")
