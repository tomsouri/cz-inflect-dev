#!/usr/bin/env python3.9

# Prevzato ze StackOverflow:
# https://stackoverflow.com/a/61827507

from __future__ import annotations
from datastructures.lemma import InflectedLemma


class Trie(dict):
    def __init__(self):
        self.all_words = []

    def add(self, key: str, value: InflectedLemma) -> None:
        node = self
        for ch in key:
            if ch not in node:
                node[ch] = Trie()
            node = node[ch]
        node.all_words.append(value)

    def words(self) -> iter[InflectedLemma]:
        """
        Yield all words stored in the whole subtree of this node.
        """
        if len(self.all_words) != 0:
            yield from self.all_words
        for ch in self:
            yield from self[ch].words()

    def longest_common_prefix(
        self, word: str
    ) -> tuple[str, iter[InflectedLemma]]:
        """
        Returns the found prefix and iter of words in the Trie that have
        longest common prefix with given word.
        """
        node = self
        prefix = word
        for i, ch in enumerate(word):
            if ch not in node:
                prefix = word[:i]
                break
            node = node[ch]
        return (prefix, node.words())


if __name__ == "__main__":
    # Example usage:
    t = Trie()

    with open(
        "/svolume/matfyz/rp-sourada/czech-automatic-declension/data/cleaned/dev_data.txt",
        "r",
    ) as f:
        lemmata = []
        for line in f:
            tokens = line.strip().split(";")
            lemmata.append(InflectedLemma(tokens[0], tokens[1:]))
    for lemma in lemmata:
        t.add(key=lemma.lemma, value=lemma)
    (x, y) = t.longest_common_prefix("elektrokolo")
    print(x)
    input()
    print([str(z) for z in y])
    input()
    (x, y) = t.longest_common_prefix("jablko")
    print(x, [str(z) for z in y])
