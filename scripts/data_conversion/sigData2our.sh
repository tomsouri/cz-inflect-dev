#!/bin/bash

# The source sigmorphon data file.
SRC=$1

# The file to which write lemma+tag (src for our neural models)
LEMMATAG=$2

# The file to which write forms (tgt for our neural models)
FORM=$3

LEM=lemmata.tmp
#FORM=forms.tmp
TAG=tags.tmp

#  sed 's/   / <SPACE> /g' ensures that original space (in the new data represented by three consequent spaces) will be replaced by a special token for space <SPACE>
cat $SRC | cut -f 1 | python3 split2chars.py |  sed 's/   / <SPACE> /g' > $LEM

cat $SRC | cut -f 2 | python3 split2chars.py |  sed 's/   / <SPACE> /g' > $FORM

cat $SRC | cut -f 3 | sed 's/;/ /g' > $TAG

paste -d "#" $LEM $TAG | sed 's/#/ # /g' >  $LEMMATAG
