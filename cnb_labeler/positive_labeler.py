from config import CARDWORDS, POSITIVE_LABELS
from .dict_utils import read_dicts, get_token_to_sense

import json
import random
import os
from colorama import Fore
from colorama import Style

def select_sense(senses, dictionary):
    for i, sense in enumerate(senses):
        print("\t", i, dictionary[sense]["word"], dictionary[sense]["definition"])
    
    index = input("Input:")
    index = int(index)
    return senses[index]


def label(cardwords, dictionary, token_to_sense):
    cardword = random.choice(cardwords)
    print(cardword)

    clue = input("CLUE:")
    if len(clue) == 0:
        return None
    
    print("CLUE SENSES")
    clue_sense = select_sense(token_to_sense[clue], dictionary)

    print("CARDWORD SENSES")
    cardword_sense = select_sense(token_to_sense[cardword], dictionary)

    label = int(input("Label [0=Unrelated, 1=Weak, 2=Strong, 3=Related not through text]:"))


    print(f"{Fore.GREEN}{dictionary[clue_sense]['word']}: {dictionary[clue_sense]['definition']}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{dictionary[cardword_sense]['word']}: {dictionary[cardword_sense]['definition']}{Style.RESET_ALL}")

    return {
        "cardword": cardword,
        "cardword_sense": cardword_sense,
        "clue_token": clue,
        "clue_sense": clue_sense,
        "label": label
    }


def main():
    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()

    if os.path.exists(POSITIVE_LABELS):
        with open(POSITIVE_LABELS, "r") as file:
            labels_json = json.loads(file.read())
    else:
        labels_json = []
    
    dictionary = read_dicts()
    token_to_sense = get_token_to_sense(dictionary)

    while(True):
        print(f"===== {len(labels_json)} =====")
        result = label(cardwords, dictionary, token_to_sense)

        if result is None:
            break
            
        labels_json.append(result)
    
        with open(POSITIVE_LABELS, "w+") as file:
            file.write(json.dumps(labels_json, indent=4, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()