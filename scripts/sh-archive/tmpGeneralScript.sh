#!/bin/bash

# TODO CONFIG
CONFIG=configs/generalConfig.yaml
# TODO NAME
NAME=GeneralModel_v0.3

#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection
cd $DATADIR

CURDATE=$(date | sed "s/ /_/g")


#DIR=$(cat $CONFIG | egrep "save_model:" | sed 's/save_model: //g')


#MODEL=data/inner/onmt/run/model_is_training_independent_of_eval_set_TEST2_step_25000.pt

LOGDIR="data/log/evaluate_models/onmt/experiments/$NAME""_""$CURDATE""/"
TRAIN_LOG="$LOGDIR""train.log"
SRC_VOCAB="$LOGDIR""vocab.src"
TGT_VOCAB="$LOGDIR""vocab.tgt"


LOGDIRMODEL=$LOGDIR"model/"
mkdir -p $LOGDIRMODEL
SAVE_MODEL="$LOGDIRMODEL""$NAME"


STEPS=$(cat $CONFIG | egrep "train_steps:" | sed 's/train_steps: //g')
MODEL_PATH="$LOGDIRMODEL""$NAME""_step_$STEPS.pt"

# TODO: misto prepisovani v CONFIGu muzu dle
# https://opennmt.net/OpenNMT-py/options/train.html
# upravit parametry na command line a dat --save_config (toto misto kopirovani
# configu)

#cat $CONFIG | sed "s=log_file: =log_file: $TRAIN_LOG\n# =g" | sed "s=save_model: model=save_model: $LOGDIRMODEL$NAMEn#=g" | sed "s=src_vocab: =src_vocab: $SRC_VOCAB\n#=g" | sed "s=tgt_vocab: =tgt_vocab: $TGT_VOCAB\n#=g" > tmp.txt
#cp tmp.txt $CONFIG
#rm tmp.txt

DEVPRED="$LOGDIR""predictions.txt"

DEV=data/cleaned/neural/dev.src
DEVGOLD=data/cleaned/neural/dev.tgt


EVALSCRIPT="src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py"

SAVE_CONFIG="$LOGDIR""config_""$NAME""_""$CURDATE"".yaml"

#cp $CONFIG $LOGDIR"config_"$NAME"_"$CURDATE.yaml

.venv/bin/onmt_build_vocab -config $CONFIG -n_sample -1 \
    --src_vocab $SRC_VOCAB \
    --tgt_vocab $TGT_VOCAB \
#    --save_config $SAVE_CONFIG \
#    --log_file $TRAIN_LOG \
#    --save_model $SAVE_MODEL \

 .venv/bin/onmt_train --config $CONFIG \
     --log_file $TRAIN_LOG \
     --save_model $SAVE_MODEL \
     --src_vocab $SRC_VOCAB \
     --tgt_vocab $TGT_VOCAB
#     --save_config $SAVE_CONFIG \


# .venv/bin/onmt_translate -model $MODEL_PATH -src $DEV  -output $DEVPRED  -gpu 0 -verbose

# .venv/bin/python3 $EVALSCRIPT --name $NAME  --pred $DEVPRED --gold $DEVGOLD --logdir $LOGDIR
