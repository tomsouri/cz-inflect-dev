#!/usr/bin/env python3.9

from __future__ import annotations

from config import MORFFLEX_TRIE_PICKLED_DIR
from data import get_train_data
from datastructures.trie import Trie
from datastructures.lemma import InflectedLemma

import os
import pickle


class MorfFlexRetrogradeTrie:
    """
    Wrapper of a standard character-based trie, which for given key stores the
    given value.

    The retrograde trie containing train data from MorfFlex. It loads the data
    during initialization.
    """

    def __init__(self, train_data_size: int = 360_000) -> None:
        pickled_filename = MorfFlexRetrogradeTrie.get_pickle_filename(
            train_data_size
        )
        # If you want to save time with building the trie,
        # uncomment this
        # and comment the line under this
        
        #if os.path.exists(pickled_filename):
            # If the trie with the given train_data_size has been already
            # created, load the pickled
        #    with open(pickled_filename, "rb") as pickle_off:
        #        trie = pickle.load(pickle_off)
        #else:
            # If the trie has never been created, build it and pickle to be
            # used another time.
            #trie = MorfFlexRetrogradeTrie.fill_pickle_trie(train_data_size)

        trie = MorfFlexRetrogradeTrie.fill_pickle_trie(train_data_size)
        
        self._trie = trie

    def longest_common_suffix(
        self, lemma: str
    ) -> tuple[str, iter[InflectedLemma]]:
        """
        Finds the lemmata in the inner trie with longest common suffix.
        """
        reversed_lemma = lemma[::-1]
        (
            reversed_prefix_of_reversed_words,
            lemmata,
        ) = self._trie.longest_common_prefix(word=reversed_lemma)
        suffix = reversed_prefix_of_reversed_words[::-1]
        return (suffix, lemmata)

    @staticmethod
    def get_pickle_filename(train_data_size: int) -> str:
        return MORFFLEX_TRIE_PICKLED_DIR + f"{train_data_size}_trie.pickle"

    @staticmethod
    def fill_pickle_trie(train_data_size: int) -> Trie:
        """Creates the inner trie, fills it with the train data and pickles it
        and returns it."""
        pickle_filename = MorfFlexRetrogradeTrie.get_pickle_filename(
            train_data_size
        )
        train_data = get_train_data(train_data_size)

        train_data = list(train_data)

        trie = Trie()
        for lemma in train_data:
            reversed_lemma = lemma.lemma[::-1]
            trie.add(key=reversed_lemma, value=lemma)
        with open(pickle_filename, "wb") as fh:
            pickle.dump(trie, fh)
        return trie
