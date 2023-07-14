#!/bin/bash

DESCRIPTION="OnmtModelInProcess"
CONFIG="example.yaml"
DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection

cd $DATADIR

CURDATE=$(date | sed "s/ /_/g")

cp $CONFIG configs/date/$CURDATE.yaml
#.venv/bin/onmt_build_vocab -config $CONFIG -n_sample -1 

#.venv/bin/onmt_train -config example.yaml

.venv/bin/onmt_translate -model data/inner/onmt/run/model_step_100000.pt -src data/cleaned/neural/dev_small.src -output data/log/evaluate_models/onmt/pred_100000_$CURDATE.txt -gpu 0 -verbose

.venv/bin/python3 src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py --name $DESCRIPTION --pred data/log/evaluate_models/onmt/pred_100000_$CURDATE.txt
