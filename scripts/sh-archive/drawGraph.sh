#!/bin/bash

# TODO CONFIG
#CONFIG=configs/generalConfig.yaml
# TODO NAME
#NAME=GeneralModel_v0.3

CONFIG=$1
NAME=$2

#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

# TODO: REMOVE
#DATADIR=/svolume/matfyz/rp-sourada/czech-automatic-inflection


cd $DATADIR

CURDATE=$(date | sed "s/ /_/g")


#DIR=$(cat $CONFIG | egrep "save_model:" | sed 's/save_model: //g')
#MODEL=data/inner/onmt/run/model_is_training_independent_of_eval_set_TEST2_step_25000.pt

###
LOGDIR="data/log/evaluate_models/onmt/experiments/LSTM_v0.3_default_Sun_Apr_23_15:22:04_CEST_2023/"
#LOGDIR="data/log/evaluate_models/onmt/experiments/$NAME""_""$CURDATE""/"
# TRAIN_LOG="$LOGDIR""train.log"
# SRC_VOCAB="$LOGDIR""vocab.src"
# TGT_VOCAB="$LOGDIR""vocab.tgt"
#TIME_LOG="$LOGDIR""time.log"


LOGDIRMODEL=$LOGDIR"model/"
mkdir -p $LOGDIRMODEL
SAVE_MODEL="$LOGDIRMODEL""$NAME"


STEPS=$(cat $CONFIG | egrep "train_steps:" | sed 's/train_steps: //g')
EVERY=$(cat $CONFIG | egrep "save_checkpoint_steps:" | sed 's/save_checkpoint_steps: //g')
MODEL_PATH="$LOGDIRMODEL""$NAME""_step_$STEPS.pt"


DEVPRED="$LOGDIR""predictions.txt"

DEV=data/cleaned/neural/dev.src
DEVGOLD=data/cleaned/neural/dev.tgt

DEV_SMALL=data/cleaned/neural/dev_small.src
DEV_SMALL_GOLD=data/cleaned/neural/dev_small.tgt
TRAIN_SMALL=data/cleaned/neural/train_small.src
TRAIN_SMALL_GOLD=data/cleaned/neural/train_small.tgt


EVALSCRIPT="src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py"
EVAL_DURING_TRAINING="src/czech_inflection/dev_testing/eval_models/eval_during_training.py"


START=$(date +%s)

tmpdir=$LOGDIR"tmp/"
mkdir -p $tmpdir
dev_prefix=$tmpdir"dev_small.pred"
train_prefix=$tmpdir"train_small.pred"

for (( i=$EVERY; i<=$STEPS; i+=$EVERY ))
do 
    model="$LOGDIRMODEL""$NAME""_step_$i.pt"

    dev_pred=$dev_prefix$i
    .venv/bin/onmt_translate -model $model -src $DEV_SMALL  -output $dev_pred  -gpu 0 -verbose

    train_pred=$train_prefix$i
    .venv/bin/onmt_translate -model $model -src $TRAIN_SMALL  -output $train_pred  -gpu 0 -verbose

done

# vytvorit dev_small.src, tgt
# head -n14000 dev.tgt > dev_small.tgt
.venv/bin/python3 $EVAL_DURING_TRAINING --name $NAME \
    --dev_pred $dev_prefix \
    --dev_gold $DEV_SMALL_GOLD \
    --train_pred $train_prefix \
    --train_gold $TRAIN_SMALL_GOLD \
    --every $EVERY \
    --max_steps $STEPS \
    --logdir $LOGDIR

END=$(date +%s)
DIFF=$(( $END - $START ))
DIFF_MIN=$(($DIFF / 60))
DIFF_HOUR=$(($DIFF / 3600))
echo -e "TRAIN-DEV ACCS\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours"
echo -e "TRAIN-DEV ACCS\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours" >> $TIME_LOG
