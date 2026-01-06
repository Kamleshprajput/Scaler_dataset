from datetime import datetime, timedelta
import random

def random_past_datetime(days_back=180):
    now = datetime.utcnow()
    return now - timedelta(days=random.randint(0, days_back),
                           hours=random.randint(0, 23),
                           minutes=random.randint(0, 59))
