#!/usr/bin/env python3.9

"""
Executable script to be run to test the models accuracy.
"""
from __future__ import annotations

import argparse

from dev_testing.eval_models.evaluate_model import evaluate_model
from dev_testing.eval_models.accuracies import (
    lemma_per_form_acc,
    lemma_per_lemma_acc,
)
from data import (
    get_dev_data,
    get_test_data,
    get_test_oov_data,
)

from math import inf

from dev_testing.eval_models.accuracies import method_descr

from config import create_log_dir
from config import LOG_EVAL_MODELS_DIR

from models.model import ModelBase
from models.hardcoded.sklonuj_cz import SklonujCzModel
from models.retrograde_model.retrograde_model import RetrogradeModel
from models.baselines.simple import SimpleBaseline


parser = argparse.ArgumentParser()
parser.add_argument(
    "--models",
    default="all",
    type=str,
    help="""The models to be tested, separated by semicolon ';'.
    To test all available models, enter 'all'.
    To run exhaustive test of the Retrograde model with different
    combination of parameters, enter 'retro-all'.""",
)
parser.add_argument(
    "--max_size",
    default=inf,
    type=int,
    help="Maximal number of lemmata in the test set.",
)

parser.add_argument(
    "--test",
    default=False,
    action="store_true",
    help="Test on all the dev, test and test-oov sets",
)


# Supported models:
# ONMT models not supported, they have to be run separately.
__MODELS_DICT = {
    "simple": SimpleBaseline,
    "sklonuj_cz": SklonujCzModel,
    "retrograde": RetrogradeModel,
}


def eval_and_print(
    model: ModelBase,
    log_dir_path: str,
    lemma_evaluation_methods,
    data_getting_methods,
):
    """
    Evaluate given model, log results and print the accuracies.
    """
    for data_getting_method in data_getting_methods:
        dataset = data_getting_method.__doc__.strip().split("\n")[0]
        log_model_file = log_dir_path + model.name + f".{dataset}.pred"
        log_gold_file = log_dir_path + f"gold.{dataset}.pred"
        log_res_file = log_dir_path + model.name + f".{dataset}.res"

        accs = evaluate_model(
            model=model,
            max_size=args.max_size,
            # For testing on large dev data or test or test-oov data, change
            # this argument to appropriate data getting method
            data_getting_method=data_getting_method,
            acc_methods=lemma_evaluation_methods,
            log_model_filename=log_model_file,
            log_gold_filename=log_gold_file,
            log_results_filename=log_res_file,
        )
        # Nice indent:
        # print(
        #    f"{model.name:<30}"
        #    + "".join(f"{f'{acc.value:.8f}':<30}" for acc in accs)
        # )
        # Tab indent:
        print(
            f"{model.name}"
            + "\t"
            + f"{dataset}"
            + "\t"
            + "\t".join(f"{acc.value:.8f}" for acc in accs)
        )


def main(args: argparse.Namespace) -> None:
    if args.models == "all":
        model_clss = __MODELS_DICT.values()
    elif args.models == "retro-all":
        model_clss = []
    else:
        model_clss = [
            __MODELS_DICT[model_name] for model_name in args.models.split(";")
        ]
    if args.test:
        data_getting_methods = [get_dev_data, get_test_data, get_test_oov_data]
    else:
        data_getting_methods = [get_dev_data]

    log_dir_path = create_log_dir(
        base_dir=LOG_EVAL_MODELS_DIR, descr=args.models
    )


    lemma_evaluation_methods = [lemma_per_form_acc, lemma_per_lemma_acc]

    # Nice indent:
    # print(
    #     f"{'Tested model':<30}" + f"{'dataset':<10}"
    #     + "".join(
    #         f"{method_descr(eval_method):<30}"
    #         for eval_method in lemma_evaluation_methods
    #     )
    # )

    # Tab indent:
    print(
        "Tested model"
        + "\t"
        + "dataset"
        + "\t"
        + "\t".join(
            f"{method_descr(eval_method)}"
            for eval_method in lemma_evaluation_methods
        )
    )

    if args.models == "retro-all":
        # Evaluate a lot of retrograde models
        train_sizes = [
            1,
            2,
            4,
            5,
            10,
            50,
            100,
            200,
            400,
            500,
            800,
            1_000,
            2_000,
            5_000,
            10_000,
            20_000,
            40_000,
            80_000,
            120_000,
            150_000,
            175_000,
            200_000,
            225_000,
            250_000,
            280_000,
            320_000,
            360_000,
        ]
        combine_counts = [
            1,
            2,
            4,
            8,
            16,
            32,
            64,
            128,
            256,
            512,
            1024,
            2048,
            4096,
            8192,
            16384,
            32768,
            65536,
            131072,
        ]
        for train_size in train_sizes:
            for combine_count in combine_counts:
                if combine_count > train_size:
                    continue

                model = RetrogradeModel(
                    train_size=train_size, number_to_combine=combine_count
                )
                eval_and_print(
                    model=model,
                    log_dir_path=log_dir_path,
                    lemma_evaluation_methods=lemma_evaluation_methods,
                    data_getting_methods=data_getting_methods,
                )

    for model_cls in model_clss:
        model = model_cls()
        eval_and_print(
            model=model,
            log_dir_path=log_dir_path,
            lemma_evaluation_methods=lemma_evaluation_methods,
            data_getting_methods=data_getting_methods,
        )

    return


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)
