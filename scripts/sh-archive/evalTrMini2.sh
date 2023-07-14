#!/bin/bash

# Path to config file
CONFIG=configs/transformer_mini2.yaml

# Model
NAME="Transformer_v0.7_batch32_drops0.2_hid64_wv64_2he_1lay_ff128"

LOGDIR="data/log/evaluate_models/onmt/experiments/Transformer_v0.7_batch32_drops0.2_hid64_wv64_2he_1lay_ff128_Sat_May_20_19:38:03_CEST_2023/"

DEV_PREFIX="dev"

# Current date in nice format for logging the results.
#CURDATE=$(date | sed "s/ /_/g")

# Directory for logging all files.
#LOGDIR="data/log/evaluate_models/onmt/experiments/$NAME""_""$CURDATE""/"


CHECKPOINT_PATH=""

# When training from checkpoint (because previous training failed)
#CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/Transformer_v0.2_tutorial_Wed_May__3_12:52:11_CEST_2023/model/Transformer_v0.2_tutorial_step_65000.pt"
#CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/Transformer_v0.5_batch32_drops0.2_hid64_wv64_1he_1lay_ff128_Mon_May_15_16:17:45_CEST_2023/model/Transformer_v0.5_batch32_drops0.2_hid64_wv64_1he_1lay_ff128_step_4000000.pt"
#CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/Transformer_v0.6_batch32_drops0.2_hid64_wv64_1he_1lay_ff128_Wed_May_17_23:10:52_CEST_2023/model/Transformer_v0.6_batch32_drops0.2_hid64_wv64_1he_1lay_ff128_step_5520000.pt"
#CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/Transformer_v0.7_batch32_drops0.2_hid64_wv64_2he_1lay_ff128_Fri_May_19_00:07:34_CEST_2023/model/Transformer_v0.7_batch32_drops0.2_hid64_wv64_2he_1lay_ff128_step_1920000.pt"


#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection


GENERAL_SCRIPT=$DATADIR/scripts/generalEvaluation.sh

#GENERAL_SCRIPT=$DATADIR/scripts/generalTrain.sh

bash $GENERAL_SCRIPT $DATADIR $CONFIG $NAME $LOGDIR $DEV_PREFIX $CHECKPOINT_PATH
