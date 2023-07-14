#!/usr/bin/env python3.9

"""
Reads from stdin and adds the raw lemma (as 1st column) to each row and
prints to stdout. Expects the columns in the input to be separated by
tab "\t".
"""

import sys
from morfflex.transform_morfflex import raw_lemma_from_lemma

if __name__ == "__main__":
    separator = "\t"

    for line in sys.stdin:
        line = line.rstrip()
        lemma = line.split(sep=separator, maxsplit=1)[0]
        raw = raw_lemma_from_lemma(lemma) 
        print(raw + separator + line)