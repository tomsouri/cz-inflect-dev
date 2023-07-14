#!/bin/bash
# Example call:
#	bash evalSigRes.sh sig.pred gold.tgt NonneuralBaseline path/to/log/dir dev
SIG_PRED=$1
GOLD=$2
NAME=$3
LOGDIR=$4
DATASET=$5

HOME="/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection"
SPLIT_CHARS="scripts/data_conversion/split2chars.py"

EVALSCRIPT="src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py"

PYTHON=.venv/bin/python3

DEVPRED=$LOGDIR/$DATASET"_predictions.txt"
DEVGOLD=$GOLD

cd $HOME

cat $SIG_PRED | cut -f 2 | $PYTHON $SPLIT_CHARS > $DEVPRED

$PYTHON $EVALSCRIPT --name "$NAME""_"$DATASET""  --pred $DEVPRED --gold $DEVGOLD --logdir $LOGDIR
