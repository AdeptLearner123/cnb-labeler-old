from config import CARDWORDS, SCENARIOS

import json
import random
import os

NUM_POS = 2
NUM_NEG = 4

def generate_scenario(cardwords):
    sample = random.sample(cardwords, NUM_POS + NUM_NEG)
    pos_words = sample[:NUM_POS]
    neg_words = sample[NUM_POS:]

    print("POS:", ",".join(pos_words))
    print("NEG:", ",".join(neg_words))
    clue = input("CLUE:")

    if len(clue) == 0:
        return None
    return {
        "pos": pos_words,
        "neg": neg_words,
        "clue": clue
    }


def main():
    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()
    
    if os.path.exists(SCENARIOS):
        with open(SCENARIOS, "r") as file:
            scenarios = json.loads(file.read())
    else:
        scenarios = []
    
    while(True):
        print(f"=== {len(scenarios)} ===")
        scenario = generate_scenario(cardwords)
        if scenario is not None:
            scenarios.append(scenario)
        
        with open(SCENARIOS, "w+") as file:
            file.write(json.dumps(scenarios, indent=4))



if __name__ == "__main__":
    main()