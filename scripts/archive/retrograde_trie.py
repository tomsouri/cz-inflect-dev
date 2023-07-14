class RetrogradeTrie(dict):
    word = ""

    def add(self, *inflected_lemmata: InflectedLemma) -> None:
        for inflected_lemma in inflected_lemmata:
            node = self
            # Iterate over reversed lemma:
            for ch in reversed(inflected_lemma.lemma):
                if ch not in node:
                    node[ch] = RetrogradeTrie()
                node = node[ch]
            node.word = inflected_lemma

    def words(self) -> list[InflectedLemma]:
        if self.word:
            yield self.word
        for ch in self:
            yield from self[ch].words()

    def longest_common_suffix(self, word: str) -> tuple[str, list[str]]:

        # Returns the list of words in the Trie that have longest common suffix with given word.

        # Reverse the string:
        word = word[::-1]
        node = self
        reversed_suffix = word
        for i, ch in enumerate(word):
            if ch not in node:
                reversed_suffix = word[:i]
                break
            node = node[ch]
        suffix = reversed_suffix[::-1]
        return (suffix, list(node.words()))
