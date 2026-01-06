from faker import Faker
from utils.ids import uuid4
from utils.random import weighted_choice

fake = Faker()

DEPARTMENT_WEIGHTS = {
    "Engineering": 0.35,
    "Marketing": 0.18,
    "Operations": 0.20,
    "IT": 0.15,
    "Support": 0.12,
}

ROLE_WEIGHTS = {
    "ic": 0.72,
    "manager": 0.18,
    "admin": 0.03,
    "service": 0.07,
}

def generate_users(conn, snapshot_id, num_users):
    cur = conn.cursor()

    for _ in range(num_users):
        user_id = uuid4()
        department = weighted_choice(DEPARTMENT_WEIGHTS)
        role = weighted_choice(ROLE_WEIGHTS)
        is_active = False if fake.random_int(0, 100) < 15 else True

        cur.execute(
            """
            INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                snapshot_id,
                fake.name(),
                fake.email(),
                department,
                role,
                is_active,
            ),
        )

    conn.commit()
