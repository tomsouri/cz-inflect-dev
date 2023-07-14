#!/bin/bash

devdir=../../../../baselines/2022InflectionST/part1/development_languages
surpdir=../../../../baselines/2022InflectionST/part1/surprise_languages

tgtdir=../../data/cleaned/neural/sig22

#for lang in ang ara asm bra ckt evn gml goh got guj heb hsb hsi hun itl kat ket khk kor krl lud mag nds non pol poma sjo slk tur vep ;
for lang in ang ara asm evn got heb hun kat khk kor krl lud non pol poma slk tur vep ;
do
    dir=$devdir
    trainf=$dir/$lang"_large.train"
    devf=$dir/$lang.dev
    testf=$dir/$lang.gold
    
    outdir=$tgtdir/$lang
    mkdir -p $outdir
    
    bash sigData2our.sh $trainf $outdir/train.src $outdir/train.tgt
    
    bash sigData2our.sh $devf $outdir/dev.src $outdir/dev.tgt
    
    bash sigData2our.sh $testf $outdir/test.src $outdir/test.tgt ;
done

