#!/bin/bash

ROOTDIR="neural/data_exps/6_complex"
#ROOTDIR="neural"

# Model
NAME="Data_06_complex_LSTM_v0.40"

SMALL_DATA_STEM="_small"

# Path to config file
CONFIG=configs/data.yaml

CHECKPOINT_PATH=""
#CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/LSTM_v0.34_2_lay+batch20+emb64+brnn_enc+hid_100_Fri_May_19_13:35:58_CEST_2023/model/LSTM_v0.34_2_lay+batch20+emb64+brnn_enc+hid_100_step_1040000.pt"

#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

GENERAL_SCRIPT=$DATADIR/scripts/dataScript.sh

bash $GENERAL_SCRIPT $ROOTDIR $DATADIR $CONFIG $NAME $SMALL_DATA_STEM $CHECKPOINT_PATH
