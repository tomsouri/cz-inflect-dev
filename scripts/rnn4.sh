#!/bin/bash

# Path to config file
CONFIG=configs/rnn4.yaml

# Model
NAME="LSTM_v0.46_3_lay+batch256+emb64+brnn_enc+hid_100"

CHECKPOINT_PATH=""
#CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/LSTM_v0.27_def+1_layers+batchsize20+wordEmb64+shared_embs+brnn_enc+hidden_100+adam+0.001_learnRate+2048_validBatch_Sat_May_13_06:40:37_CEST_2023/model/LSTM_v0.27_def+1_layers+batchsize20+wordEmb64+shared_embs+brnn_enc+hidden_100+adam+0.001_learnRate+2048_validBatch_step_260000.pt"
#CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/LSTM_v0.33_2_lay+batch20+emb64+brnn_enc+hid_100_Fri_May_19_00:04:52_CEST_2023/model/LSTM_v0.33_2_lay+batch20+emb64+brnn_enc+hid_100_step_260000.pt"
#CHECKPOINT_PATH="data/log/evaluate_models/onmt/experiments/LSTM_v0.34_2_lay+batch20+emb64+brnn_enc+hid_100_Fri_May_19_13:35:58_CEST_2023/model/LSTM_v0.34_2_lay+batch20+emb64+brnn_enc+hid_100_step_1040000.pt"

#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

GENERAL_SCRIPT=$DATADIR/scripts/generalScript.sh

bash $GENERAL_SCRIPT $DATADIR $CONFIG $NAME $CHECKPOINT_PATH
