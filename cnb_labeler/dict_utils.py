from config import DICTS_DIR

import os
import json
from collections import defaultdict

def read_dicts():
    dictionary = dict()

    for filename in os.listdir(DICTS_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(DICTS_DIR, filename), "r") as file:
                dictionary.update(json.loads(file.read()))
    
    return dictionary


def get_token_to_sense(dictionary):
    token_to_sense = defaultdict(lambda: [])
    for sense_id, entry in dictionary.items():
        for token in entry["tokens"]:
            token_to_sense[token] += [sense_id]
    return token_to_sense