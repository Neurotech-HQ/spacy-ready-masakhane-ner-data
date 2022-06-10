import os
import sys
import json


def extract_entities(entities):
    """
    Extract entities from the given entities.
    """
    labels = []
    for entity in entities:
        labels.append(entity["label"])
    return labels


def get_all_available_labels(path):
    """
    Get all available labels in the given path.
    """
    labels = []
    path = os.path.join("spacy-ready-swa", path)
    with open(path) as f:
        data = json.load(f)
        for item in data:
            labels.extend(extract_entities(item["entities"]))
    return list(set(labels))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_all_availble_labels.py <path>")
        sys.exit(1)
    path = sys.argv[1]
    labels = get_all_available_labels(path)
    print(labels)