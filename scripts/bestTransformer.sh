#!/bin/bash

# Path to config file
CONFIG=configs/Transformer_best.yaml

# Model
NAME="Transformer_best_v0.11_tutorial_batch1024_accumcount4_LR2"


# Current date in nice format for logging the results.
#CURDATE=$(date | sed "s/ /_/g")

# Directory for logging all files.
#LOGDIR="data/log/evaluate_models/onmt/experiments/$NAME""_""$CURDATE""/"


CHECKPOINT_PATH=""

# When training from checkpoint (because previous training failed)
#CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/Transformer_v0.9_Wu&Cotterell_Sun_Jun_11_09:29:17_CEST_2023/model/Transformer_v0.9_Wu&Cotterell_step_200000.pt"

#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection

DATADIR=/storage/praha1/home/souradat/tmp5-rp/rp-sourada/czech-automatic-inflection


#GENERAL_SCRIPT=$DATADIR/scripts/generalScript.sh

#GENERAL_SCRIPT=$DATADIR/scripts/generalTrain.sh

GENERAL_SCRIPT=$DATADIR/scripts/finalTrainEval.sh


bash $GENERAL_SCRIPT $DATADIR $CONFIG $NAME $CHECKPOINT_PATH
