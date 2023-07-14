#!/bin/bash

# A script for running building vocabulary, training, translation, evaluation of
# the translation and evaluation of accuracies during training, using OpenNMT
# library.

# Path to config file
CONFIG=$1

# Name of the model (to be able to recognize it among the other logged results)
NAME=$2

###############################################################################
######## PREPARE ALL VARIABLES ################################################

# The project datadir in Metacentrum.
#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

cd $DATADIR

# Current date in nice format for logging the results.
CURDATE=$(date | sed "s/ /_/g")

# Directory for logging all files.
LOGDIR="data/log/evaluate_models/onmt/experiments/$NAME""_""$CURDATE""/"
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
     --tgt_vocab $TGT_VOCAB
#     --save_config $SAVE_CONFIG \

END=$(date +%s)
DIFF=$(( $END - $START ))
DIFF_MIN=$(($DIFF / 60))
DIFF_HOUR=$(($DIFF / 3600))
echo -e "TRAINING\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours"
echo -e "TRAINING\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours" >> $TIME_LOG

###############################################################################
######## TRANSLATION ##########################################################

START=$(date +%s)

.venv/bin/onmt_translate -model $MODEL_PATH -src $DEV  -output $DEVPRED  -gpu 0 -verbose

END=$(date +%s)
DIFF=$(( $END - $START ))
DIFF_MIN=$(($DIFF / 60))
DIFF_HOUR=$(($DIFF / 3600))
echo -e "TRANSLATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours"
echo -e "TRANSLATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours" >> $TIME_LOG

###############################################################################
######## EVALUATION OF FINAL MODEL ############################################

START=$(date +%s)

.venv/bin/python3 $EVALSCRIPT --name $NAME  --pred $DEVPRED --gold $DEVGOLD --logdir $LOGDIR

END=$(date +%s)
DIFF=$(( $END - $START ))
DIFF_MIN=$(($DIFF / 60))
DIFF_HOUR=$(($DIFF / 3600))
echo -e "EVALUATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours"
echo -e "EVALUATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours" >> $TIME_LOG

###############################################################################
######## EVALUATION OF ACCS DURING TRAINING ###################################

START=$(date +%s)

# Dir to save the predicitons
tmpdir=$LOGDIR"tmp/"
mkdir -p $tmpdir

# File prefixes to save the predictions.
dev_prefix=$tmpdir"dev_small.pred"
train_prefix=$tmpdir"train_small.pred"

for (( i=$EVERY; i<=$STEPS; i+=$EVERY ))
do 
    # The concrete model checkpoint after i steps of training.
    model="$LOGDIRMODEL""$NAME""_step_$i.pt"

    # Translate the dev data.
    dev_pred=$dev_prefix$i
    .venv/bin/onmt_translate -model $model -src $DEV_SMALL  -output $dev_pred  -gpu 0 -verbose


    # Translate the train data.
    train_pred=$train_prefix$i
    .venv/bin/onmt_translate -model $model -src $TRAIN_SMALL  -output $train_pred  -gpu 0 -verbose

done

# TODO: During building of the data,
# vytvorit dev_small.src, tgt
# head -n14000 dev.tgt > dev_small.tgt

# Evaluate the accuracies on dev and train data for all model checkpoints.
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

###############################################################################
######## THE END ##############################################################


git add -f $LOGDIR/*.*
git commit -m'experiment logs'

git add docs/hyperparams.txt
git commit -m'hyperparams diary'













