#!/usr/bin/env python3

"""
Read lines from stdin, remove duplicate lines and print to stdout.
That is, for every line print only its first occurrence.
"""

import sys

lines = set()

for line in sys.stdin:
	line = line.strip()
	if line in lines:
		continue
	else:
		print(line)
		lines.add(line)


