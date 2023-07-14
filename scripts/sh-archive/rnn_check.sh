#!/bin/bash

# Path to config file
CONFIG=configs/rnn_check.yaml

# Model
NAME="check_LSTM_v0.23_def+4_layers+batchsize256+wordEmb128"

CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/LSTM_v0.23_def+4_layers+batchsize256+wordEmb128_Wed_May__3_13:01:45_CEST_2023/model/LSTM_v0.23_def+4_layers+batchsize256+wordEmb128_step_100000.pt"

#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

GENERAL_SCRIPT=$DATADIR/scripts/generalScript.sh

bash $GENERAL_SCRIPT $DATADIR $CONFIG $NAME $CHECKPOINT_PATH