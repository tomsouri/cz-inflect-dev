#!/usr/bin/env python3

from __future__ import annotations

from datastructures.lemma import InflectedLemma

def unzip(tuples_list: iter[tuple]) -> tuple[iter,iter]:
    return zip(*tuples_list)

def writelines(filename: str, lines: iter[str]):
    with open(filename, "w") as fout:
        for line in lines:
            fout.write(line + "\n")

def convert2neural_format(
    inflected_lemmata: iter[InflectedLemma],
    src_filename: str,
    tgt_filename: str):
    """ Converts the given list of inflected lemmata to 
    a format supported by neural networks and saves it to files."""

    lemma_tag_separator = "#"
    token_sep = " "

    tags_singular = [f"S{i}" for i in range(1, 8)]
    tags_plural = [f"P{i}" for i in range(1, 8)]
    tags = tags_singular + tags_plural

    src_string_list, tgt_string_list = unzip(
        (lemma.lemma + lemma_tag_separator + tags[i], lemma.inflected_forms[i])
        for lemma in inflected_lemmata for i in range(len(tags))
        )
    

    src_token_list = map(lambda x: token_sep.join(x),src_string_list)
    tgt_token_list = map(lambda x: token_sep.join(x),tgt_string_list)

    writelines(src_filename, src_token_list)
    writelines(tgt_filename, tgt_token_list)

def convert_from_neural_format(lemmata: iter[str], pred_filename) -> iter[InflectedLemma]:

    # tagy a token_sep na nekolika mistech hardcodovane
    tags_singular = [f"S{i}" for i in range(1, 8)]
    tags_plural = [f"P{i}" for i in range(1, 8)]
    tags = tags_singular + tags_plural

    token_sep = " "

    with open(pred_filename, "r") as preds:
        for lemma in lemmata:
            forms = []
            for _ in range(len(tags)):
                form = "".join(preds.readline().rstrip().split(token_sep))
                forms.append(form)
            yield InflectedLemma(lemma, forms)

def convert_from_neural_format(pred_filename) -> iter[InflectedLemma]:

    # tagy a token_sep na nekolika mistech hardcodovane
    tags_singular = [f"S{i}" for i in range(1, 8)]
    tags_plural = [f"P{i}" for i in range(1, 8)]
    tags = tags_singular + tags_plural

    token_sep = " "

    with open(pred_filename, "r") as preds:
        forms = []
        for line in preds:
            form = "".join(line.rstrip().split(token_sep))
            forms.append(form)
            if (len(forms) == len(tags)):
                yield InflectedLemma(forms[0], forms)
                forms = []

        # Use if you want inconsistent lemmata with insufficient number of
        # inflected forms:
        if (len(forms) != 0):
            print("WARNING: The last lemma does not contain full table of forms.")
            forms += ["?"] * (len(tags) - len(forms))
            yield InflectedLemma(forms[0], forms)

if __name__ == "__main__":
    from data import (
        get_train_data,
        get_dev_data, 
        get_test_data, 
        get_test_oov_data
    )
    from config import (
        NEURAL_TRAIN_SRC,
        NEURAL_TRAIN_TGT,
        NEURAL_DEV_SRC,
        NEURAL_DEV_TGT,
        NEURAL_TEST_SRC,
        NEURAL_TEST_TGT,
        NEURAL_TEST_OOV_SRC,
        NEURAL_TEST_OOV_TGT
    )
    for data_method, src_file, tgt_file in zip(
        [get_train_data, get_dev_data, get_test_data, get_test_oov_data], 
        [NEURAL_TRAIN_SRC, NEURAL_DEV_SRC, NEURAL_TEST_SRC, NEURAL_TEST_OOV_SRC],
        [NEURAL_TRAIN_TGT, NEURAL_DEV_TGT, NEURAL_TEST_TGT, NEURAL_TEST_OOV_TGT]
        ):
        convert2neural_format(data_method(), src_file, tgt_file)
