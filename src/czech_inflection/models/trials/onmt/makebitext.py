#!/usr/bin/env python3

import sys
import os

def tobitext(fn):
    data = []
    for line in eachline(fn):
        tokens = line.split("\t")
        if (len(tokens)!= 3):
            print(tokens)
            input()
        lemma = tokens[0]
        inflected = tokens[1]
        features = tokens[2]
        features = features.split(";")

        src = " ".join(lemma) + " # " + " ".join(features)
        tgt = " ".join(inflected)
        data.append((src,tgt))

def eachline(fn):
    with open(fn, "r"):
        for line in fn:
            if line!="":
                yield line

def writelines(fn, lines):
    with open(fn, "w") as fout:
        fout.writelines(lines)


def main():
    dirname = "data"

    train_file = sys.argv[1]
    dev_file = sys.argv[2]
    test_file = sys.argv[3]

    train = tobitext(train_file)
    dev = tobitext(dev_file)
    test = tobitext(test_file)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    writelines("data/train.src", [src for (src, tgt) in train])
    writelines("data/train.tgt", [tgt for (src, tgt) in train])
    writelines("data/dev.src", [src for (src, tgt) in dev])
    writelines("data/dev.tgt", [tgt for (src, tgt) in dev])
    writelines("data/test.src", [src for (src, tgt) in test])
    writelines("data/test.tgt", [tgt for (src, tgt) in test])
    



    
    
    

if __name__ == "__main__":
    main()