#!/bin/bash


DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection

CONF=isTrainingIndependentOfEvalSet_DEV.yaml
MODEL=data/inner/onmt/run/model_is_training_independent_of_eval_set_DEV_step_25000.pt

DEV=data/cleaned/neural/dev_large.src
TEST=data/cleaned/neural/test.src

cd $DATADIR


.venv/bin/onmt_build_vocab -config $CONF -n_sample -1 

.venv/bin/onmt_train -config $CONF

CURDATE=$(date | sed "s/ /_/g")
.venv/bin/onmt_translate -model $MODEL -src $DEV  -output data/log/evaluate_models/onmt/is_training_indep_of_eval_set_DEV_on_DEV_$CURDATE.txt -gpu 0 -verbose
.venv/bin/onmt_translate -model $MODEL -src $TEST -output data/log/evaluate_models/onmt/is_training_indep_of_eval_set_DEV_on_TEST_$CURDATE.txt -gpu 0 -verbose

