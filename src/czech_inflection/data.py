#!/usr/bin/env python3.9

from __future__ import annotations
import os
from math import inf

from datastructures.lemma import InflectedLemma
from dev_testing.build_data.build_test_oov_data import build_test_oov_data
from morfflex.train_dev_test_split import build_train_dev_test_split_data
from config import (
    TRAIN_DATA_FILE, 
    DEV_DATA_FILE, 
#    DEV_DATA_LARGE_FILE, 
    TEST_DATA_FILE, 
    TEST_OOV_DATA_FILE
)

def get_test_oov_data(max_size: int = inf) -> list[InflectedLemma]:
    """test-oov
    Returns list of test-oov data.
    """
    if not os.path.exists(TEST_OOV_DATA_FILE):
        build_test_oov_data(tgt=TEST_OOV_DATA_FILE)

    return list(
        __get_data(
            filename=TEST_OOV_DATA_FILE,
            max_size=max_size,
        )
    )

def get_test_data(max_size: int = inf) -> list[InflectedLemma]:
    """test
    Returns list of test data.
    """
    if not os.path.exists(TEST_DATA_FILE):
        build_train_dev_test_split_data(
            test_tgt=TEST_DATA_FILE
            )
    return list(
        __get_data(
            filename=TEST_DATA_FILE,
            max_size=max_size,
        )
    )

def get_dev_data(max_size: int = inf) -> list[InflectedLemma]:
    """dev
    Returns list of dev data.
    """
    if not os.path.exists(DEV_DATA_FILE):
        build_train_dev_test_split_data(
            dev_tgt=DEV_DATA_FILE
            )
    return list(
        __get_data(
            filename=DEV_DATA_FILE,
            max_size=max_size,
        )
    )




def get_train_data(max_size: int = inf) -> iter[InflectedLemma]:
    """train
    Returns iterator over train data.
    """
    if not os.path.exists(TRAIN_DATA_FILE):
        build_train_dev_test_split_data(
            train_tgt=TRAIN_DATA_FILE
            )
    return __get_data(
        filename=TRAIN_DATA_FILE,
        max_size=max_size,
    )


def __get_data(
    filename: str,  max_size: int = inf
) -> iter[InflectedLemma]:

    counter = 0
    for lemma in InflectedLemma.multiple_from_file(filename):
        if counter >= max_size:
            break
        yield lemma
        counter += 1