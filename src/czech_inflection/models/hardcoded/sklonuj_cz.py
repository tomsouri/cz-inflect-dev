#!/usr/bin/env python3

"""
IMPLEMENTS THE MODEL BASED ON SKLONUJ.CZ After importing the model and creating
an instance you can simply call its method `inflect` with a lemma: string as
an argument.

> Example call:

from sklonuj_cz import SklonujCzModel

model = SklonujCzModel()
lemma = "internetoplavec"
forms = model.inflect(lemma)


> Example result in forms:
['internetoplavec', 'internetoplavce', 'internetoplavci', 'internetoplavec',
'internetoplavče', 'internetoplavci', 'internetoplavcem', 'internetoplavce',
'internetoplavců', 'internetoplavcům', 'internetoplavce', 'internetoplavce',
'internetoplavcích', 'internetoplavci']
"""

from __future__ import annotations

import subprocess
import sys
from config import SKLONUJ_CZ_PHP
from models.model import ModelBase

# To be able to run PHP script, you need to install PHP according to
# https://medium.com/@bahadirmezgil/how-to-install-php-and-apache-on-linux-ubuntu-linux-mint-ea73a1c1c426
# and the package mb_string: sudo apt install php7.3-mbstring


class SklonujCzModel(ModelBase):
    @property
    def name(self) -> str:
        return "Sklonuj.cz"

    def inflect(self, lemma: str) -> list[str]:
        """
        Inflect the given lemma.

        Parameters:
            lemma(str): the lemma to be inflected

        Returns:
            list[str]: the inflected forms.
        """

        # Wrap the `_inflect_multiple` method.
        lemmata = [lemma]
        inflected_forms_lists = self.__inflect_multiple(lemmata)
        inflected_forms = inflected_forms_lists[0]

        # Hack to fix the bug that the sklonuj.cz script sometimes returns less
        # than 14 forms
        while len(inflected_forms) < 14:
            inflected_forms.append("?")

        return inflected_forms

    def __inflect_multiple(self, lemmata: list[str]) -> list[list[str]]:
        """
        # Inflects the given list of lemmata, uses the hardcoded PHP rules for
        the inflection.

        Uses the model's way to inflect every given lemma, that is, create the
        inflected forms of each lemma.

        Parameters: lemmata (list[str]): The list of lemmata (strings) to be
        inflected.

        Returns: list[list[str]]: A list containing inflected forms for each
        given lemma, these lists inside another list.
        """
        # Use PHP script with hardcoded rules in the subprocess.
        args = " ".join(lemmata)

        process = subprocess.Popen(
            "php " + SKLONUJ_CZ_PHP + " " + args,
            shell=True,
            stdout=subprocess.PIPE,
        )
        script_response = process.stdout.read()
        result_string = script_response.decode("utf-8")

        # Convert the result from the PHP script to the desired format.
        inflected_forms_strings = [
            part for part in result_string.split(";") if part != ""
        ]
        inflected_forms_lists = [
            inflected_forms_string.split()
            for inflected_forms_string in inflected_forms_strings
        ]

        return inflected_forms_lists


if __name__ == "__main__":
    lemmata = sys.argv[1:]
    model = SklonujCzModel()
    tokens_lists = [model.inflect(lemma=lemma) for lemma in lemmata]
    for (lemma, tokens_list) in zip(lemmata, tokens_lists):
        print(
            f"Lemma: {lemma}" + "\ninflected forms: " + ", ".join(tokens_list)
        )
