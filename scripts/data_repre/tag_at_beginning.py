#!/usr/bin/env python3

import sys

srcf = sys.argv[1]
tgtf = sys.argv[2]

sep = " # "

with open(srcf, "r") as src, open(tgtf, "w") as tgt:
	for line in src:
		line = line.strip()
		toks = line.split(sep)
		tgt.write(sep.join(toks[::-1]) + "\n")
