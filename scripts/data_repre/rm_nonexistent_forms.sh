#!/bin/bash

# bash rm_nonexistent_forms.sh ../../data/cleaned/neural ../../data/cleaned/neural/dev_exps/removed_nonexistent


srcdir=$1
tgtdir=$2

TMP2=tmp2.tmp

for f in train train_small ; 
do
	paste $srcdir/$f.src $srcdir/$f.tgt | egrep -v "\?" > $TMP2
	cut -f 1 $TMP2 > $tgtdir/$f.src
    	cut -f 2 $TMP2 > $tgtdir/$f.tgt ;
done

# Copy other files
for f in $(ls $srcdir | egrep -v "train" | egrep "\."); do
    cp $srcdir/$f $tgtdir/ ;
done
