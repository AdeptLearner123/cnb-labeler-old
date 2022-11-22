from config import CARDWORDS, SCENARIO_LABELS
from .dict_utils import read_dicts, get_token_to_sense

import json
import random
import os

POS_SAMPLES = 2
NEG_SAMPLES = 6

def select_sense(senses, dictionary):
    print("SENSES:")
    for i, sense in enumerate(senses):
        print("\t", i, sense, dictionary[sense]["definition"])
    
    index = input("Input:")
    index = int(index)
    return senses[index]



def label(cardwords, dictionary, token_to_sense):
    sample_cardwords = random.sample(cardwords, POS_SAMPLES + NEG_SAMPLES)
    pos_cardwords = sample_cardwords[:POS_SAMPLES]
    neg_cardwords = sample_cardwords[POS_SAMPLES:]

    print(f"POS:", ", ".join(pos_cardwords))
    print(f"NEG:", ", ".join(neg_cardwords))
    print("CLUE:")

    clue = input()
    if len(clue) == 0:
        return None

    if clue == "s":
        return clue

    clue_senses = token_to_sense[clue]
    if len(clue_senses) == 0:
        return None
    
    clue_sense = select_sense(clue_senses, dictionary)
    
    pos_senses = {}
    for cardword in pos_cardwords:
        print("POS WORD:", cardword)
        pos_sense = select_sense(token_to_sense[cardword], dictionary)
        pos_senses[pos_sense] = int(input("STRENGTH:"))
    
    neg_senses = {}
    for cardword in neg_cardwords:
        print("NEG WORD:", cardword)
        neg_sense = select_sense(token_to_sense[cardword], dictionary)
        neg_senses[neg_sense] = int(input("STRENGTH:"))

    return {
        "clue": clue,
        "clue_sense": clue_sense,
        "pos_cardwords": pos_cardwords,
        "pos_senses": pos_senses,
        "neg_cardwords": neg_cardwords,
        "neg_senses": neg_senses
    }




def main():
    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()

    if os.path.exists(SCENARIO_LABELS):
        with open(SCENARIO_LABELS, "r") as file:
            labels_json = json.loads(file.read())
    else:
        labels_json = []
    
    dictionary = read_dicts()
    token_to_sense = get_token_to_sense(dictionary)

    while(True):
        result = label(cardwords, dictionary, token_to_sense)

        if result is None:
            break
        
        if result == "s":
            continue

        labels_json.append(result)
    
    with open(POSITIVE_LABELS, "w+") as file:
        file.write(json.dumps(labels_json, indent=4, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()