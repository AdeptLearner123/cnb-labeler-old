from config import SCENARIOS
from .dict_utils import read_dicts, get_token_to_sense

import json
from colorama import Fore, Style

RELATION_COLORS = [ Fore.WHITE, Fore.GREEN, Fore.YELLOW, Fore.CYAN ]


def get_sense_relations(clue, clue_sense, token, token_to_sense, dictionary):
    senses = token_to_sense[token]
    sense_relations = { sense:0 for sense in senses }
    while(True):
        print(sense_relations)
        print(Fore.GREEN, "TOKEN:", token, Style.RESET_ALL)
        print(Fore.YELLOW, "CLUE:", clue, dictionary[clue_sense]['definition'], Style.RESET_ALL)
        print("Senses:")
        for i, sense in enumerate(senses):
            relation = sense_relations[sense]
            print(RELATION_COLORS[relation], f"\t [{i}] {dictionary[sense]['word']} : {dictionary[sense]['definition']}", Style.RESET_ALL)
        input_text = input("Input [0 = Unrelated, 1 = Related, 2 = Unsure, 3 = Related but not through text]:")

        if len(input_text) == 0:
            return sense_relations
        elif " " in input_text:
            idx, relation = input_text.split(" ")
            idx = int(idx)
            relation = int(relation)
        else:
            idx = int(input_text)
            relation = 1
        sense_relations[senses[idx]] = relation
        
        print("\n" * 6)


def set_scenario_cardword_senses(scenario, token_to_sense, dictionary):
    cardword_senses = dict()
    for i, word in enumerate(scenario["pos"]):
        clue_sense = scenario["clue_senses"][i]
        
        if clue_sense is None:
            continue

        cardword_senses[word] = get_sense_relations(scenario["clue"], clue_sense, word, token_to_sense, dictionary)
    for word in scenario["neg"]:
        clue_sense = scenario["clue_senses"][0]

        if clue_sense is None:
            continue

        cardword_senses[word] = get_sense_relations(scenario["clue"], clue_sense, word, token_to_sense, dictionary)
    scenario["cardword_senses"] = cardword_senses



def main():
    with open(SCENARIOS, "r") as file:
        scenarios = json.loads(file.read())
    
    unlabeled_idxs = [ i for i, scenario in enumerate(scenarios) if "clue_senses" in scenario and "cardword_senses" not in scenario ]
    dictionary = read_dicts()
    token_to_sense = get_token_to_sense(dictionary)

    for i, idx in enumerate(unlabeled_idxs):
        print(f"=== {i}/{len(unlabeled_idxs)} ===")
        print(idx)
        set_scenario_cardword_senses(scenarios[idx], token_to_sense, dictionary)

        with open(SCENARIOS, "w") as file:
            file.write(json.dumps(scenarios, indent=4))


if __name__ == "__main__":
    main()