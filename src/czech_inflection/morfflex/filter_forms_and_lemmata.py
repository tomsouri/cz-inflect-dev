#!/usr/bin/env python3

from __future__ import annotations

from morfflex.transform_morfflex import raw_lemma_from_lemma
from datastructures.lemma import InflectedLemma

from config import MORFFLEX_RAW, MORFFLEX_COLUMN_SEPARATOR
from config import (
    FILTERED_DATA_FULL,
)


def count_forms(lemmata: iter[InflectedLemmaFormsDict]):
    counter = 0
    for lemma_form_dict in lemmata:
        counter += lemma_form_dict.count_forms()
    return counter

# filter_lemmata_and_forms
def __filter_lemmata_and_forms() -> iter[InflectedLemma]:
    """
    Reads the raw morfflex file and turns it to iterator over InflectedLemmata.
    The raw morfflex file should contain randomly shuffled rows, but the rows
    containing the same lemma (or the same raw lemma) should appear
    consecutively. If 2 lemmata have the same raw lemma, they appear
    consecutively in the result.
    """
    # Lemmata with all forms from morfflex
    lemmata = __load_lemmata_with_all_forms(MORFFLEX_RAW)

    lemmata = list(lemmata)
    descr="All nouns shuffled"
    print(f"{descr}:\t{len(lemmata)}\t{count_forms(lemmata)}")

    # Convert complex_lemma to raw_lemma
    lemmata = (__lemma_complex_to_raw(lemma) for lemma in lemmata)

    lemmata = list(lemmata)
    descr="Complex lemma to raw lemma"
    print(f"{descr}:\t{len(lemmata)}\t{count_forms(lemmata)}")

    # Lemmata with selected basic forms
    lemmata = __apply_tag_selector(
        lemmata, tag_selector=lambda tag: tag[-1] == "-"
    )

    lemmata = list(lemmata)
    descr="Basic forms only"
    print(f"{descr}:\t{len(lemmata)}\t{count_forms(lemmata)}")


    # Remove negation forms
    lemmata = __apply_tag_selector(
        lemmata, tag_selector=lambda tag: tag[10] != "N"
    )

    lemmata = list(lemmata)
    descr="Removed negations"
    print(f"{descr}:\t{len(lemmata)}\t{count_forms(lemmata)}")

    # Simplify tags to contain only number and case flags.
    lemmata = (__simplify_tags(lemma) for lemma in lemmata)

    lemmata = list(lemmata)
    descr="Simplified tags"
    print(f"{descr}:\t{len(lemmata)}\t{count_forms(lemmata)}")

    # Define allowed tags sets:
    tags_singular = [f"S{i}" for i in range(1, 8)]
    tags_plural = [f"P{i}" for i in range(1, 8)]
    tags = tags_singular + tags_plural

    taglists = [[], ["XX"], ["XX", "S1"], tags_singular, tags_plural, tags]
    tagsets = [set(taglist) for taglist in taglists]

    tags_set = set(tags)

    # Removed lemmata with strange tag set
    lemmata = filter(
        lambda lemma: (set(lemma.inflected_forms) in tagsets), lemmata
    )

    lemmata = list(lemmata)
    descr="Removed lemmata with strange tag set"
    print(f"{descr}:\t{len(lemmata)}\t{count_forms(lemmata)}")

    # Complete tags and forms to the count of 14
    lemmata = (__complete_tags(lemma, tags=tags_set) for lemma in lemmata)

    lemmata = list(lemmata)
    descr="Completed incomplete paradigm tables"
    print(f"{descr}:\t{len(lemmata)}\t{count_forms(lemmata)}")

    # Convert dict{tag:form} to list[form]
    lemmata = (
        InflectedLemma(
            lemma.lemma, [lemma.inflected_forms[tag] for tag in tags]
        )
        for lemma in lemmata
    )


    lemmata = list(lemmata)
    descr="Filtered inflected lemmata"
    print(f"{descr}:\t{len(lemmata)}\t{14 * len(lemmata)}")

    InflectedLemma.multiple_to_file(lemmata, FILTERED_DATA_FULL)

# morfflex2formdict
def __load_lemmata_with_all_forms(
    filename: str,
) -> iter[InflectedLemmaFormsDict]:
    """
    Read raw morfflex and extract every lemma with a dict {tag: form}.
    """
    with open(filename, "r") as f:
        last_lemma = ""
        last_inflected_lemma = None
        counter = 0
        for line in f:
            line = line.rstrip()
            tokens = line.split(MORFFLEX_COLUMN_SEPARATOR)
            (lemma, tag, form) = tuple(tokens)

            if lemma != last_lemma:
                if (
                    counter != 0
                ):
                    # Ensure that None will not be yielded at the beginning
                    yield last_inflected_lemma

                last_lemma = lemma
                last_inflected_lemma = InflectedLemmaFormsDict(lemma, {})
                counter += 1

            last_inflected_lemma.inflected_forms[tag] = form

        # This should be here, because without it we are missing the last
        # lemma. However, it is not a big deal. if
        # last_inflected_lemma.inflected_forms != {}: yield
        #     last_inflected_lemma



def __apply_tag_selector(
    lemmata: iter[InflectedLemmaFormsDict], tag_selector: callable[[str], bool]
) -> iter[InflectedLemmaFormsDict]:
    modifier = lambda lemma: __select_tags(lemma, tag_selector)
    return (modifier(lemma) for lemma in lemmata)



def __simplify_tags(lemma: InflectedLemmaFormsDict) -> InflectedLemmaFormsDict:
    """
    Simplify tags in the given lemma to contain only number and case flags.
    """

    def simplify_tags_in_dict(forms: dict[str, str]) -> dict[str, str]:
        old_tags = list(forms.keys())

        def simplify(tag: str) -> str:
            return tag[3:5]

        for old_tag in old_tags:
            forms[simplify(old_tag)] = forms[old_tag]
            del forms[old_tag]
        return forms

    lemma.inflected_forms = simplify_tags_in_dict(lemma.inflected_forms)
    return lemma


def __complete_tags(
    lemma: InflectedLemmaFormsDict, tags: set[str]
) -> InflectedLemmaFormsDict:
    def complete_tags_in_dict(
        lemma: str, forms: dict[str, str], tags: set[str]
    ) -> dict[str, str]:
        old_tags = list(forms.keys())
        count = len(old_tags)
        if count == 0:
            default_value = lemma
            for tag in tags:
                forms[tag] = default_value
        if count == 1:
            old_tag = old_tags[0]
            default_value = forms[old_tag]
            del forms[old_tag]
            for tag in tags:
                forms[tag] = default_value
        if count == 2:
            default_value = forms["XX"]
            for old_tag in old_tags:
                del forms[old_tag]
            for tag in tags:
                forms[tag] = default_value
        if count == 7:
            missing_tags = tags - set(old_tags)
            for tag in missing_tags:
                forms[tag] = "?"
        if count == 14:
            # Nothing to complete
            pass
        return forms

    lemma.inflected_forms = complete_tags_in_dict(
        lemma.lemma, lemma.inflected_forms, tags
    )
    return lemma


class InflectedLemmaFormsDict:
    def __init__(
        self, complex_lemma: str, inflected_forms: dict[str, str]
    ) -> None:
        self.lemma = complex_lemma
        self.inflected_forms = inflected_forms
    def count_forms(self):
        return sum([1 for _ in self.inflected_forms])


def __lemma_complex_to_raw(
    lemma: InflectedLemmaFormsDict,
) -> InflectedLemmaFormsDict:
    lemma.lemma = raw_lemma_from_lemma(lemma.lemma)
    return lemma


# GENERIC METHODS ###
def __select_tags(
    lemma: InflectedLemmaFormsDict, tag_selector: callable[[str], bool]
) -> InflectedLemmaFormsDict:
    """
    Expects tag # Skip lemmata that are equal to the last lemma _selector to
    return true, if the given tag should be preserved, false if it should be
    removed.
    """
    to_be_deleted = []
    for tag in lemma.inflected_forms:
        if not tag_selector(tag):
            to_be_deleted.append(tag)
    for tag in to_be_deleted:
        del lemma.inflected_forms[tag]
    return lemma

if __name__ == "__main__":
    __filter_lemmata_and_forms()