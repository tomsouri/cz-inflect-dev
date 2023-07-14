from abc import abstractmethod

class SimpleModel(ModelBase):
    """
    Baseclass for every model, in which there is no advantage in calling 
    the `inflect` method for multiple lemmata at the same time,
    and it is sufficient enough to call a simple inflection method multiple times.
    """

    def inflect(self, lemmata: list[str]) -> list[list[str]]:
        """
        Inflects each given lemma calling its `__inflect_single` method for the lemmata one by one.
        """
        return [self.__inflect_single(lemma) for lemma in lemmata]

    @abstractmethod
    def __inflect_single(self, lemma: str) -> list[str]:
        """
        Inflects the single given lemma.
        
        Uses the model's way to inflect the given lemma,
        that is, to create a list of inflected forms.

        Parameters:
        lemma (str): The lemma to be inflected.

        Returns:
        list[str]: The list of inflected forms.
        """


    #@abstractmethod
    #def inflect(self, lemmata: list[str]) -> list[list[str]]:
        """
        Inflects the given list of lemmata.

        Uses the model's way to inflect every given lemma,
        that is, create the inflected forms of each lemma.

        Parameters:
        lemmata (list[str]): The list of lemmata (strings) to be inflected.

        Returns:
        list[list[str]]: A list containing inflected forms for each given lemma, these lists inside another list.
        """