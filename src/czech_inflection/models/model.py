#!/usr/bin/env python3.9

"""
The interface for Model for inflection.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ModelBase(ABC):
    """
    Baseclass for every model for czech inflection.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Getter of the name describing the model.
        """

    @abstractmethod
    def inflect(self, lemma: str) -> list[str]:
        """
        Inflect the given lemma.

        Use the model's particular way to inflect the given lemma, that is,
        to create a list of inflected forms.

        Parameters:
            lemma(str): the lemma to be inflected

        Returns:
            list[str]: the inflected forms.
        """
