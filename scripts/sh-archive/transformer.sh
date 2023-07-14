#!/bin/bash

# Path to config file
CONFIG=configs/transformer.yaml

# Model
NAME="Transformer_v0.1_def"

#DATADIR=/storage/brno2/home/souradat/rp-sourada/czech-automatic-inflection
DATADIR=/storage/praha1/home/souradat/rp-sourada/czech-automatic-inflection

GENERAL_SCRIPT=$DATADIR/scripts/generalScript.sh

bash $GENERAL_SCRIPT $CONFIG $NAME