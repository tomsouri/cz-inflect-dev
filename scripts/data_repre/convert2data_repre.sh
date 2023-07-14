#!/bin/bash

# bash convert2data_repre.sh ../../data/cleaned/neural ../../data/cleaned/neural/dev_exps/1_tag_at_beginning tag_at_beginning.py copyScript.sh python3 bash

# bash convert2data_repre.sh neural data_exps/1_tag_at_beginning processSrc.sh processTgt.sh python3 bash

srcdir=$1
tgtdir=$2

src_proc_script=$3
tgt_proc_script=$4

SRC_RUNNER=$5
TGT_RUNNER=$6

for f in $(ls $srcdir/*.src); 
do
	fn=$(basename "$f")
	tgtf=$tgtdir/$fn
	$SRC_RUNNER $src_proc_script $f $tgtf
done

for f in $(ls $srcdir/*.tgt); 
do
	fn=$(basename "$f")
	tgtf=$tgtdir/$fn
	$TGT_RUNNER $tgt_proc_script $f $tgtf
done


