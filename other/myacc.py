#!/usr/bin/env python3

import sys

inp = sys.argv[1]
out = sys.argv[2]

all = 0
corr= 0

with open(inp,"r") as ifile, open(out,"r") as ofile:
        while(True):
                line1 = ifile.readline().strip()
                line2 = ofile.readline().strip()

                if not line1 or not line2:
                # If either file has reached the end, exit the loop
                        break

                #if line2 == "?":
                #    print(line1, line2)
                all += 1
                if  line1 == line2 or line2 == "?":
                        corr += 1
#                else:
#                        print(line1, line2)
#                        input()
print(all, corr, corr/all)
