#!/bin/bash

DATADIR=$1
#DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

LOGDIR=$2
#LOGDIR="data/log/evaluate_models/onmt/experiments/DataSig22_SLK_\<SPACE\>_LSTM_v0.40_Fri_Jun_30_20\:07\:24_CEST_2023/"
#LOGDIR="data/log/evaluate_models/onmt/experiments/DataSig22_SLK_<SPACE>_LSTM_v0.40_Fri_Jun_30_20:07:24_CEST_2023/"

# model name
NAME=$3
#NAME="DataSig22_SLK_\<SPACE\>_LSTM_v0.40"
#NAME="DataSig22_SLK_<SPACE>_LSTM_v0.40"

cd $DATADIR

STEPS=$(cat $LOGDIR"training_accs.txt" | sed 's/ //g' | sed 's/0\./\t0\./g' | cut -f 1 | egrep "\!" | sed 's/\!\!//g'  | tail -n1)

# Extract the language
tmp=${NAME#*_}
tmp=${tmp%%_*}
lang=$(echo "$tmp" | tr '[:upper:]' '[:lower:]')

MODEL_PATH="$LOGDIR""model/""$NAME""_step_$STEPS.pt"

for SET in dev test; do

	# source file for test predictions
	DEV=$DATADIR/data/cleaned/neural/sig22/$lang/$SET.src
	DEVGOLD=$DATADIR/data/cleaned/neural/sig22/$lang/$SET.tgt

	# target file for my predictions
	origpred="$LOGDIR""$SET""_predictions.txt"

	TRANSL_BATCHSIZE=4096

	# CREATE PREDICTIONS AND EVAL BY MY SCRIPT

	cd $DATADIR

	echo "Running translation of sig22 $lang $SET set with model $NAME""_step_""$STEPS.pt"

	.venv/bin/onmt_translate -model $MODEL_PATH -src $DEV  -output $origpred  -gpu 0 -batch_size $TRANSL_BATCHSIZE

	EVALSCRIPT="src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py"

	.venv/bin/python3 $EVALSCRIPT --name $NAME"_""$SET"  --pred $origpred --gold $DEVGOLD --logdir $LOGDIR --train_steps $STEPS


	# CONVERT TO SIG FORMAT AND EVAL

	nospace=$DATADIR/$LOGDIR"$SET""_nospace_pred.txt"

	# Here replace back the special <SPACE> token by space.
	cat $origpred | sed 's/ //g' | sed 's/<SPACE>/ /g' > $nospace

	sigdatadir="/storage/praha1/home/souradat/baselines/2022InflectionST/part1/development_languages"
	lemmata=$DATADIR/$LOGDIR$SET"_lemmata.tmp"
	features=$DATADIR/$LOGDIR$SET"_features.tmp"

	if [ "$SET" = "dev" ]; then
	    suffix="dev"
	else
	    suffix="gold"
	fi

	cut -f 1 $sigdatadir/$lang.$suffix > $lemmata
	cut -f 3 $sigdatadir/$lang.$suffix > $features

	# Create the sig-format prediction file
	sigpreds="/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection/data/log/evaluate_models/sig"
	paste $lemmata $nospace $features > $sigpreds/$lang"_large.""$SET"

	sigevaldir="/storage/praha1/home/souradat/baselines/2022InflectionST/evaluation"
	cd $sigevaldir
	python3 evaluate.py $sigpreds $sigdatadir $DATADIR/$LOGDIR"ALL_SIG_EVAL.txt" --evaltype $SET --partition _large ;
done
