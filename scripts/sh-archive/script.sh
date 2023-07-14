#!/bin/bash


DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection



cd $DATADIR

.venv/bin/onmt_build_vocab -config example.yaml -n_sample -1 

.venv/bin/onmt_train -config example.yaml

CURDATE=$(date | sed "s/ /_/g")

.venv/bin/onmt_translate -model data/inner/onmt/run/model_step_3000.pt -src data/cleaned/neural/dev_small.src -output data/log/evaluate_models/onmt/pred_1000_$CURDATE.txt -gpu 0 -verbose
