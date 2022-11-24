from config import LABELS_DIR, TRAIN_LABELS, TEST_LABELS
from .dict_utils import read_dicts

import random
import json
import os
import math

TRAIN_TEST_SPLIT = 0.8

def annotate_label(label, dictionary):
    cardword_sense = label["cardword_sense"]
    clue_sense = label["clue_sense"]

    return {
        "word1": dictionary[cardword_sense]["word"],
        "def1": dictionary[cardword_sense]["definition"],
        "word2": dictionary[clue_sense]["word"],
        "def2": dictionary[clue_sense]["definition"],
        "label": label["label"]
    }


def main():
    dictionary = read_dicts()

    labels = []

    for filename in os.listdir(LABELS_DIR):
        with open(os.path.join(LABELS_DIR, filename), "r") as file:
            labels += json.loads(file.read())

    labels = [ label for label in labels if label["label"] != 3 ]    
    annotated_labels = [ annotate_label(label, dictionary) for label in labels ]

    random.shuffle(annotated_labels)

    split_idx = math.floor(TRAIN_TEST_SPLIT * len(annotated_labels))
    train_labels = annotated_labels[:split_idx]
    test_labels = annotated_labels[split_idx:]

    with open(TRAIN_LABELS, "w+") as file:
        file.write(json.dumps(train_labels, indent=4, ensure_ascii=False))

    with open(TEST_LABELS, "w+") as file:
        file.write(json.dumps(test_labels, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()