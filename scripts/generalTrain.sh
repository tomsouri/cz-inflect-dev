#!/bin/bash

# A script for running building vocabulary, training, translation, evaluation of
# the translation and evaluation of accuracies during training, using OpenNMT
# library.

DATADIR=$1

# Path to config file
CONFIG=$2

# Name of the model (to be able to recognize it among the other logged results)
NAME=$3

LOGDIR=$4

# If set to "", means no checkpoint and it is the default setting in ONMT for
# no checkpoint.
# Used for training from a trained model.
CHECKPOINT_PATH=$5

###############################################################################
######## PREPARE ALL VARIABLES ################################################

# The project datadir in Metacentrum.
#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
#DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

cd $DATADIR

# Current date in nice format for logging the results.
#CURDATE=$(date | sed "s/ /_/g")

# Directory for logging all files.
#LOGDIR="data/log/evaluate_models/onmt/experiments/$NAME""_""$CURDATE""/"
TRAIN_LOG="$LOGDIR""train.log"
SRC_VOCAB="$LOGDIR""vocab.src"
TGT_VOCAB="$LOGDIR""vocab.tgt"
TIME_LOG="$LOGDIR""time.log"

# Where to save model checkpoints during training.
LOGDIRMODEL=$LOGDIR"model/"
mkdir -p $LOGDIRMODEL
SAVE_MODEL="$LOGDIRMODEL""$NAME"

# Extract some variables from the config file,
STEPS=$(cat $CONFIG | egrep "train_steps:" | sed 's/train_steps: //g')
EVERY=$(cat $CONFIG | egrep "save_checkpoint_steps:" | sed 's/save_checkpoint_steps: //g')

# The path to final model (after all training steps)
MODEL_PATH="$LOGDIRMODEL""$NAME""_step_$STEPS.pt"

# TODO: misto prepisovani v CONFIGu muzu dle
# https://opennmt.net/OpenNMT-py/options/train.html
# upravit parametry na command line a dat --save_config (toto misto kopirovani
# configu)

# File to store dev predictions of the final model.
DEVPRED="$LOGDIR""predictions.txt"

# Data for dev evaluation of the final model.
DEV=data/cleaned/neural/dev.src
DEVGOLD=data/cleaned/neural/dev.tgt

# Smaller data for evaluation of accs during training.
DEV_SMALL=data/cleaned/neural/dev_small.src
DEV_SMALL_GOLD=data/cleaned/neural/dev_small.tgt
TRAIN_SMALL=data/cleaned/neural/train_small.src
TRAIN_SMALL_GOLD=data/cleaned/neural/train_small.tgt

# Paths to scripts for evaluating.
# (Those are my own scripts and are coded in a very messy way...
# But since I use an only slightly changed version to evaluate the other models
# too, I do not expect them to cause the problem.)
EVALSCRIPT="src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py"
EVAL_DURING_TRAINING="src/czech_inflection/dev_testing/eval_models/eval_during_training.py"

# Where to save the complete configuration file.
SAVE_CONFIG="$LOGDIR""config_""$NAME""_""$CURDATE"".yaml"

# Copy config file as it is.
cp $CONFIG $LOGDIR"config.yaml"

###############################################################################
#### BUILD VOCAB ##############################################################

# This is to measure time elapsed during different phases of the script.
START=$(date +%s)

# Run this to save the configuration file
# (does not build the vocabularies, I have no idea why)
.venv/bin/onmt_build_vocab -config $CONFIG -n_sample -1 \
    --save_config $SAVE_CONFIG \
    --src_vocab $SRC_VOCAB \
    --tgt_vocab $TGT_VOCAB

# Run this to build the vocabularies
.venv/bin/onmt_build_vocab -config $CONFIG -n_sample -1 \
    --src_vocab $SRC_VOCAB \
    --tgt_vocab $TGT_VOCAB

# This is to measure time elapsed during different phases of the script.
END=$(date +%s)
DIFF=$(( $END - $START ))
DIFF_MIN=$(($DIFF / 60))
DIFF_HOUR=$(($DIFF / 3600))
echo -e "BUILD_VOCAB\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours"
echo -e "BUILD_VOCAB\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours" >> $TIME_LOG

###############################################################################
######## TRAINING #############################################################

START=$(date +%s)

.venv/bin/onmt_train --config $CONFIG \
     --log_file $TRAIN_LOG \
     --save_model $SAVE_MODEL \
     --src_vocab $SRC_VOCAB \
     --tgt_vocab $TGT_VOCAB \
     --log_file_level "DEBUG" \
     --train_from "$CHECKPOINT_PATH"
#     --save_config $SAVE_CONFIG \

END=$(date +%s)
DIFF=$(( $END - $START ))
DIFF_MIN=$(($DIFF / 60))
DIFF_HOUR=$(($DIFF / 3600))
echo -e "TRAINING\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours"
echo -e "TRAINING\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours" >> $TIME_LOG

echo $LOGDIR
