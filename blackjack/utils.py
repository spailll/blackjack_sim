# blackjack/utils.py

import yaml
import random

def load_settings(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def set_random_seed(seed_val):
    random.seed(seed_val)