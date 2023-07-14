#!/usr/bin/env python3

import sys

srcf = sys.argv[1]
tgtf = sys.argv[2]

sep = " # "

with open(srcf, "r") as src, open(tgtf, "w") as tgt:
	for line in src:
		line = line.strip()
		toks = line.split(" ")
#		tags = toks[-3:]
#		rest = toks[:-3]
#		restoks = rest[::-1] + tags

		res = " ".join(toks[::-1])


#		lemma = toks[0]
#		tag = toks[1]
#		tag = "".join(tag.split(" "))
#		res = sep.join([lemma,tag])
		tgt.write(res + "\n")
#		tgt.write(sep.join(toks[::-1]) + "\n")
