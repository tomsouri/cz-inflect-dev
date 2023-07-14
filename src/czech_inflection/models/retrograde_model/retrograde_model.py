#!/usr/bin/env python3.9

from __future__ import annotations
from datastructures.lemma import InflectedLemma
from models.retrograde_model.retrograde_trie import MorfFlexRetrogradeTrie
from models.model import ModelBase

from collections import Counter

UNKNOWN = "?"


def longest_common_suffix_len(a: str, b: str) -> int:
    """
    Finds the lenght of longest common suffix of two strings.

    Parameters:
        a(str), b(str): the string to find the common suffix of.

    Returns:
        int: the length of the longest common suffix

    Example: > longest_common_suffix_len(a="hrad", b="had")
    2
    (the longest common suffix is "ad", whose lenght is 2).
    """
    max_lenght = min(len(a), len(b))
    suf_len = 0
    for i in range(1, max_lenght + 1):
        if a[-i] == b[-i]:
            suf_len += 1
        else:
            break
    # suf = a[len(a)-suf_len:]
    return suf_len


def inflect_by_pattern(lemma: str, pattern: InflectedLemma) -> list[str]:
    """
    Inflect given lemma according to pattern with inflected forms.

    Parameters:
        lemma (str): the lemma string to be inflected
        pattern(InflectedLemma): the pattern lemma with all its inflected forms

    Returns:
        list[str]: All the inflected forms of the lemma, according to the
        pattern.

    Simplified explanation:  (Explains why it should be what we want, but
    does not work when the pattern stem is not present in some of the inflected
    forms.)

    Exact explanation: In each pattern inflected form, remove the prefix of the
    length of the pattern stem, and replace it with the lemma stem.

    Example 1: lemma: had, pattern: hrad.

    Longest common suffix: "ad". Pattern stem: "hr", lemma stem: "h"

    hr-ad   -> h-ad
    hr-adu  -> h-adu
    hr-adu  -> h-adu
    hr-ad   -> h-ad
    hr-ade  -> h-ade
    hr-adu  -> h-adu
    hr-adem -> h-adem
    ...

    Example 2: lemma: panák, pattern: domek

    Longest common suffix: "k". Pattern stem: "dome", lemma stem: "paná"

    dome-k  ->  paná-k
    domk-u  ->  paná-u
    domk-u  ->  paná-u
    dome-k  ->  paná-k
    domk-u  ->  paná-u
    domk-u  ->  paná-u
    domk-em ->  paná-em
    ...
    (Yes, this is not correct inflection. The reason is that the pattern has
    really short common suffix with the lemma.)
    """
    PRESERVE_UNKNOWN = True

    pattern_lemma = pattern.lemma
    suffix_len = longest_common_suffix_len(lemma, pattern_lemma)

    if suffix_len == 0:
        # If the common suffix length is 0, return copies of the lemma
        return [lemma] * len(pattern.inflected_forms)

    pattern_stem = pattern_lemma[:-suffix_len]
    stem = lemma[:-suffix_len]

    # kdyz ma pattern v inflected forms "?" jako unknown tvar:
    #               x dej tam misto snahy o vysklonovani proste lemma.
    #               - nebo spis vrat taky unknown tvar (deje se by default)
    inflected_forms = [
        stem + pattern_form[len(pattern_stem) :]
        for pattern_form in pattern.inflected_forms
    ]
    if PRESERVE_UNKNOWN:
        for i in range(len(inflected_forms)):
            if pattern.inflected_forms[i] == UNKNOWN:
                inflected_forms[i] = UNKNOWN

    return inflected_forms


def combine_predictions(predictions: list[list[str]]) -> list[str]:
    """
    Combine multiple predictions of inflected forms to one prediction.
    """

    def most_common(lst: list[str]) -> str:
        """
        Finds most common element of a given list.
        If it is UNKNOWN, try to return the second most common element.
        If there is no second most common element, return UNKNOWN.
        """
        most = Counter(lst).most_common(1)[0][0]
        ### If the most common is "?"", try to replace it with the second most common.
        if most == UNKNOWN:
            try:
                most = Counter(lst).most_common(2)[1][0]
            except:
                most = UNKNOWN
        ###
        return most

    combined = [
        most_common([predictions[j][i] for j in range(len(predictions))])
        for i in range(len(predictions[0]))
    ]
    return combined


class RetrogradeModel(ModelBase):
    @property
    def name(self) -> str:
        def __human_readable_count(count: int) -> str:
            """Converts count of data to human-readable form and return it as a
            string."""
            string_repre = str(count)

            if string_repre.endswith("000"):
                string_repre = string_repre[:-3] + "K"
            if string_repre.endswith("000K"):
                string_repre = string_repre[:-4] + "M"

            return string_repre

        string_repre = __human_readable_count(self._train_size)
        return (
            f"Retrograde[size={string_repre}][comb={self.number_to_combine}]"
        )

    def __init__(
        self,
        train_size: int = 360_000,
        inflect_by_pattern_method: callable[
            [str, InflectedLemma], InflectedLemma
        ] = inflect_by_pattern,
        number_to_combine: int = 131_072,
    ) -> None:
        self._train_size = train_size
        self._trie = MorfFlexRetrogradeTrie(train_size)
        self._inflect_by_pattern = inflect_by_pattern_method

        # the number of candidate patterns to choose at maximum
        self.number_to_combine = number_to_combine

    def inflect(self, lemma: str) -> list[str]:
        """
        Inflect the given lemma and return list of its inflected forms.

        Parameters:
            lemma(str): the lemma to be inflected

        Returns:
            list[str]: the inflected forms.
        """
        patterns = self._get_closest(lemma, max_count=self.number_to_combine)

        ###
        # patterns = list(patterns)
        # print("Patterns:")
        # print([p.lemma for p in patterns])
        # print("Inflections of patterns:")
        # print([p.inflected_forms for p in patterns])
        ###

        inflected_forms_lists = [
            self._inflect_by_pattern(lemma, pattern) for pattern in patterns
        ]

        ###
        # print("inflected_forms_list")
        # print(inflected_forms_lists)
        ###

        selected_forms = combine_predictions(inflected_forms_lists)

        ###
        # print("Selected forms before ? removal:")
        # print(selected_forms)
        # print("Selected forms after ? removal:")
        ###

        # Replace unknowns by lemma itself.
        # (protoze se acc pocita jen pres known)
        #
        # MAYBE DO NOT REMOVE UNKNOWN AND PRESERVE IT.
        final_forms = [
            form if form != "?" else lemma for form in selected_forms
        ]

        return final_forms

    def _get_closest(
        self, lemma: str, max_count: int = 100_000
    ) -> iter[InflectedLemma]:
        """
        Finds all closest lemmata (closest in retrograde meaning, with the
        longest common suffix) in the given trie and returns the iterator over
        first `max_count` of them.

        Parameters:
            lemma(str): the lemma for which the closest lemmata should be found
            trie(MorfFlexRetrogradeTrie): the trie in which we should seek for
                the lemmata
            max_count(int): the maximal count of yielded closest lemmata

        Returns:
            iter[InflectedLemma]: the iterator over closest lemmata
        """

        (suffix, lemmata) = self._trie.longest_common_suffix(lemma)

        counter = 0

        # To improve speed performance, if suffix=="", return only 1 "closest"
        # lemma To ensure that we will not inflect by 100k patterns
        # when there is no common suffix.
        max_count = max_count if suffix != "" else 1

        for lemma in lemmata:
            if counter >= max_count:
                break
            yield lemma
            counter += 1


# For direct usage.
if __name__ == "__main__":
    model = RetrogradeModel()
    while True:
        lemma = input("Enter lemma to be inflected: ")
        print(model.inflect(lemma))


