#!/bin/bash

SRC=$1
TGT=$2

SIG=$3

mkdir -p tmp/

cat $SRC | cut -d "#" -f 1 | sed 's/ //g' > tmp/lemma.tmp

#cut -d "#" -f 2 train.src | sed 's/ //g' | sed 's/S/S;/g' | sed 's/P/P;/g' > tag.tmp

cat $SRC | sed 's/ # /\t/g' | cut -f 2 | sed 's/ /;/g' > tmp/tag.tmp

cat $TGT | sed 's/ //g' > tmp/form.tmp

paste tmp/lemma.tmp tmp/form.tmp tmp/tag.tmp > $SIG

rm tmp/*

rmdir tmp/
