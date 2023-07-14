#!/bin/bash

# Path to config file
# Not used
CONFIG=configs/rnn.yaml

#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

GENERAL_SCRIPT=$DATADIR/scripts/evalCheckpoint.sh

# Model
#NAME="LSTM_v0.21_def+4_layers+batchsize256+wordEmb128+shared_embs"
#NAME="LSTM_v0.26_def+1_layers+batchsize20+wordEmb64+shared_embs+brnn_enc+hidden_100+adam+0.001_learnRate"
#NAME="LSTM_v0.27_def+1_layers+batchsize20+wordEmb64+shared_embs+brnn_enc+hidden_100+adam+0.001_learnRate+2048_validBatch"
#NAME="LSTM_v0.25_def+1_layers+batchsize20+wordEmb64+shared_embs+brnn_enc+hidden_100"
#NAME="LSTM_v0.41_2_lay+batch256+emb64+brnn_enc+hid_250"
NAME="LSTM_v0.42_3_lay+batch256+emb64+brnn_enc+hid_100"

# Should end with "/"
#LOGDIR="data/log/evaluate_models/onmt/experiments/LSTM_v0.18_def+4_layers_batchsize256+wordEmb256+40k_steps_Sun_Apr_30_22:11:39_CEST_2023/"
#LOGDIR="data/log/evaluate_models/onmt/experiments/LSTM_v0.17_def+4_layers_batchsize256+wordEmb128+40k_steps_Sun_Apr_30_11:44:42_CEST_2023/"
#LOGDIR="data/log/evaluate_models/onmt/experiments/LSTM_v0.21_def+4_layers+batchsize256+wordEmb128+shared_embs_Tue_May__2_07:30:38_CEST_2023/"
#LOGDIR="data/log/evaluate_models/onmt/experiments/LSTM_v0.26_def+1_layers+batchsize20+wordEmb64+shared_embs+brnn_enc+hidden_100+adam+0.001_learnRate_Fri_May_12_23:43:44_CEST_2023/"
#LOGDIR="data/log/evaluate_models/onmt/experiments/LSTM_v0.25_def+1_layers+batchsize20+wordEmb64+shared_embs+brnn_enc+hidden_100_Fri_May_12_23:21:59_CEST_2023/"
#LOGDIR="data/log/evaluate_models/onmt/experiments/LSTM_v0.41_2_lay+batch256+emb64+brnn_enc+hid_250_Wed_May_24_16:52:46_CEST_2023/"
#"LSTM_v0.41_2_lay+batch256+emb64+brnn_enc+hid_250_Wed_May_24_16:52:46_CEST_2023/"
LOGDIR="data/log/evaluate_models/onmt/experiments/LSTM_v0.42_3_lay+batch256+emb64+brnn_enc+hid_100_Wed_May_24_16:58:04_CEST_2023/"
# Eval on negation data: neg2.dev

DEV_PREFIX="dev"

CHECKPOINT="260000"

MODEL_PATH="$LOGDIR""model/""$NAME""_step_""$CHECKPOINT"".pt"

bash $GENERAL_SCRIPT $DATADIR $CONFIG $NAME $LOGDIR $DEV_PREFIX $CHECKPOINT $MODEL_PATH
