import os

DB_PATH = os.getenv("DB_PATH", "output/asana_simulation.sqlite")

NUM_USERS = int(os.getenv("NUM_USERS", 7500))
NUM_SNAPSHOTS = int(os.getenv("NUM_SNAPSHOTS", 8))

INDUSTRY_WEIGHTS = {
    "Technology": 0.27,
    "Nonprofit": 0.20,
    "Retail": 0.16,
    "Media": 0.11,
    "Finance": 0.05,
    "Education": 0.05,
    "Manufacturing": 0.04,
    "Healthcare": 0.02,
    "Government": 0.01,
    "Other": 0.09
}
