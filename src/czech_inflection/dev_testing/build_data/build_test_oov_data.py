#!/usr/bin/env python3

from __future__ import annotations
from config import (
    TEST_OOV_MANUALLY_CHECKED_FILE, 
    TEST_OOV_DATA_FILE, 
    create_log_dir,
    LOG_DEV_BUILDING_DIR,
)
from datastructures.lemma import (
    ExplainedLemma,
    ExplainedInflectedLemma,
    InflectedLemma,
    Lemma,
)



def build_test_oov_data(
    src: str = TEST_OOV_MANUALLY_CHECKED_FILE,
    tgt: str = TEST_OOV_DATA_FILE,
    informative_printouts: bool = False,
) -> None:
    """
    Reads the manually checked explained inflected lemmata and converts them to
    a basic InflectedLemma format and prints to file.
    """
    print("Building test-oov data from the manually corrected file...")
    checked = ExplainedInflectedLemma.multiple_from_file(src)

    useful = __select_by_selector(checked, selector=__is_useful)

    inflected = [
        InflectedLemma.from_explained_inflected_lemma(lemma)
        for lemma in useful
    ]

    # Print the results to target file
    InflectedLemma.multiple_to_file(inflected, tgt)

    if informative_printouts:
        print("Loading the hand-checked inflected forms...")
        print(
            "Displaying the counts of the lemmata during process and selection."
        )
        print(f"{'Loaded hand-checked lemmata:':<40}{len(checked)}")
        print(f"{'Selected only useful:':<40}{len(useful)}")
        print(f"{'Final inflected lemmata:':<40}{len(inflected)}")

    # Logs:
    log_dir_path = create_log_dir(base_dir=LOG_DEV_BUILDING_DIR, descr="final")
    Lemma.multiple_to_file(checked, log_dir_path + "7-checked.txt")
    Lemma.multiple_to_file(useful, log_dir_path + "8-useful.txt")
    InflectedLemma.multiple_to_file(inflected, log_dir_path + "9-final.txt")

    print("Successfully built the dev data.")
    return

def __is_useful(lemma: ExplainedInflectedLemma) -> bool:
    """
    Determines, whether a lemma (after hand-check) is useful. Unuseful lemmata
    are marked, during the hand-check, with a hyphen "-" in the beginning of
    the lemma's lemma.
    """
    return lemma.lemma[0] != "-"


def __select_by_selector(
    lemmata: iter[ExplainedLemma], selector: callable[[ExplainedLemma], bool]
) -> iter[ExplainedLemma]:
    return [lemma for lemma in lemmata if selector(lemma)]

if __name__ == "__main__":
    build_test_oov_data()