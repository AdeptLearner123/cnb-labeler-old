from config import CARDWORDS, CLUE_THRESHOLDS

import os
import json

def main():
    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()
    
    if os.path.exists(CLUE_THRESHOLDS):
        with open(CLUE_THRESHOLDS, "r") as file:
            clue_thresholds = json.loads(file.read())
    else:
        clue_thresholds = {}

    missing_cardwords = sorted(list(set(cardwords) - set(clue_thresholds.keys())))
    for i, cardword in enumerate(missing_cardwords):
        print(f"=== {cardword} {i} / {len(missing_cardwords)} ===")
        weak_clue = input("WEAK:")
        strong_clue = input("STRONG:")
        clue_thresholds[cardword] = {
            "weak_clue": weak_clue,
            "strong_clue": strong_clue
        }

        with open(CLUE_THRESHOLDS, "w+") as file:
            file.write(json.dumps(clue_thresholds, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()