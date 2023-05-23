"""
Module for aksara dependency parsing feature
"""

import os
import dependency_parsing.core as dep_parser_core

from typing import List, Literal
from aksara.conllu import ConlluData
from aksara.core import analyze_sentence, split_sentence, sentences_from_file
from aksara.analyzer import BaseAnalyzer
from .utils.conllu_io import write_conllu


class DependencyParser:
    """
    Class to perform dependency parsing
    """

    __all_models = [
        "FR_GSD-ID_CSUI",
        "FR_GSD-ID_GSD",
        "IT_ISDT-ID_CSUI",
        "IT_ISDT-ID_GSD",
        "EN_GUM-ID_CSUI",
        "EN_GUM-ID_GSD",
        "SL_SSJ-ID_CSUI",
        "SL_SSJ-ID_GSD"
    ]

    __all_input_modes = ["f", "s"]

    def __init__(self):
        self.default_analyzer = self.__get_default_analyzer()

    def parse(
            self, input_src: str,
            input_mode: Literal['f', 's'] = 's',
            is_informal: bool = False,
            sep_regex: str = None,
            model: str = "FR_GSD-ID_CSUI"
    ) -> List[List[ConlluData]]:
        """ performs dependency parsing on the text (multiple sentences)

        If `input_mode` is set to 's', text is provided as string
        in `input_src`. Alternatively, if `input_mode` is set to 'f',
        the path to a file containing the text is provided in `input_src`

        Parameters
        ----------
        input_src : str
            text that will be parsed if `input_mode` is set to 's' or
            file path to a file containing the text if `input_mode`
            is set to 'f'

        input_mode : {'f', 's'}, optional
            specifies the source of the input, default is 's'

        is_informal : bool, optional
            tells aksara to treat text as informal one, default is False

        sep_regex : str, optional
            regex rule that specifies the end of sentence, default is None

        model : str, optional
            the model to use for dependency parsing,
            default is "FR_GSD-ID_CSUI"

        Returns
        -------
        result : list of list of ConlluData
            list of result of dependency parsing of each sentence
            in form of list of ConlluData class for each word

        Raises
        ------
        FileNotFoundError
            if `input_mode` is set to 'f' but file in `input_src` doesn't exist
        ValueError
            if `input_mode` is not in ['f', 's']

        Examples
        --------
        >>> from aksara import DependencyParser
        >>> parser = DependencyParser()
        >>> text = "Apa yang kamu inginkan? Saya ingin makan."
        >>> result = parser.parse(text)
        >>> for sentence in result: #doctest: +NORMALIZE_WHITESPACE
        ...     for conllu_word in sentence:
        ...         print(conllu_word)
        1   Apa     apa     PRON    _       _       0       root    _       _
        2   yang    yang    SCONJ   _       _       4       mark    _       _
        3   kamu    kamu    PRON    _       Number=Sing|Person=2|PronType=Prs       4       nsubj   _       _
        4   inginkan        ingin   VERB    _       Voice=Act       1       acl     _       _
        5   ?       ?       PUNCT   _       _       4       punct   _       _
        1   Saya    saya    PRON    _       Number=Sing|Person=1|PronType=Prs       2       nsubj   _       _
        2   ingin   ingin   VERB    _       _       0       root    _       _
        3   makan   makan   VERB    _       _       2       xcomp   _       _
        4   .       .       PUNCT   _       _       3       punct   _       _
        """

        sentence_list = self.__get_sentence_list(input_src.strip(), input_mode, sep_regex)

        if len(sentence_list) == 0:
            return []

        result = []

        for sentence in sentence_list:
            sentence_result = self._parse_one_sentence(
                sentence, is_informal, model
            )
            result.append(sentence_result)

        return result

    def parse_to_file(
            self, input_src: str,
            write_path: str,
            input_mode: Literal['f', 's'] = 's',
            write_mode: Literal['a', 'w', 'x'] = 'x',
            is_informal: bool = False,
            sep_regex: str = None,
            sep_column: str = '\t',
            model: str = "FR_GSD-ID_CSUI"
    ) -> str:
        """ performs dependency parsing on the text (multiple sentences)
        and save the result in the CoNLL-U format in a file specified
        by `write_path`

        If `input_mode` is set to 's', text is provided as string
        in `input_src`. Alternatively, if `input_mode` is set to 'f',
        the path to a file containing the text is provided in `input_src`

        Parameters
        ----------
        input_src : str
            text that will be parsed if `input_mode` is set to 's' or
            file path to a file containing the text if `input_mode`
            is set to 'f'

        write_path : str
            path to the file where the result will be saved to

        input_mode : {'f', 's'}, optional
            specifies the source of the input, default is 's'

        write_mode : {'x', 'a', 'w'}, optional
            mode while writing on the file specified by `write_path`, default is 'x' ::

                'x': create the specified file, throws error FileExistsError if already exists
                'a': append the pos tagging result at the end of the file,
                     create the specified file if not exists
                'w': overwrite the current file content with the pos tagging result,
                     create the specified file if not exists

            NOTE::

                - 'a' write_mode will add '\\n\\n' before the pos tagging result.
                - If you plan to use 'a' write_mode in a file that already has dependency
                  parsing result on CoNLL-U format, the sent_id between the old (already in
                  the file) and new dependency parsing result will not be in sequence.

        is_informal : bool, optional
            tell aksara to treat text as informal one, default is False

        sep_regex : str, optional
            regex rule that specifies the end of sentence, default is None

        sep_column : str, optional
            regex rule that specifies gap between columns in CoNLL-U format,
            default is '\t'

        model : str, optional
            the model to use for dependency parsing,
            default is "FR_GSD-ID_CSUI"

        Returns
        -------
        str
            absolute path of output file if succesful, null otherwise

        Raises
        ------
        FileExistError
            if `write_mode` is set to 'x' but file already exists
        ValueError
            if `write_mode` not in ['x', 'a', 'w'],
            also if `input_mode` not in ['f', 's']

        """

        result = self.parse(
            input_src, input_mode=input_mode, is_informal=is_informal,
            sep_regex=sep_regex, model=model
        )

        return write_conllu(split_sentence(input_src, sep_regex), result, write_path,
                            write_mode=write_mode, separator=sep_column)

    # pylint: disable-msg=too-many-locals
    def _parse_one_sentence(
            self, sentence: str,
            is_informal: bool = False,
            model: str = "FR_GSD-ID_CSUI"
    ) -> List[ConlluData]:
        """ performs dependency parsing on one sentence

        Parameters
        ----------
        is_informal : bool, optional
            tells aksara to treat text as informal one, default is False


        model : str, optional
            the model to use for dependency parsing,
            default is "FR_GSD-ID_CSUI"

        Returns
        -------
        result: list of ConlluData
            list of ConlluData class for each word
        """

        sentence = sentence.strip()

        if sentence == "":
            return []

        default_dependency_parser = self.__get_default_dependency_parser(model)

        analyzed_sentence = analyze_sentence(
            sentence,
            self.default_analyzer,
            default_dependency_parser,
            v1=False,
            lemma=False,
            postag=False,
            informal=is_informal
        )

        result = []
        for row in analyzed_sentence.split("\n"):
            idx, form, lemma, upos, xpos, feat, head_id, deprel, _, _ = row.split("\t")
            conllu_data = ConlluData(
                idx, form, lemma, upos, xpos, feat, head_id, deprel
            )
            result.append(conllu_data)

        return result

    def __get_sentence_list(self, input_src, input_mode, sep_regex) -> List[str]:
        """ extracts a list of sentences from text

        If `input_mode` is set to 's', text is provided as string
        in `input_src`. Alternatively, if `input_mode` is set to 'f',
        the path to a file containing the text is provided in `input_src`
        """

        if input_mode == "s":
            return split_sentence(input_src, sep_regex)

        if input_mode == "f":
            return sentences_from_file(input_src, sep_regex)

        raise ValueError(
            f"input_mode must be one of {self.__all_input_modes}, but {input_mode} was given"
        )

    def __get_default_analyzer(self) -> BaseAnalyzer:
        """ returns a base analyzer instance with aksara binary file
        """

        bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
        return BaseAnalyzer(bin_path)

    def __get_default_dependency_parser(self, model) -> dep_parser_core.DependencyParser:
        """ returns a dependency parser instance with the specified model
        """

        if model not in self.__all_models:
            raise ValueError(f"model must be one of {self.__all_models}, but {model} was given")

        return dep_parser_core.DependencyParser(model)
