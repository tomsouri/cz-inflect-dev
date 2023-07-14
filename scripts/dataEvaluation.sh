#!/bin/bash

# A script for running building vocabulary, training, translation, evaluation of
# the translation and evaluation of accuracies during training, using OpenNMT
# library.

DATAROOT=$1

DATADIR=$2

# Not used
# Path to config file
CONFIG=$3

# Name of the model (to be able to recognize it among the other logged results)
NAME=$4

LOGDIR=$5

DEV_PREFIX=$6

SMALL_DATA_STEM=$7

CHECKPOINT_PATH=$8

###############################################################################
######## PREPARE ALL VARIABLES ################################################

# The project datadir in Metacentrum.
#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
#DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

cd $DATADIR

TRANSL_BATCHSIZE=4096

# Use the saved config, not the general one.
CONFIG="$LOGDIR""config.yaml"

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

DATAPATH="data/cleaned/"$DATAROOT

# Data for dev evaluation of the final model.
DEV=$DATAPATH"/""$DEV_PREFIX"".src"
DEVGOLD=$DATAPATH"/""$DEV_PREFIX"".tgt"

# Smaller data for evaluation of accs during training.
DEV_SMALL=$DATAPATH"/dev"$SMALL_DATA_STEM".src"
DEV_SMALL_GOLD=$DATAPATH/"/dev"$SMALL_DATA_STEM".tgt"
TRAIN_SMALL=$DATAPATH"/train"$SMALL_DATA_STEM".src"
TRAIN_SMALL_GOLD=$DATAPATH"/train"$SMALL_DATA_STEM".tgt"

# Paths to scripts for evaluating.
# (Those are my own scripts and are coded in a very messy way...
# But since I use an only slightly changed version to evaluate the other models
# too, I do not expect them to cause the problem.)
EVALSCRIPT="src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py"
EVAL_DURING_TRAINING="src/czech_inflection/dev_testing/eval_models/eval_during_training.py"

###############################################################################
######## TRANSLATION ##########################################################

START=$(date +%s)

.venv/bin/onmt_translate -model $MODEL_PATH -src $DEV  -output $DEVPRED  -gpu 0 -batch_size $TRANSL_BATCHSIZE

END=$(date +%s)
DIFF=$(( $END - $START ))
DIFF_MIN=$(($DIFF / 60))
DIFF_HOUR=$(($DIFF / 3600))
echo -e "TRANSLATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours"
echo -e "TRANSLATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours" >> $TIME_LOG

###############################################################################
######## EVALUATION OF FINAL MODEL ############################################

START=$(date +%s)

.venv/bin/python3 $EVALSCRIPT --name $NAME  --pred $DEVPRED --gold $DEVGOLD --logdir $LOGDIR --train_steps $STEPS

END=$(date +%s)
DIFF=$(( $END - $START ))
DIFF_MIN=$(($DIFF / 60))
DIFF_HOUR=$(($DIFF / 3600))
echo -e "EVALUATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours"
echo -e "EVALUATION\t took $DIFF seconds\t = $DIFF_MIN minutes\t = $DIFF_HOUR hours" >> $TIME_LOG

###############################################################################
# Dir to save the predicitons
tmpdir=$LOGDIR"tmp/"
mkdir -p $tmpdir


if [ -n "$CHECKPOINT_PATH" ]; then
    # Extract the directory path of the file
    MODELS=$(dirname "$CHECKPOINT_PATH")

    # Extract the parent directory of MODELS
    PREVDIR=$(dirname "$MODELS")

    cp "$PREVDIR""/tmp/"* $tmpdir
fi




###############################################################################
######## EVALUATION OF ACCS DURING TRAINING ###################################

START=$(date +%s)



# File prefixes to save the predictions.
dev_prefix=$tmpdir"dev_small.pred"
train_prefix=$tmpdir"train_small.pred"


numbers=()  # Initialize an empty array to store the extracted numbers

# Iterate over files in the directory
for file in "$LOGDIRMODEL"*; do
    # Extract the number from the filename
    if [[ $file =~ ([0-9]+)\.pt$ ]]; then
        number=${BASH_REMATCH[1]}
        numbers+=("$number")  # Append the extracted number to the array
    fi
done

# Iterate over the array of numbers
for i in "${numbers[@]}"; do
    # The concrete model checkpoint after i steps of training.
    model="$LOGDIRMODEL""$NAME""_step_$i.pt"

    # Translate the dev data.
    dev_pred=$dev_prefix$i
    .venv/bin/onmt_translate -model $model -src $DEV_SMALL  -output $dev_pred  -gpu 0 -batch_size $TRANSL_BATCHSIZE

    # Translate the train data.
    train_pred=$train_prefix$i
    .venv/bin/onmt_translate -model $model -src $TRAIN_SMALL  -output $train_pred  -gpu 0 -batch_size $TRANSL_BATCHSIZE

done




# for (( i=$EVERY; i<=$STEPS; i+=$EVERY ))
# do 
#     # The concrete model checkpoint after i steps of training.
#     model="$LOGDIRMODEL""$NAME""_step_$i.pt"

#     # Translate the dev data.
#     dev_pred=$dev_prefix$i
#     .venv/bin/onmt_translate -model $model -src $DEV_SMALL  -output $dev_pred  -gpu 0 -batch_size $TRANSL_BATCHSIZE


#     # Translate the train data.
#     train_pred=$train_prefix$i
#     .venv/bin/onmt_translate -model $model -src $TRAIN_SMALL  -output $train_pred  -gpu 0 -batch_size $TRANSL_BATCHSIZE

# done

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


git add -f $LOGDIR/*.yaml
git add -f $LOGDIR/*.log
git add -f $LOGDIR/*.jpg
git add -f $LOGDIR/vocab.*
git add -f $LOGDIR/training_accs.txt

git commit -m'experiment logs'

git add docs/hyperparams.txt
git commit -m'hyperparams diary'
