#!/usr/bin/env python3.9

from __future__ import annotations
from collections import namedtuple
from dev_testing.eval_models.compared_lemma import ComparedLemma
from models.model import ModelBase
from datastructures.lemma import InflectedLemma
import dev_testing.eval_models.accuracies as accuracies

from data import get_dev_data

Accuracy = namedtuple("Accuracy", ("value", "description"))


def evaluate_model(
    model: ModelBase,
    max_size: int = 10000,
    data_getting_method: callable[int, list[InflectedLemma]] = get_dev_data,
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
    gold = data_getting_method(max_size)

    gold = list(gold)

    lemmata = [x.lemma for x in gold]

    # Predict:
    pred_forms_only = [model.inflect(lemma) for lemma in lemmata]

    # Convert predicted forms to InflectedLemmata
    pred = [
        InflectedLemma(lemma, forms)
        for (lemma, forms) in zip(lemmata, pred_forms_only)
    ]
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
            model_name=model.name,
            accs=accs,
            compared_lemmata=compared_lemmata,
            filename=log_results_filename,
        )

    return accs


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
    # TODO: add more information, such as speed of prediction etc.
    with open(filename, "w") as fileholder:
        strings_to_print = [
            model_name,
            "\n\n",
            f"Eval_data size: {len(compared_lemmata)} lemmata",
            "\n\n",
            "\n".join(f"{acc.description:<45}{acc.value:.8f}" for acc in accs),
            "\n\n",
        ]

        for string_to_print in strings_to_print:
            fileholder.write(string_to_print)

        ComparedLemma.multiple_to_fileholder(compared_lemmata, fileholder)

    return
