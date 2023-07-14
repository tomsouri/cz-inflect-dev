#!/usr/bin/env python3.9

from __future__ import annotations
import re
from abc import ABC, abstractmethod  # abstract base class for abstract methods


class Lemma(ABC):
    """
    A parent class for a Lemma with multiple types of added information.
    Provides inverse methods to load instances from string and create string
    from instances.
    """

    _separator = ";"
    _instance_separator = "\n"
    _not_separator = ","

    @classmethod
    @abstractmethod  # Has to be overriden.
    def from_string(cls, string: str) -> Lemma:
        ...

    @abstractmethod  # Has to be overriden.
    def __str__(self) -> str:
        ...

    @classmethod
    def multiple_from_string(cls, long_string: str) -> iter[Lemma]:
        return [
            cls.from_string(instance)
            for instance in long_string.split(cls._instance_separator)
        ]

    @classmethod
    def multiple_from_file(cls, filename: str) -> iter[Lemma]:
        with open(filename, "r") as f:
            file_content = f.read()
        return cls.multiple_from_string(file_content)

    @classmethod
    def multiple_to_string(cls, lemmata: iter[Lemma]) -> str:
        """
        Converts an iterator of instances of ExplainedLemma to a string
        representing them. It is the inverse method to
        ExplainedLemma.multiple_from_string(),
        """
        return cls._instance_separator.join((str(lemma) for lemma in lemmata))

    @classmethod
    def multiple_to_file(cls, lemmata: iter[Lemma], filename) -> None:
        with open(filename, "w") as f:
            f.write(cls.multiple_to_string(lemmata))

    @classmethod
    def substitute_separators(cls, string: str) -> str:
        """
        Returns the given string without the class separators.
        """
        separators = [cls._separator, cls._instance_separator]

        result = string
        for sep in separators:
            result = re.sub(sep, cls._not_separator, result)
        return result


class ExplainedLemma(Lemma):
    """
    Represents a lemma with additive information: explanation, what does it
    mean.
    """

    _separator = ";"
    _instance_separator = "\n"
    _not_separator = ","

    def __init__(
        self,
        lemma: str,
        main_description: str,
        other_description: str,
        example: str,
    ) -> None:
        # substitute separators in all the given strings
        args = [lemma, main_description, other_description, example]
        converted = (ExplainedLemma.substitute_separators(arg) for arg in args)
        (
            self.lemma,
            self.main_description,
            self.other_description,
            self.example,
        ) = tuple(converted)

    def from_string(string: str) -> ExplainedLemma:
        """
        Convert a string representing one instance of Lemma to the instance. It
        is the inverse method to __str__(self).
        """
        return ExplainedLemma(*string.split(ExplainedLemma._separator))

    def __str__(self) -> str:
        """
        Convert the instance to a string representation.
        """
        return ExplainedLemma._separator.join(
            (
                self.lemma,
                self.main_description,
                self.other_description,
                self.example,
            )
        )


class InflectedLemma(Lemma):
    """
    Represents a simple lemma with its inflected forms.
    """

    _instance_separator = "\n"

    def __init__(self, lemma: str, inflected_forms: list[str]) -> None:
        self.lemma = lemma
        self.inflected_forms = inflected_forms

    def __str__(self) -> str:
        """
        The lemma has to be an explicit part of the InflectedLemma
        datastructure, because sometimes a word does not have 1st case of
        singular number (pomnozna podst. jmena).
        """
        return InflectedLemma._separator.join(
            [self.lemma] + self.inflected_forms
        )

    def from_string(string: str) -> InflectedLemma:
        tokens = string.split(InflectedLemma._separator)
        lemma = tokens[0]
        inflected_forms = tokens[1:]
        return InflectedLemma(lemma, inflected_forms)

    def pretty_repr(self) -> str:
        """
        Returns a pretty human-readable string that represents a lemma with its
        inflected forms.
        """
        forms = self.inflected_forms
        count = len(forms) // 2
        result = f"{'Lemma:':<10}" + self.lemma.upper()
        result += "\n"
        result += "\n".join(
            f"{i+1}.{forms[i]:<25}{i+1}.{forms[i+count]}" for i in range(count)
        )
        return result

    @classmethod
    def from_explained_inflected_lemma(cls, lemma: ExplainedInflectedLemma):
        return cls(lemma=lemma.lemma, inflected_forms=lemma.inflected_forms)

    @classmethod
    def multiple_to_file(cls, lemmata: iter[InflectedLemma], filename) -> None:
        with open(filename, "w") as f:
            for lemma in lemmata:
                f.write(str(lemma))
                f.write(cls._instance_separator)
        return

    @classmethod
    def multiple_from_file(cls, filename: str) -> iter[Lemma]:
        with open(filename, "r") as f:
            # It is crucial that "\n" is the instance separator of
            # InflectedLemma
            for line in f:
                line = line.rstrip()
                yield cls.from_string(line)


def get_pretty_string_inflected_forms(
    lemma: str, forms: list[str], separator: str
) -> str:
    """
    Returns a pretty human-readable string that represents a lemma with its
    inflected forms.
    """
    s = separator
    questions = ["kdo/co", "bez", "ke/k", "vidím", "volám", "o", "s"] * 2
    questions[7] = "ti/ty/ta"
    questions = [f"({q})" for q in questions]

    count = len(forms) // 2

    p1 = forms[:count]
    p2 = forms[count:]
    q1 = questions[:count]
    q2 = questions[count:]

    result = f"{s}{'Lemma':<10}{s} {lemma.upper()}"
    result += "\n\n"

    result += "\n".join(
        f"\t{s}{i+1}. {q1[i]:<9}{s} {p1[i]:<20}\t{s}{i+1}. {q2[i]:<10}{s} {p2[i]}"
        for i in range(count)
    )
    return result


class ExplainedInflectedLemma(Lemma):
    """
    Represents lemma with explanations and also its inflected forms. Is used
    for hand-check of the inflections.
    """

    _separator = "|"
    _instance_separator = "\n\n---\n\n"
    _is_checked_separator = "\n\n--DONE-\n\n"

    def __init__(
        self,
        lemma: str,
        main_description: str,
        other_description: str,
        example: str,
        inflected_forms: list[str],
    ) -> None:
        # TODO: substitute separators
        self.lemma = lemma
        self.main_description = main_description
        self.other_description = other_description
        self.example = example
        self.inflected_forms = inflected_forms

    @classmethod
    def from_explained_lemma(
        cls, explained_lemma: ExplainedLemma, inflected_forms: list[str]
    ) -> ExplainedInflectedLemma:
        return cls(
            explained_lemma.lemma,
            explained_lemma.main_description,
            explained_lemma.other_description,
            explained_lemma.example,
            inflected_forms,
        )

    def __str__(self) -> str:
        """
        Quite complicated way to turn all the data (lemma, explanation,
        inflected forms) to a human-readable-format string.
        """
        s = ExplainedInflectedLemma._separator
        result = f"{self.lemma}" + "\n"
        result += f"{s}{'Main dscr':<10}{s} {self.main_description}" + "\n"
        result += f"{s}{'Other dscr':<10}{s} {self.other_description}" + "\n"
        result += f"{s}{'Example':<10}{s} {self.example}" + "\n"
        result += "\n"
        result += get_pretty_string_inflected_forms(
            self.lemma, self.inflected_forms, separator=s
        )
        result += "\n"
        return result

    def from_string(string: str) -> ExplainedInflectedLemma:
        """
        The inverse method to `__str__`. Loads the instance from the
        human-readable string representation.
        """
        s = ExplainedInflectedLemma._separator
        (descr, forms) = tuple(string.split("\n\n\t" + s))
        toks = descr.split(s)
        toks = [t.strip(" \t\n") for t in toks]
        (lemma, main, other, example) = tuple([toks[2 * i] for i in range(4)])

        toks = forms.split(s)
        toks = [t.strip(" \t\n") for t in toks]

        inflected_forms = [toks[4 * i + 1] for i in range(7)] + [
            toks[4 * i + 3] for i in range(7)
        ]

        return ExplainedInflectedLemma(
            lemma, main, other, example, inflected_forms
        )

    @classmethod
    def multiple_to_string(cls, lemmata: iter[ExplainedInflectedLemma]) -> str:
        """
        Uses `_is_checked_separator` which serves during hand-check of the
        inflected forms to determine, which are already checked.
        """
        return cls._is_checked_separator + cls._instance_separator.join(
            (str(lemma) for lemma in lemmata)
        )

    @classmethod
    def multiple_from_string(cls, long_string: str) -> iter[Lemma]:
        """
        Uses `_is_checked_separator` which serves during hand-check of the
        inflected forms to determine, which are already checked.
        """
        checked_part = cls._instance_separator.join(
            long_string.split(cls._is_checked_separator)[:-1]
        )
        if checked_part == "":
            return iter([])
        return [
            cls.from_string(instance)
            for instance in checked_part.split(cls._instance_separator)
            if instance != ""
        ]


# Example usage, trial to see, whether it works the way it should.
"""
forms1 = ['jaaaaaaaaaaaaaaaablko', 'jaaaaaaaaaaaaaaaablka',
'jaaaaaaaaaaaaaaaablku', 'jaaaaaaaaaaaaaaaablko', 'jaaaaaaaaaaaaaaaablko',
'jaaaaaaaaaaaaaaaablku', 'jaaaaaaaaaaaaaaaablkem', 'jaaaaaaaaaaaaaaaablka',
'jaaaaaaaaaaaaaaaablk', 'jaaaaaaaaaaaaaaaablkům', 'jaaaaaaaaaaaaaaaablka',
'jaaaaaaaaaaaaaaaablka', 'jaaaaaaaaaaaaaaaablkech', 'jaaaaaaaaaaaaaaaablky']
forms2 = ['jablko', 'jablka', 'jablku', 'jablko', 'jablko', 'jablku',
'jablkem', 'jablka', 'jablk', 'jablkům', 'jablka', 'jablka', 'jablkech',
'jablky'] forms3 = ['internetoplavec', 'internetoplavce', 'internetoplavci',
'internetoplavec', 'internetoplavče', 'internetoplavci', 'internetoplavcem',
'internetoplavce', 'internetoplavců', 'internetoplavcům', 'internetoplavce',
'internetoplavce', 'internetoplavcích', 'internetoplavci']

e = ExplainedInflectedLemma("jablko", "hezke ovoce", "vyrabi se z toho strudl",
"Chutna ti jablko?", forms2) g =
ExplainedInflectedLemma('jaaaaaaaaaaaaaaaablko', 'hodne dlouhe jablko',
'opravdu hodne dlouhe jablko', 'Je jaaaaaaaaaaaaaaaablko delsi nez jablko?',
forms1) h = ExplainedInflectedLemma("internetoplavec", "uzivatel internetu",
"sikovny a vytrvaly uzivatel internetu", "Jsem internetoplavec. A ty?", forms3)

lemmata = [e,g,h] ExplainedInflectedLemma.multiple_to_file(lemmata,
filename="test1.txt") ExplainedInflectedLemma.multiple_to_file(lemmata,
filename="test2.txt") input() new_lemmata =
ExplainedInflectedLemma.multiple_from_file(filename="test2.txt") new_all_string
= ExplainedInflectedLemma.multiple_to_file(new_lemmata, filename="test3.txt")

with open("test1.txt") as f, open("test3.txt") as g:
    a = f.read() b = g.read()

print(a==b)

string = str(e) print(string) f = ExplainedInflectedLemma.from_string(string)
string2 = str(f) print(string2)

print(string == string2)
"""
