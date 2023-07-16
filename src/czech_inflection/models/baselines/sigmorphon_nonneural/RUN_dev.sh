#!/bin/bash

cd /storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection/src/czech_inflection/models/baselines/sigmorphon_nonneural/

#python3 baseline.py -o -p SMALL_DATA/
python3 quicker_baseline.py --path="../../../../../data/cleaned/sig_format/" --outpath="predictions/" --dev

