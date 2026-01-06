import os

DB_PATH = os.getenv("DB_PATH", "output/asana_simulation.sqlite")

NUM_USERS = int(os.getenv("NUM_USERS", 7500))
NUM_SNAPSHOTS = int(os.getenv("NUM_SNAPSHOTS", 8))

# Industry weights based on companiesnumber.txt (161 total companies)
# Ratios: Technology(43), Nonprofit(33), Retail(25), Media(17), Education(6), 
# Finance(6), Food(6), Marketing(6), Manufacturing(5), Healthcare(3), 
# Telecom(3), Automotive(2), Energy(2), Government(2), Travel(2)
INDUSTRY_WEIGHTS = {
    "Technology": 43/161,  # 0.267
    "Nonprofit": 33/161,   # 0.205
    "Retail and consumer": 25/161,  # 0.155
    "Media and entertainment": 17/161,  # 0.106
    "Education": 6/161,    # 0.037
    "Finance": 6/161,      # 0.037
    "Food and Hospitality": 6/161,  # 0.037
    "Marketing and Creative service": 6/161,  # 0.037
    "Manufacturing": 5/161,  # 0.031
    "Healthcare": 3/161,   # 0.019
    "Telecommunications": 3/161,  # 0.019
    "Automotive": 2/161,   # 0.012
    "Energy": 2/161,       # 0.012
    "Government": 2/161,   # 0.012
    "Travel and transport": 2/161,  # 0.012
}
