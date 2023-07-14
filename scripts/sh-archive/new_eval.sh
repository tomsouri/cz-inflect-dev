#!/bin/bash

DESCRIPTION="Transformer_v0.1"
#CONFIG="example.yaml"
DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection

cd $DATADIR

CURDATE=$(date | sed "s/ /_/g")
MODEL=data/inner/onmt/run/model_step_100000.pt
SRC=data/cleaned/neural/dev.src
TGT=data/log/evaluate_models/onmt/pred_100000_$CURDATE.txt
EVAL=src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py
DEVGOLD=data/cleaned/neural/dev.tgt

NEWTGT=data/log/evaluate_models/onmt/pred_100000_Thu_Mar_16_19:28:18_CET_2023.txt
#cp $CONFIG configs/date/$CURDATE.yaml
#.venv/bin/onmt_build_vocab -config $CONFIG -n_sample -1

#.venv/bin/onmt_train -config example.yaml

#.venv/bin/onmt_translate -model $MODEL -src $SRC -output $TGT -gpu 0 -verbose

.venv/bin/python3 $EVAL --name $DESCRIPTION --pred $NEWTGT --gold $DEVGOLD

#.venv/bin/python3 $EVALSCRIPT --name isTrainingIndepOfEvalSet_DEV2_on_DEV --pred $DEVPRED --gold $DEVGOLD
