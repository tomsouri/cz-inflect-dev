#!/usr/bin/env python3.9

# example call: .venv/bin/python3
# src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py --name
# "First onmt model" --pred data/log/evaluate_models/onmt/EXAMPLE_FILE.txt

from __future__ import annotations
from collections import namedtuple
from dev_testing.eval_models.compared_lemma import ComparedLemma

# from models.model import ModelBase
from datastructures.lemma import InflectedLemma

from morfflex.convert2neural import convert_from_neural_format

from math import inf

import dev_testing.eval_models.accuracies as accuracies
import argparse

from config import create_log_dir, LOG_EVAL_MODELS_DIR, HYPERPARAMS_DIARY

# from data import get_dev_data, get_test_data

parser = argparse.ArgumentParser()
# parser.add_argument( "--small", default=True, action="store_true",
#     help="""Small dev set is used.""", )
parser.add_argument(
    "--pred",
    default="unknown_file.pred",
    type=str,
    help="The file containg the predictions of the model",
)

parser.add_argument(
    "--gold",
    default=None,
    type=str,
    help="The file containg the gold predictions",
)
parser.add_argument(
    "--name",
    default="UnknownOnmtModel",
    type=str,
    help="Description of the model",
)
parser.add_argument(
    "--logdir",
    default=None,
    type=str,
    help="Directory to print logs",
)
parser.add_argument(
    "--train_steps",
    default="x",
    type=str,
    help="Number of train steps",
)
parser.add_argument(
    "--max_size",
    default=inf,
    type=int,
    help="Maximal number of lemmata in the test set.",
)


Accuracy = namedtuple("Accuracy", ("value", "description"))


def evaluate_model(
    model_name: str,
    pred_filename: str,
    gold_filename: str,
    log_model_filename: str = None,
    log_gold_filename: str = None,
    log_results_filename: str = None,
    acc_methods: list[callable[[InflectedLemma, InflectedLemma], float]] = [
        accuracies.lemma_per_form_acc,
        accuracies.lemma_per_lemma_acc,
    ],
) -> list[Accuracy]:
    """
    Evaluates the model on the development/test/test-oov data.

    Computes two different accuracies (by default).

    Parameters: model (ModelBase): The model to be tested. max_size (int):
    Maximal count of lemmata in the evaluation set. log_model_filename (str):
    The file, where print the model logs (predicted inflected forms). If None
    (default), doesn't print it. log_gold_filename (str): The file, where print
    the gold logs (gold inflected forms). If None (default), doesn't print it.
    log_results_filename (str): The file, where print the results (computed
    accuracies and another info). If None (default), doesn't print it. #
    lemma_evaluations (list[callable]): All functions, that should be used to
    compute accuracies.

    Returns: list[Accuracy]: For each given function in `lemma_evaluations`, an
    instance of Accuracy:
        value (float): the computed accuracy description (str): the description
        of the accuracy computation method.
    """
    gold = convert_from_neural_format(pred_filename=gold_filename)
    gold = list(gold)

    # Predict: pred_forms_only = [model.inflect(lemma) for lemma in lemmata]

    # Convert predicted forms to InflectedLemmata pred = [
    # InflectedLemma(lemma, forms) for (lemma, forms) in zip(lemmata,
    #    pred_forms_only) ]

    pred = convert_from_neural_format(pred_filename=pred_filename)
    pred = list(pred)

    # Check whether the number of predictions and gold lemmata is the same.
    if len(pred) != len(gold):
        print(
            "WARNING: The number of predicted lemmata differs from the number of gold lemmata."
        )
        print("Setting accuracy to 0.")
        accs = [
            Accuracy(
                value=0,
                description=accuracies.method_descr(acc_method),
            )
            for acc_method in acc_methods
        ]
        return accs

    accs = [
        Accuracy(
            value=accuracies.all_lemmata_accuracy(pred, gold, acc_method),
            description=accuracies.method_descr(acc_method),
        )
        for acc_method in acc_methods
    ]

    compared_lemmata = [ComparedLemma(p, g) for (p, g) in zip(pred, gold)]

    # logovani
    if log_model_filename is not None:
        __log_data(data=pred, filename=log_model_filename)
    if log_gold_filename is not None:
        __log_data(data=gold, filename=log_gold_filename)
    if log_results_filename is not None:
        __log_results(
            model_name=model_name,
            accs=accs,
            compared_lemmata=compared_lemmata,
            filename=log_results_filename,
        )

    return accs


# def evaluate_model_on_dev_data( model_name: str, pred_filename: str,
#     max_size: int = 10000, data_getting_method: callable[int,
#     list[InflectedLemma]] = get_dev_data, log_model_filename: str = None,
#     log_gold_filename: str = None, log_results_filename: str = None,
#     acc_methods: list[callable[[InflectedLemma, InflectedLemma], float]] =
#     [accuracies.lemma_per_form_acc, accuracies.lemma_per_lemma_acc] ) ->
#     list[Accuracy]: """ Evaluates the model on the development/test/test-oov
#     data.

#     Computes two different accuracies (by default).

#     Parameters: model (ModelBase): The model to be tested. max_size (int):
#     Maximal count of lemmata in the evaluation set. log_model_filename (str):
#     The file, where print the model logs (predicted inflected forms). If None
#     (default), doesn't print it. log_gold_filename (str): The file, where
#     print the gold logs (gold inflected forms). If None (default), doesn't
#     print it. log_results_filename (str): The file, where print the results
#     (computed accuracies and another info). If None (default), doesn't print
#     it. # lemma_evaluations (list[callable]): All functions, that should be
#     used to compute accuracies.

#     Returns: list[Accuracy]: For each given function in `lemma_evaluations`,
#     an instance of Accuracy: value (float): the computed accuracy description
#         (str): the description of the accuracy computation method. """ gold =
#         data_getting_method(max_size) lemmata = [x.lemma for x in gold]

#     # Predict:
#     #pred_forms_only = [model.inflect(lemma) for lemma in lemmata]

#     # Convert predicted forms to InflectedLemmata
#     #pred = [
#     #    InflectedLemma(lemma, forms)
#     #    for (lemma, forms) in zip(lemmata, pred_forms_only)
#     #]

#     pred = convert_from_neural_format(lemmata=lemmata,
#     pred_filename=pred_filename) pred = list(pred)

#     accs = [ Accuracy( value=accuracies.all_lemmata_accuracy(pred, gold,
#         acc_method), description=accuracies.method_descr(acc_method), ) for
#             acc_method in acc_methods ]

#     compared_lemmata = [ComparedLemma(p, g) for (p, g) in zip(pred, gold)]

#     # logovani
#     if log_model_filename is not None: __log_data(data=pred,
#         filename=log_model_filename) if log_gold_filename is not None:
#     __log_data(data=gold, filename=log_gold_filename) if log_results_filename
#         is not None: __log_results( model_name=model_name, accs=accs,
#     compared_lemmata=compared_lemmata, filename=log_results_filename, )

#     return accs


def __log_data(data: list[InflectedLemma], filename: str) -> None:
    """
    Logs the given predicted/gold data to given file.
    """
    with open(filename, "w") as f:
        f.write("\n\n".join(lemma.pretty_repr() for lemma in data))


def __log_results(
    model_name: str,
    accs: list[Accuracy],
    compared_lemmata: list[ComparedLemma],
    filename: str,
) -> None:
    """
    Logs the results of predictions with accuracies and compared lemmata to
    given file.
    """
    with open(filename, "w") as fileholder:
        strings_to_print = [
            model_name,
            "\n\n",
            f"Eval_data size: {len(compared_lemmata)} lemmata",
            "\n\n",
            "\n".join(f"{acc.description:<45}{acc.value:.8f}" for acc in accs),
            "\n\n",
            # The following is removed because it was not correct (unknown
            # forms are not counted to form-acc) "Correctly inflected forms: ",
            # f"{int(accs[0].value * 14 * len(compared_lemmata))}/{14 *
            # len(compared_lemmata)}",
            "\n\n",
        ]

        for string_to_print in strings_to_print:
            fileholder.write(string_to_print)

        ComparedLemma.multiple_to_fileholder(compared_lemmata, fileholder)

    return


def main(args):

    log_dir_path = (
        args.logdir
        if args.logdir is not None
        else create_log_dir(base_dir=LOG_EVAL_MODELS_DIR, descr=args.name)
    )

    log_model_file = log_dir_path + args.name + ".pred"
    log_gold_file = log_dir_path + "gold.pred"
    log_res_file = log_dir_path + args.name + ".res"

    accs = evaluate_model(
        model_name=args.name,
        pred_filename=args.pred,
        gold_filename=args.gold,
        # max_size=args.max_size, data_getting_method=get_dev_data,
        # acc_methods=lemma_evaluation_methods,
        log_model_filename=log_model_file,
        log_gold_filename=log_gold_file,
        log_results_filename=log_res_file,
    )

    print(
        f"{args.name:<30}"
        + "".join(f"{f'{acc.value:.8f}':<30}" for acc in accs)
    )

    # Write results to hyperparams diary.

    from datetime import datetime

    # date = datetime.today().strftime('%Y-%m-%d')
    date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    train_steps = args.train_steps
    if train_steps[-3:] == "000":
        train_steps = train_steps[:-3] + "k"

    output = (
        f"{args.name:<65} & {train_steps:<7} & {date} & "
        + " & ".join(f"{f'{acc.value:.8f}':<15}" for acc in accs)
        + "\n"
    )

    with open(HYPERPARAMS_DIARY, "a") as f:
        f.write(output)

    print("The results were written to the files:")
    print(log_model_file)
    print(log_gold_file)
    print(log_res_file)


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)
