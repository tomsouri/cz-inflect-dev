#!/bin/bash

# bash allOurData2sig.sh ../../data/cleaned/neural/ /storage/praha1/home/souradat/baselines/2022InflectionST/part1/development_languages/

srcdir=$1
tgtdir=$2

bash ourData2sig.sh $srcdir/train.src $srcdir/train.tgt $tgtdir/morfflex_large.train

bash ourData2sig.sh $srcdir/dev.src $srcdir/dev.tgt $tgtdir/morfflex.dev

bash ourData2sig.sh $srcdir/test.src $srcdir/test.tgt $tgtdir/morfflex.gold

bash ourData2sig.sh $srcdir/test-oov.src $srcdir/test-oov.tgt $tgtdir/morfflex.test-oov



# TODO: test-oov

