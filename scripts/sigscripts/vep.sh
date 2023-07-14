#!/bin/bash

#ROOTDIR="neural/data_exps/1_tag_at_beginning"
ROOTDIR="neural/sig22/vep"
#ROOTDIR="neural"

# Model
NAME="DataSig22_VEP_LSTM_v0.40_warm4k"

SMALL_DATA_STEM=""

# Path to config file
CONFIG=configs/sig_general.yaml

CHECKPOINT_PATH=""
#CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/LSTM_v0.34_2_lay+batch20+emb64+brnn_enc+hid_100_Fri_May_19_13:35:58_CEST_2023/model/LSTM_v0.34_2_lay+batch20+emb64+brnn_enc+hid_100_step_1040000.pt"

#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

GENERAL_SCRIPT=$DATADIR/scripts/dataScript.sh

bash $GENERAL_SCRIPT $ROOTDIR $DATADIR $CONFIG $NAME $SMALL_DATA_STEM $CHECKPOINT_PATH
