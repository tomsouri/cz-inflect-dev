#!/bin/bash

srcf=$1
tgtf=$2

cat $srcf | sed 's/ #//g' > $tgtf
