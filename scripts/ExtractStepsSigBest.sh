#!/bin/bash

# Extract number of steps that are with the best dev accuracy.
steps=$(cat training_accs.txt | sed 's/ //g' | sed 's/0\./\t0\./g' | cut -f 1 | egrep "\!" | sed 's/\!\!//g'  | tail -n1)
echo "AHOJ$steps.txt"

