#!/usr/bin/env python3.9

from __future__ import annotations
from datastructures.lemma import InflectedLemma
from dev_testing.eval_models.accuracies import (
    check_form_prediction,
    lemma_per_lemma_acc,
)

#
# - docstrings, explain the working
questions = ["kdo/co", "bez", "ke/k", "vidím", "volám", "o", "s"] * 2
questions[7] = "ti/ty/ta"
questions = [f"({q})" for q in questions]


class ComparedLemma:
    def __init__(
        self, pred_lemma: InflectedLemma, gold_lemma: InflectedLemma
    ) -> None:
        self.lemma = gold_lemma.lemma
        self.gold_forms = gold_lemma.inflected_forms
        self.pred_forms = pred_lemma.inflected_forms

    def is_completely_correct(self):
        return 1 == lemma_per_lemma_acc(self.pred_forms, self.gold_forms)[0]

    def __str__(self):
        checked = [
            check_form_prediction(pred, gold)
            for (pred, gold) in zip(self.pred_forms, self.gold_forms)
        ]
        labels = [f"S{i}" for i in range(1, 8)] + [
            f"P{i}" for i in range(1, 8)
        ]
        result = f"Lemma: {self.lemma}" + "\n"
        for i in range(len(self.gold_forms)):
            if checked[i] is False:
                result += (
                    "\t"
                    + f"{labels[i]} "
                    + f"{questions[i]:<10}: "
                    + f"{self.pred_forms[i]:<15} "
                    + f"({self.gold_forms[i]})"
                    + "\n"
                )
        return result

    @staticmethod
    def multiple_to_str(compared_lemmata: list[ComparedLemma]) -> str:
        completely_correct_lemmata_count = sum(
            1 for lemma in compared_lemmata if lemma.is_completely_correct()
        )
        result = (
            "Completely correctly inflected lemmata:"
            + f"{completely_correct_lemmata_count}/{len(compared_lemmata)}"
            + "\n\n"
        )
        for lemma in compared_lemmata:
            if not lemma.is_completely_correct():
                result += str(lemma) + "\n"
        return result

    @staticmethod
    def multiple_to_fileholder(
        compared_lemmata: list[ComparedLemma], fileholder
    ) -> None:
        completely_correct_lemmata_count = sum(
            1 for lemma in compared_lemmata if lemma.is_completely_correct()
        )
        fileholder.write(
            "Completely correctly inflected lemmata:"
            + f"{completely_correct_lemmata_count}/{len(compared_lemmata)}"
            + "\n\n"
        )
        for lemma in compared_lemmata:
            if not lemma.is_completely_correct():
                fileholder.write(str(lemma) + "\n")
        return
