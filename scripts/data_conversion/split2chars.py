#!/usr/bin/env python3

import sys

for line in sys.stdin:
	line = line.strip()
	res = " ".join(line)
	print(res)
