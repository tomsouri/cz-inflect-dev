#!/usr/bin/env python3

from __future__ import annotations

from morfflex.transform_morfflex import raw_lemma_from_lemma
from datastructures.lemma import InflectedLemma

from config import (
    FILTERED_DATA_FULL,
    TRAIN_DUP_FILE,
    DEV_DUP_FILE,
    TEST_DUP_FILE
)

def build_train_dev_test_split_data(
    train_tgt: str = TRAIN_DUP_FILE, 
    dev_tgt: str = DEV_DUP_FILE, 
    test_tgt: str = TEST_DUP_FILE
    ) -> None:
    """
    Loads the whole available data, splits it to the train, dev and test parts
    and saves them to given files.

    Expects the `__load_filtered_data` method to return Inflected lemmata in a
    shuffled order, however, when they have the same raw lemma, they should
    appear consecutively. Otherwise, the zero-size intersection of the train
    and the dev set (and the zero-size intersection of the train and the test
    set) is not guaranteed.
    """
    print("Building the train, dev and test data...")

    # vzhledem k tomu, ze tahle metoda uz mi vraci lemmata shufflovana, muzu
    # tady proste vzit prvnich X jako test, dalsich X jako dev a pak nejakych Y
    # jako train.
    
    #TADY
    lemmata = list(__load_filtered_data())

    test_count = 44_000
    dev_count = test_count
    train_count = 360_000

    # THIS iwould not be sufficient, because it could happen that there are two
    # lemmata with the same raw lemma on the border of the sets
    
    #test_lemmata = lemmata[:test_count] dev_lemmata =
    #lemmata[test_count:test_count + dev_count] train_lemmata =
    #lemmata[test_count + dev_count : test_count + dev_count + train_count]


    train_lemmata = []
    dev_lemmata = []
#    dev_large_lemmata = []
    test_lemmata = []

    i = 0
    while i<test_count:
        test_lemmata.append(lemmata[i])
        i += 1
    last_raw_lemma = raw_lemma_from_lemma(test_lemmata[-1].lemma)
    
    # Skip lemmata that are equal to the last lemma
    while (raw_lemma_from_lemma(lemmata[i].lemma) == last_raw_lemma):
        i+=1

    new_end_index = i+dev_count
    while i<new_end_index:
        dev_lemmata.append(lemmata[i])
        i += 1
    last_raw_lemma = raw_lemma_from_lemma(dev_lemmata[-1].lemma)

    # Skip lemmata that are equal to the last lemma
    while (raw_lemma_from_lemma(lemmata[i].lemma) == last_raw_lemma):
        i+=1
    
    new_end_index = i+train_count
    while i<new_end_index:
        train_lemmata.append(lemmata[i])
        i += 1

    InflectedLemma.multiple_to_file(lemmata=train_lemmata, filename=train_tgt)
    InflectedLemma.multiple_to_file(lemmata=dev_lemmata, filename=dev_tgt)
    InflectedLemma.multiple_to_file(lemmata=test_lemmata, filename=test_tgt)


def __load_filtered_data() -> iter[InflectedLemma]:
    return InflectedLemma.multiple_from_file(FILTERED_DATA_FULL)

if __name__ == "__main__":
    build_train_dev_test_split_data()