#!/bin/bash

# A script for running building vocabulary, training, translation, evaluation of
# the translation and evaluation of accuracies during training, using OpenNMT
# library.

DATADIR=$1

# Path to config file
CONFIG=$2

# Name of the model (to be able to recognize it among the other logged results)
NAME=$3

CHECKPOINT_PATH=$4

###############################################################################
######## PREPARE ALL VARIABLES ################################################

# The project datadir in Metacentrum.
#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
#DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

cd $DATADIR

# Current date in nice format for logging the results.
CURDATE=$(date | sed "s/ /_/g")

# Directory for logging all files.
LOGDIR="data/log/evaluate_models/onmt/experiments/$NAME""_""$CURDATE""/"

TRAIN_SCRIPT=$DATADIR/scripts/generalTrain.sh
#EVAL_SCRIPT=$DATADIR/scripts/generalEvaluation.sh

EVAL_LAST_CKP=$DATADIR/scripts/generalEvalOfLastCheckpoint.sh
EVAL_DURING=$DATADIR/scripts/generalEvalDuringTraining.sh

bash $TRAIN_SCRIPT $DATADIR $CONFIG $NAME $LOGDIR $CHECKPOINT_PATH

for DEV_PREFIX in "dev" "test" "test-oov";
do
    bash $EVAL_LAST_CKP $DATADIR $CONFIG $NAME $LOGDIR $DEV_PREFIX $CHECKPOINT_PATH ;
done


#bash $EVAL_DURING $DATADIR $CONFIG $NAME $LOGDIR $DEV_PREFIX $CHECKPOINT_PATH
