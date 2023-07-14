#!/bin/bash

DEV="data/cleaned/neural/dev_small.src"

CONFIG="example.yaml"
DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection

EVALSCRIPT="src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py"

CURDATE=$(date | sed "s/ /_/g")

LOGS="data/log/evaluate_models/onmt/all_train_sizes_$CURDATE.txt"


cd $DATADIR



# cp $CONFIG configs/date/$CURDATE.yaml
#.venv/bin/onmt_build_vocab -config $CONFIG -n_sample -1 

#.venv/bin/onmt_train -config example.yaml


for trainsize in {1000..100000..1000}
do
	DESCRIPTION="OnmtModel_trainsteps_$trainsize"
	OUTPUT="data/log/evaluate_models/onmt/outputs/all/pred_$trainsize.$CURDATE.txt"

	.venv/bin/onmt_translate -model data/inner/onmt/run/model_step_$trainsize.pt -src $DEV -output $OUTPUT -gpu 0 -verbose

	.venv/bin/python3 $EVALSCRIPT --name $DESCRIPTION --pred $OUTPUT >> $LOGS
done
