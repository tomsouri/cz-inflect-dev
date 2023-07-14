#!/usr/bin/env python3

from __future__ import annotations
import re

from datastructures.lemma import InflectedLemma


def raw_lemma_from_lemma(lemma):
    """
    Extracts the raw lemma from the MorfFlex complex lemma, such as
    "Aaasenův_;Y_^(*2)"

    In MorfFlex, different meanings of same lemmas are distinguished and
    additional comments can be provided for every lemma meaning. The lemma
    itself without the comments and meaning specification is called a raw
    lemma. The following examples illustrate this:

    - Japonsko_;G (raw lemma: Japonsko)
    - se_^(zvr._zájmeno/částice) (raw lemma: se)
    - tvořit_:T (raw lemma: tvořit)
    (source: README in czech-morfflex-pdt-161115)
    """
    # for pattern in ["(\w)*", "[^_]*"]: groups = re.search(pattern, lemma)
    #    lemma = groups.group()

    pattern = "(\w)*"
    groups = re.search(pattern, lemma)
    lemma = groups.group()

    pattern = "[^_]*"
    groups = re.search(pattern, lemma)
    lemma = groups.group()

    raw_lemma = lemma
    return raw_lemma


def same_lemma_in(
    lemma: InflectedLemma, list_of_lemmata: list[InflectedLemma]
) -> bool:
    for infl_lemma in list_of_lemmata:
        if lemma.lemma == infl_lemma.lemma:
            return True
    return False
