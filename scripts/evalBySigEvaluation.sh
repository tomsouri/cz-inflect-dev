#!/bin/bash

DATADIR=$1
LOGDIR=$2
NAME=$3
DEV_PREFIX=$4

origpred=$DATADIR/$LOGDIR"predictions.txt"
nospace=$DATADIR/$LOGDIR"nospace_pred.txt"

# Here replace back the special <SPACE> token by space.
cat $origpred | sed 's/ //g' | sed 's/<SPACE>/ /g' > $nospace

# Extract the language
tmp=${NAME#*_}
tmp=${tmp%%_*}
lang=$(echo "$tmp" | tr '[:upper:]' '[:lower:]')

sigdatadir="/storage/praha1/home/souradat/baselines/2022InflectionST/part1/development_languages"
lemmata=$DATADIR/$LOGDIR"lemmata.tmp"
features=$DATADIR/$LOGDIR"features.tmp"

cut -f 1 $sigdatadir/$lang.dev > $lemmata
cut -f 3 $sigdatadir/$lang.dev > $features
sigpreds="/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection/data/log/evaluate_models/sig"
paste $lemmata $nospace $features > $sigpreds/$lang"_large."$DEV_PREFIX

sigevaldir="/storage/praha1/home/souradat/baselines/2022InflectionST/evaluation"
cd $sigevaldir
python3 evaluate.py $sigpreds $sigdatadir $DATADIR/$LOGDIR"ALL_SIG_EVAL.txt" --evaltype dev --partition _large

cd $DATADIR
#git add $LOGDIR"ALL_SIG_EVAL.txt"
#git commit -m'my model on sig evaluation'
