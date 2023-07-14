#!/usr/bin/env python3

import os
from config import MORFFLEX_RAW, MORFFLEX_LEMMATA, MORFFLEX_COLUMN_SEPARATOR

from morfflex.transform_morfflex import raw_lemma_from_lemma

def build_lemmata_only():
    if not os.path.exists(MORFFLEX_RAW):
        raise Exception("Morfflex file does not exist.")

    last_word = ""
    with open(MORFFLEX_RAW, "r") as src, open(MORFFLEX_LEMMATA, "w") as tgt:
        for line in src:
            word = line.split(MORFFLEX_COLUMN_SEPARATOR)[0]
            if word != last_word:
                last_word = word
                word = raw_lemma_from_lemma(word)
                if word != "":
                    tgt.write(word + "\n")

if __name__ == "__main__":
    build_lemmata_only()