import os

from typing import Union
from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser


class Lemmatizer:
    def __init__(self):
        self.default_analyzer = self.__get_default_analyzer()
        self.default_dependency_parser = self.__get_default_dependency_parser()

    def lemmatize(self, word_input: str, is_informal: bool = False) -> Union[str, list]:
        """

        performs lemmatization on a word,

        then returns a string containing its corresponding

        lemma as the result or a list if the word contains

        certain affixes



        parameters
        ----------

        input: str

            the word that will be analyzed



        is_informal: bool

            tell aksara to treat text as informal , default to False



        return
        ------

        ReturnType: str | list

            will return string containing each word's lemma or
            list if the word contains certain affixes

        """
        word_input = word_input.strip()

        if word_input == "":
            return ""

        lemmatized_result = self.lemmatize_batch([word_input], is_informal)

        if len(lemmatized_result) > 1:
            return lemmatized_result

        result = lemmatized_result[0][1]

        return result

    def lemmatize_batch(
        self, list_word: list, is_informal: bool = False
    ) -> list[tuple[str, str]]:
        """

        performs lemmatization on the sentence list,

        then returns a list containing each word paired with its

        corresponding lemma as the result



        parameters
        ----------

        input: list

            the list of words (sentence) that will be analyzed



        is_informal: bool

            tell aksara to treat text as informal , default to False



        return
        ------

        ReturnType: list

            will return list containing each word paired with its

            corresponding lemma as the result

        """

        if list_word == []:
            return []

        input_text = " ".join(list_word)

        temp_result = analyze_sentence(
            text=input_text,
            analyzer=self.default_analyzer,
            dependency_parser=self.default_dependency_parser,
            v1=False,
            lemma=True,
            postag=False,
            informal=is_informal,
        )

        result = []

        for line in temp_result.split("\n"):
            _, word, lemma = line.split("\t")
            result.append((word, lemma))

        return result

    def __get_default_analyzer(self) -> BaseAnalyzer:
        bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
        return BaseAnalyzer(bin_path)

    def __get_default_dependency_parser(self) -> DependencyParser:
        return DependencyParser()