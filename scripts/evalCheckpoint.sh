#!/bin/bash

# A script for running evaluation of a specific checkpoint.

DATADIR=$1

# Path to config file
# Not used
CONFIG=$2

# Name of the model (to be able to recognize it among the other logged results)
# The number of training steps of the specific checkpoint should be specified
# there! 
NAME=$3

LOGDIR=$4

DEV_PREFIX=$5

# Number of steps of training
CHECKPOINT=$6

MODEL_PATH=$7


###############################################################################
######## PREPARE ALL VARIABLES ################################################

# The project datadir in Metacentrum.
#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
#DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

cd $DATADIR

CHECKPOINT_LOGDIR="$LOGDIR""checkpoints_eval/""$CHECKPOINT""steps/"
mkdir -p $CHECKPOINT_LOGDIR

TIME_LOG="$CHECKPOINT_LOGDIR""time.log"
# File to store dev predictions of the final model.
DEVPRED="$CHECKPOINT_LOGDIR""predictions.txt"

# Data for dev evaluation of the final model.
DEV="data/cleaned/neural/""$DEV_PREFIX"".src"
DEVGOLD="data/cleaned/neural/""$DEV_PREFIX"".tgt"


# Paths to scripts for evaluating.
# (Those are my own scripts and are coded in a very messy way...
# But since I use an only slightly changed version to evaluate the other models
# too, I do not expect them to cause the problem.)
EVALSCRIPT="src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py"
#EVAL_DURING_TRAINING="src/czech_inflection/dev_testing/eval_models/eval_during_training.py"

###############################################################################
######## TRANSLATION ##########################################################

START=$(date +%s)

.venv/bin/onmt_translate -model $MODEL_PATH -src $DEV  -output $DEVPRED  -gpu 0 -batch_size 2048

END=$(date +%s)
DIFF=$(( $END - $START ))
DIFF_MIN=$(($DIFF / 60))
DIFF_HOUR=$(($DIFF / 3600))
echo -e "TRANSLATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours"
echo -e "TRANSLATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours" >> $TIME_LOG

###############################################################################
######## EVALUATION OF FINAL MODEL ############################################

START=$(date +%s)

.venv/bin/python3 $EVALSCRIPT --name $NAME  --pred $DEVPRED --gold $DEVGOLD --logdir $CHECKPOINT_LOGDIR --train_steps $CHECKPOINT

END=$(date +%s)
DIFF=$(( $END - $START ))
DIFF_MIN=$(($DIFF / 60))
DIFF_HOUR=$(($DIFF / 3600))
echo -e "EVALUATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours"
echo -e "EVALUATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours" >> $TIME_LOG

# ###############################################################################
######## THE END ##############################################################


git add -f $CHECKPOINT_LOGDIR/*.*
git commit -m'experiment logs'

git add docs/hyperparams.txt
git commit -m'hyperparams diary'
