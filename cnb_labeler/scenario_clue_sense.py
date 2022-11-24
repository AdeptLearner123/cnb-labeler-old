from config import SCENARIOS
from .dict_utils import read_dicts, get_token_to_sense

import json
from colorama import Fore
from colorama import Style

def select_sense(token, token_to_sense, dictionary):
    print("Select clue sense:")
    senses = token_to_sense[token]
    for i, sense in enumerate(senses):
        print(f"\t [{i}] {dictionary[sense]['word']} : {dictionary[sense]['definition']}")
    idx = input("Index:")
    if len(idx) == 0:
        return None
    return senses[int(idx)]


def set_scenario_clue_senses(scenario, token_to_sense, dictionary):
    clue = scenario["clue"]
    clue_senses = []
    for pos_word in scenario["pos"]:
        print(Fore.GREEN, "POS WORD:", pos_word, Style.RESET_ALL)
        print(Fore.YELLOW, "CLUE:", clue, Style.RESET_ALL)
        clue_senses.append(select_sense(clue, token_to_sense, dictionary))
    scenario["clue_senses"] = clue_senses


def main():
    with open(SCENARIOS, "r") as file:
        scenarios = json.loads(file.read())
    
    unlabeled_idxs = [ i for i, scenario in enumerate(scenarios) if "clue_senses" not in scenario ]
    dictionary = read_dicts()
    token_to_sense = get_token_to_sense(dictionary)

    for i, idx in enumerate(unlabeled_idxs):
        print(f"=== {i}/{len(unlabeled_idxs)} ===")
        set_scenario_clue_senses(scenarios[idx], token_to_sense, dictionary)

        with open(SCENARIOS, "w") as file:
            file.write(json.dumps(scenarios, indent=4))
        
        print(6 * "\n")


if __name__ == "__main__":
    main()