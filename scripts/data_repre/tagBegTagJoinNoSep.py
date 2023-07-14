#!/usr/bin/env python3

# Converts data from the baseline format to the format with joined tag at the
# beginning, without the separator. 
# J A B L K O # S 4         -> S4 J A B L K O

import sys

srcf = sys.argv[1]
tgtf = sys.argv[2]

sep = " # "

with open(srcf, "r") as src, open(tgtf, "w") as tgt:
    for line in src:
        line = line.strip()
        toks = line.split(sep)
        tag = toks[1]
        lemma = toks[0]

        result = "".join(tag.split(" ")) + " " + lemma
        tgt.write(result + "\n")
