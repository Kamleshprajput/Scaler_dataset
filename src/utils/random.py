import random

def weighted_choice(weight_dict: dict):
    keys = list(weight_dict.keys())
    weights = list(weight_dict.values())
    return random.choices(keys, weights=weights, k=1)[0]
