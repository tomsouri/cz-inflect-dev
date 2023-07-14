#!/usr/bin/env python3.9

"""
Implements simple morfflex "bag-of-words" lexicon to recognise OOV words.
Example usage:

from morfflex import Lexicon 
vocab = Lexicon() 
word = "jablko"
vocab.is_OOV(word)
"""
import os
from config import MORFFLEX_LEMMATA
from morfflex.build_lemmata_only import build_lemmata_only


class MorfflexLexicon:
    # change path to the file, add check if the file exists, if not, call
    # get_words_from_morfflex

    def __init__(self, filename=MORFFLEX_LEMMATA):
        def get_vocab_set(vocab_filename):
            """
            Reads given/default morfflex vocabulary file and creates a set as a
            bag of words contained in the dictionary.
            """
            if not os.path.exists(vocab_filename):
                build_lemmata_only()

            vocab_set = set()
            with open(vocab_filename, "r") as f:
                for line in f:
                    word = self.__convert_word(line)
                    vocab_set.add(word)
            return vocab_set

        self.vocab_set = get_vocab_set(filename)

    def __convert_word(self, word):
        converted = word.removesuffix("\n")
        converted = converted.lower()
        return converted

    def __contains(self, word):
        return self.__convert_word(word) in self.vocab_set

    def is_OOV(self, word):
        return not self.__contains(word)


if __name__ == "__main__":
    vocab = MorfflexLexicon()
    while True:
        print("Enter word:")
        word = input()
        print(vocab.__contains(word))
