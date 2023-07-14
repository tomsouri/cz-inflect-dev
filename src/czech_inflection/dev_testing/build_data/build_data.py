#!/usr/bin/env python3.9

from __future__ import annotations
import argparse
import random

from dev_testing.build_data.cestina20reader import get_lemmata
from datastructures.lemma import (
    ExplainedLemma,
    ExplainedInflectedLemma,
)
from dev_testing.build_data.build_test_oov_data import build_test_oov_data
from morfflex.lexicon import MorfflexLexicon
from models.hardcoded.sklonuj_cz import SklonujCzModel

from config import create_log_dir
from config import LOG_DEV_BUILDING_DIR
from config import TEST_OOV_MANUALLY_CHECKED_FILE, TEST_OOV_DATA_FILE
from config import SEED

parser = argparse.ArgumentParser()
parser.add_argument(
    "--inflect",
    default=False,
    action="store_true",
    help="Load the raw data and creates the inflected forms of the lemmata "
    + "and print to file to be hand-checked.",
)
parser.add_argument(
    "--load_checked",
    default=False,
    action="store_true",
    help="Load the checked inflected forms and create the dev data.",
)
parser.add_argument(
    "--filename",
    default=TEST_OOV_MANUALLY_CHECKED_FILE,
    help="The file from which to load the checked inflected forms.",
)


def main(args: argparse.Namespace):
    def inflect() -> None:
        print("Creating the inflected forms...")
        print(
            "Displaying the counts of the lemmata during process and selection."
        )

        # Prepare the directory to print the results:
        log_dir_path = create_log_dir(
            base_dir=LOG_DEV_BUILDING_DIR, descr="unchecked"
        )

        # Load the lemmata from the input cestina2.0 files
        lemmata = get_lemmata()

        # Convert to ExplainedLemma datastructure.
        explained_lemmata = [
            ExplainedLemma(
                lemma.lemma,
                lemma.main_description,
                lemma.other_description,
                lemma.example,
            )
            for lemma in lemmata
        ]
        print(
            f"{'Loaded lemmata from the input files:':<40}"
            + f"{len(explained_lemmata)}"
        )
        ExplainedLemma.multiple_to_file(
            explained_lemmata, log_dir_path + "1-explained.txt"
        )

        words_only = __select_by_selector(
            explained_lemmata, selector=__is_word
        )
        print(f"{'Selected words (without phrases):':<40}{len(words_only)}")
        ExplainedLemma.multiple_to_file(
            words_only, log_dir_path + "2-words_only.txt"
        )

        # This does nothing. Since the most of the words are nouns and since
        # it is not easy to decide it automatically, we decide it manually
        # during manual inflection.
        nouns_only = __select_by_selector(words_only, selector=__is_noun)
        print(f"{'Selected nouns:':<40}{len(nouns_only)}")
        ExplainedLemma.multiple_to_file(
            nouns_only, log_dir_path + "3-nouns_only.txt"
        )

        lexicon = MorfflexLexicon()
        OOV_only = [
            lemma for lemma in nouns_only if lexicon.is_OOV(lemma.lemma)
        ]
        print(f"{'Selected OOV words:':<40}{len(OOV_only)}")
        ExplainedLemma.multiple_to_file(
            OOV_only, log_dir_path + "4-OOV_only.txt"
        )

        random.seed(SEED)
        random.shuffle(OOV_only)
        shuffled = OOV_only
        print(f"{'Shuffled:':<40}{len(shuffled)}")
        ExplainedLemma.multiple_to_file(
            shuffled, log_dir_path + "5-shuffled.txt"
        )

        model = SklonujCzModel()
        inflected = [
            ExplainedInflectedLemma.from_explained_lemma(
                expl_lemma, model.inflect(expl_lemma.lemma)
            )
            for expl_lemma in shuffled
        ]
        print(f"{'Inflected:':<40}{len(inflected)}")
        ExplainedInflectedLemma.multiple_to_file(
            inflected, log_dir_path + "6-inflected.txt"
        )
        return

    if args.inflect:
        inflect()
    elif args.load_checked:
        build_test_oov_data(src=args.filename, informative_printouts=True)
    else:
        print(
            "You can inflect the lemmata or load the checked inflected forms."
        )
        print("Choose:")
        print("--inflect")
        print("--load_checked")


def __is_word(lemma: ExplainedLemma) -> bool:
    """
    Lemma is a word (not a phrase), if it does not contain a space.
    """
    return " " not in lemma.lemma.strip()


def __is_noun(lemma: ExplainedLemma) -> bool:
    """Always return true, ignore this selector."""
    return True


def __select_by_selector(
    lemmata: iter[ExplainedLemma], selector: callable[[ExplainedLemma], bool]
) -> iter[ExplainedLemma]:
    return [lemma for lemma in lemmata if selector(lemma)]


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)
