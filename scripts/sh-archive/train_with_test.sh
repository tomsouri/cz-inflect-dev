#!/bin/bash


DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection



cd $DATADIR

#.venv/bin/onmt_build_vocab -config train_with_test.yaml -n_sample -1 

#.venv/bin/onmt_train -config train_with_test.yaml

CURDATE=$(date | sed "s/ /_/g")

.venv/bin/onmt_translate -model data/inner/onmt/run/model_train_with_test_step_1250.pt -src data/cleaned/neural/dev_large.src -output data/log/evaluate_models/onmt/train_with_test_pred_dev_large_$CURDATE.txt -gpu 0 -verbose
.venv/bin/onmt_translate -model data/inner/onmt/run/model_train_with_test_step_1250.pt -src data/cleaned/neural/test.src -output data/log/evaluate_models/onmt/train_with_test_pred_test_$CURDATE.txt -gpu 0 -verbose

