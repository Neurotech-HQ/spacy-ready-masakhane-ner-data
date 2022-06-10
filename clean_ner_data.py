import os
import re
import sys
import json
from typing import List

khane_to_spacy_labels = {
    "PER": "PERSON",
    "ORG": "ORG",
    "LOC": "LOC",
    "DATE": "DATE",
}


def load_text_data(filepath):
    sentences = []
    filepath = os.path.join("swa", filepath)
    with open(filepath) as f:
        temp_sentence = []
        for line in f:
            if not line.strip().startswith(". O"):
                temp_sentence.append(line)
                continue
            sentences.append(temp_sentence)
            temp_sentence = []
    return sentences


def get_entities(sentence: List[str]):
    entities = []
    raw_sentence = ""
    for annotated_word in sentence:
        annotated_word = annotated_word.strip()
        if not annotated_word:
            continue
        raw_word, entity = annotated_word.split(" ")
        raw_sentence += f" {raw_word}"
        if entity == "O":
            continue
        entity_type, entity_name = entity.split("-")
        if entity_type == "I":
            entities[-1]["text"] += f" {raw_word}"
        else:
            entities.append(
                {
                    "start": len(raw_sentence) - len(raw_word),
                    "end": len(raw_sentence),
                    "text": raw_word,
                    "label": khane_to_spacy_labels[entity_name],
                }
            )
    return raw_sentence, entities


def convert_to_spacy_format(sentences):
    for sentence in sentences:
        raw_sentence, entities = get_entities(sentence)
        yield raw_sentence, entities


def clean_ner_data(filepath):
    """clean_ner_data

    Steps:
        1. Load data from filepath
        2. Convert to spacy format
        3. Save to filepath in json format

    Args:
        filepath (_type_): _description_
    """
    sentences = load_text_data(filepath)
    ner_data = []
    cleaned_sentences = convert_to_spacy_format(sentences)
    root_name = filepath.split(".")[0]
    new_filename = os.path.join("spacy-ready-swa", f"{root_name}.json")
    if not os.path.exists("spacy-ready-swa"):
        os.mkdir("spacy-ready-swa")

    with open(new_filename, "w") as f:
        for sentence, entities in cleaned_sentences:
            ner_data.append({"text": sentence, "entities": entities})
        json.dump(ner_data, f)


def main():
    """main

    Steps:
        1. Get a list of filepaths in the command line
        2. For each filepath, clean the data

    """

    filepaths = sys.argv[1:]
    if not filepaths:
        filepaths = [
            "train.txt",
            "dev.txt",
            "test.txt",
        ]
    for filepath in filepaths:
        clean_ner_data(filepath)


if __name__ == "__main__":
    main()
