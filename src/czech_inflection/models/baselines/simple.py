#!/usr/bin/env python3.9

from __future__ import annotations
from models.model import ModelBase


class SimpleBaseline(ModelBase):
    @property
    def name(self) -> str:
        return "Simple baseline"

    def inflect(self, lemma: str) -> list[str]:
        """
        Inflect the given lemma and return list of its inflected forms.

        Parameters:
            lemma(str): the lemma to be inflected

        Returns:
            list[str]: the inflected forms.
        """
        return [lemma] * 14