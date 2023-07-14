#!/bin/bash

# Path to config file
CONFIG=configs/transformer_mini.yaml

# Model
#NAME="Transformer_v0.3_batchTypeSents_batch64_droupouts0.2_hidden256_wordvec256"
NAME="Transformer_v0.4_warpup4k_batch32_droupouts0.2_hid64_wordvec64_1head_1layer_ff128"


# Directory for logs
# Should en with "/"
#LOGDIR="data/log/evaluate_models/onmt/experiments/Transformer_v0.3_batchTypeSents_batch64_droupouts0.2_hidden256_wordvec256_Fri_May_12_22:45:55_CEST_2023/"
LOGDIR="data/log/evaluate_models/onmt/experiments/Transformer_v0.4_warpup4k_batch32_droupouts0.2_hid64_wordvec64_1head_1layer_ff128_Sun_May_14_01:00:43_CEST_2023/"

#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

GENERAL_SCRIPT=$DATADIR/scripts/generalEvaluation.sh

DEV_PREFIX="dev_medium"

bash $GENERAL_SCRIPT $DATADIR $CONFIG $NAME $LOGDIR $DEV_PREFIX
