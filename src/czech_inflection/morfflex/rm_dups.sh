#!/bin/bash

# Script for removal of duplicates using python script for duplicate removal.

pthscript=$1
tgtfile=$2

filename=$(basename "$tgtfile")

srcfile=data/processed/morfflex/splits_with_duplicates/$filename

cat $srcfile | python3 $pthscript > $tgtfile
