#!/usr/bin/env python3.9

from __future__ import annotations

def check_form_prediction(pred: str, gold: str) -> bool:
    if gold == "?":
        return None
    return set(pred.split("/")) <= set(gold.split("/"))


def lemma_per_form_acc(
    pred_forms: list[str], gold_forms: list[str]
) -> tuple[float, float]:
    """Form accuracy
    Computes form accuracy for """
    checked = [
        check_form_prediction(pred, gold)
        for (pred, gold) in zip(pred_forms, gold_forms)
    ]
    value = sum(1 for form_result in checked if form_result) / 14
    weight = sum(1 for form_result in checked if form_result is not None) / 14
    return (value, weight)


def lemma_per_lemma_acc(
    pred_forms: list[str], gold_forms: list[str]
) -> tuple[float, float]:
    """Full-paradigm accuracy
    Acc. per lemma (all forms must be correct)."""
    checked = [
        check_form_prediction(pred, gold)
        for (pred, gold) in zip(pred_forms, gold_forms)
    ]
    value = 1 if set(checked) <= {True, None} else 0
    weight = 1
    return (value, weight)


def all_lemmata_accuracy(pred_lemmata, gold_lemmata, lemma_acc):
    """
    Compute a specific accuracy for list of predicted lemmata.
    """
    values, weights = [], []
    for pred, gold in zip(pred_lemmata, gold_lemmata):
        value, weight = lemma_acc(pred.inflected_forms, gold.inflected_forms)
        values.append(value)
        weights.append(weight)
    weights_sum = sum(weights)
    total_weights = weights_sum if weights_sum != 0 else 1
    return sum(values) / total_weights


def method_descr(method: callable) -> str:
    """
    Extracts the first line of the method docstring.
    """
    return method.__doc__.strip().split("\n")[0]
