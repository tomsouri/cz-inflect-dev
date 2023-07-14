#!/usr/bin/bash

DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

cd $DATADIR

PYTHON=.venv/bin/python3

EVAL=src/czech_inflection/dev_testing/eval_models/main.py

$PYTHON $EVAL
