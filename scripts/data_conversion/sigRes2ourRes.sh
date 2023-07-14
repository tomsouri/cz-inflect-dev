#!/bin/bash

# Not used

SIG=$1
OUR=$2

cat $SIG | cut -f 2 | python3 split2chars.py > $OUR
