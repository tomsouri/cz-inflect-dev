#!/usr/bin/env python3

"""
IMPLEMENTS EXTRACTING THE IMPORTANT PARTS FROM THE CSV FILES FROM CESTINA 2.0.
"""

import csv
import re
from collections import namedtuple
from config import CESTINA20FILES

# defines in which column in the input csv file there is the lemma and the
# description
__DEFAULT_COLUMN_DICT = {"lemma": 5, "description": 4}


def __split_description(description):
    """
    Split the given description to main description, other description and
    example of usage.
    """
    find_example = re.search("(?<=\\<em>)(.)*(?=\\<\\/em>)", description)

    example = find_example.group() if find_example else ""

    description = re.sub("(\\<em>)(.)*(\\<\\/em>)", "", description)
    description = re.sub("\n", " ", description)
    description = re.sub("\r", "", description)
    descriptions = re.split(";", description, maxsplit=1)

    main_description = descriptions[0]
    other_description = descriptions[1] if len(descriptions) > 1 else ""
    # if len(descriptions) > 1: other_description = descriptions[1] else:
    #    other_description = ""

    return main_description, other_description, example


Lemma = namedtuple(
    "Lemma", ("lemma", "main_description", "other_description", "example")
)


def __parse_row(row: str) -> Lemma:
    """
    Gets a row and creates a corresponding instance of Lemma and returns it.
    """

    lemma = row[__DEFAULT_COLUMN_DICT["lemma"]]
    description = row[__DEFAULT_COLUMN_DICT["description"]]

    main_description, other_description, example = __split_description(
        description
    )

    return Lemma(lemma, main_description, other_description, example)


def __get_lemmata_from_single_file(filename):
    """
    Reads csv file from given file and extracts columns regarding to
    __DEFAULT_COLUMN_DICT.
    """
    with open(filename, "r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            yield __parse_row(row)


def get_lemmata():
    for filename in CESTINA20FILES:
        for lemma in __get_lemmata_from_single_file(filename):
            yield lemma
