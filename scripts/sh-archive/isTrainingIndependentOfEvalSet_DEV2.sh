#!/bin/bash


DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection

CURDATE=$(date | sed "s/ /_/g")

CONF=isTrainingIndependentOfEvalSet_DEV2.yaml
MODEL=data/inner/onmt/run/model_is_training_independent_of_eval_set_DEV2_step_25000.pt
DEVPRED="data/log/evaluate_models/onmt/is_training_indep_of_eval_set_DEV2_on_DEV_$CURDATE.txt"
TESTPRED="data/log/evaluate_models/onmt/is_training_indep_of_eval_set_DEV2_on_TEST_$CURDATE.txt"



DEV=data/cleaned/neural/dev_large.src
TEST=data/cleaned/neural/test.src
DEVGOLD=data/cleaned/neural/dev_large.tgt
TESTGOLD=data/cleaned/neural/test.tgt


EVALSCRIPT="src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py"

cd $DATADIR


.venv/bin/onmt_build_vocab -config $CONF -n_sample -1 

.venv/bin/onmt_train -config $CONF

.venv/bin/onmt_translate -model $MODEL -src $DEV  -output $DEVPRED  -gpu 0 -verbose
.venv/bin/onmt_translate -model $MODEL -src $TEST -output $TESTPRED -gpu 0 -verbose

.venv/bin/python3 $EVALSCRIPT --name isTrainingIndepOfEvalSet_DEV2_on_DEV --pred $DEVPRED --gold $DEVGOLD

.venv/bin/python3 $EVALSCRIPT --name isTrainingIndepOfEvalSet_DEV2_on_TEST --pred $TESTPRED --gold $TESTGOLD
