#!/usr/bin/env python3.9

"""
Reads from stdin and adds a random column (as 1st column) to each row and
prints to stdout. The random number is the same for rows having the same 1st
column before the change. Expects the columns in the input to be separated by
tab "\t".
"""

import sys
import random
from config import SEED
from morfflex.transform_morfflex import raw_lemma_from_lemma

if __name__ == "__main__":
    separator = "\t"
    random.seed(SEED)
    last_rand = random.random()
    last_lemma = ""
    for line in sys.stdin:
        line = line.rstrip()
        lemma = line.split(sep=separator, maxsplit=1)[0]
        if raw_lemma_from_lemma(lemma) != raw_lemma_from_lemma(last_lemma):
            last_lemma = lemma
            last_rand = random.random()
        print(str(last_rand) + separator + line)
