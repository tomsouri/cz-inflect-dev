
#!/bin/bash

# A script for running building vocabulary, training, translation, evaluation of
# the translation and evaluation of accuracies during training, using OpenNMT
# library.

DATAROOT=$1

DATADIR=$2

# Path to config file
CONFIG=$3

# Name of the model (to be able to recognize it among the other logged results)
NAME=$4

SMALL_DATA_STEM=$5

CHECKPOINT_PATH=$6




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

TRAIN_SCRIPT=$DATADIR/scripts/dataTrain.sh
EVAL_SCRIPT=$DATADIR/scripts/dataEvaluation.sh

DEV_PREFIX="dev"

bash $TRAIN_SCRIPT $DATAROOT $DATADIR $CONFIG $NAME $LOGDIR $CHECKPOINT_PATH

bash $EVAL_SCRIPT $DATAROOT $DATADIR $CONFIG $NAME $LOGDIR $DEV_PREFIX $SMALL_DATA_STEM $CHECKPOINT_PATH


# If the NAME says that it is running on sig data, evaluate it using the sig evaluate script.
if [[ $NAME == "DataSig22"* ]]; then
    cd $DATADIR
    #bash scripts/evalBySigEvaluation.sh $DATADIR $LOGDIR $NAME $DEV_PREFIX
    # Runs evaluation of the best model both on the dev and the test set.
    bash scripts/evalSigOnTest.sh $DATADIR $LOGDIR $NAME
else
    echo "Variable NAME does not start with 'DataSig22'."
    # Add alternative action here
fi
