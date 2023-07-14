#!/usr/bin/env python3.9

"""
Provides global configurations, such as absolute paths to data.
"""

import os
import datetime, re
from pathlib import Path

def removesuffix(str, suf):
    return str[:-len(suf)]

def __get_data_dir():
    suffix = "src/czech_inflection/config.py"

    # Get name of this `config.py` script
    file_path = os.path.realpath(__file__)

    base_dir = removesuffix(file_path, suffix)
    #base_dir = file_path.removesuffix(suffix)

    data_dir = base_dir + "data/"
    return data_dir, base_dir

HYPERPARAMS_DIARY="docs/hyperparams.txt"

DATA_DIR, BASE_DIR = __get_data_dir()

__RAW_DIR = DATA_DIR + "raw/"
__PROCESSED_DIR = DATA_DIR + "processed/"
__CLEANED_DIR = DATA_DIR + "cleaned/"
__LOG_DIR = DATA_DIR + "log/"
__INNER_DIR = DATA_DIR + "inner/"

__CESTINA20_DIR = __RAW_DIR + "cestina20/"
CESTINA20FILES = [
    __CESTINA20_DIR + filename
    for filename in ("pismeno-j.csv", "pismeno-e.csv")
]

LOG_DEV_BUILDING_DIR = __LOG_DIR + "building_dev_data/"
LOG_EVAL_MODELS_DIR = __LOG_DIR + "evaluate_models/"

TEST_OOV_MANUALLY_CHECKED_FILE = __PROCESSED_DIR + "dev_data_manual_check.txt"

__DUPLICATES_DIR = __PROCESSED_DIR + "morfflex/splits_with_duplicates/"
TRAIN_DUP_FILE = __DUPLICATES_DIR + "train_data.txt"
DEV_DUP_FILE = __DUPLICATES_DIR + "dev_data.txt"
TEST_DUP_FILE = __DUPLICATES_DIR + "test_data.txt"



TRAIN_DATA_FILE = __CLEANED_DIR + "train_data.txt"
DEV_DATA_FILE = __CLEANED_DIR + "dev_data.txt"
#DEV_DATA_FILE = __CLEANED_DIR + "dev_data.txt"
#DEV_DATA_LARGE_FILE = __CLEANED_DIR + "dev_large_data.txt"
TEST_DATA_FILE = __CLEANED_DIR + "test_data.txt"
TEST_OOV_DATA_FILE = __CLEANED_DIR + "test_oov_data.txt"

__NEURAL_DIR = __CLEANED_DIR + "neural/"
NEURAL_TRAIN_SRC = __NEURAL_DIR + "train.src"
NEURAL_TRAIN_TGT = __NEURAL_DIR + "train.tgt"
NEURAL_DEV_SRC = __NEURAL_DIR + "dev.src"
NEURAL_DEV_TGT = __NEURAL_DIR + "dev.tgt"
#NEURAL_DEV_LARGE_SRC = __NEURAL_DIR + "dev_large.src"
#NEURAL_DEV_LARGE_TGT = __NEURAL_DIR + "dev_large.tgt"
NEURAL_TEST_SRC = __NEURAL_DIR + "test.src"
NEURAL_TEST_TGT = __NEURAL_DIR + "test.tgt"
NEURAL_TEST_OOV_SRC = __NEURAL_DIR + "test-oov.src"
NEURAL_TEST_OOV_TGT = __NEURAL_DIR + "test-oov.tgt"


MORFFLEX_LEMMATA = __PROCESSED_DIR + "morfflex/morfflex-lemmata-only.txt"
__MORFFLEX_WHOLE = __RAW_DIR + "czech-morfflex-2.0.tsv"
__MORFFLEX_NOUNS = __PROCESSED_DIR + "morfflex/morfflex-nouns.tsv"
__MORFFLEX_NOUNS_SHUFFLED = (
    __PROCESSED_DIR + "morfflex/morfflex-nouns-shuffled.tsv"
)

FILTERED_DATA_FULL = __PROCESSED_DIR + "morfflex/filtered_data_full.txt"

# Choose appropriate morfflex raw file:
MORFFLEX_RAW = __MORFFLEX_NOUNS_SHUFFLED

MORFFLEX_TRIE_PICKLED_DIR = __INNER_DIR + "trie/"

MORFFLEX_COLUMN_SEPARATOR = "\t"


SKLONUJ_CZ_PHP = __INNER_DIR + "sklonuj_cz.php"

SEED = 42


def create_log_dir(base_dir: str, descr: str = "") -> str:
    """
    Creates a directory for logs inside the `base_dir` directory and returns
    the path to it.

    Parameters:
        base_dir (str): the directory inside which the new directory should be
        created. descr (str): Additional short description of the directory.
    """
    name = str(datetime.datetime.now()).replace(" ", "_")
    name = re.sub("\.\d*", "-" + descr, name)
    dir_path = base_dir + name + "/"
    path = Path(dir_path)
    path.mkdir(exist_ok=True)
    # os.mkdir(dir_path)
    return dir_path
