from config import CARDWORDS, NEGATIVE_LABELS
from .dict_utils import read_dicts, get_token_to_sense

import json
import random

def label(cardwords, dictionary, token_to_sense):
    cardword = random.choice(cardwords)
    cardword_sense = random.choice(token_to_sense[cardword])
    clue_sense, clue_entry = random.choice(list(dictionary.items()))
    clue_token = clue_entry["tokens"][0]

    print(cardword)
    print(dictionary[cardword_sense]["definition"])
    print(clue_token)
    print(dictionary[clue_sense]["definition"])
    label = input("Label [0=Unrelated, 1=Weak, 2=Strong]:")
    
    if len(label) == 0:
        return None

    label = int(label)

    return {
        "cardword": cardword,
        "cardword_sense": cardword_sense,
        "clue_token": clue_token,
        "clue_sense": clue_sense,
        "label": label
    }


def main():
    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()

    with open(NEGATIVE_LABELS, "r") as file:
        labels_json = json.loads(file.read())
    
    dictionary = read_dicts()
    token_to_sense = get_token_to_sense(dictionary)

    while(True):
        result = label(cardwords, dictionary, token_to_sense)

        if result is None:
            break
            
        labels_json.append(result)
    
    with open(NEGATIVE_LABELS, "w+") as file:
        file.write(json.dumps(labels_json, indent=4, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()