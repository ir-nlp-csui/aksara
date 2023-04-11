import codecs
import os
import re

from typing import List, Literal
from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser


def morphological_analyzer(
        sentences: str,
        is_informal: bool = False,
        sep_regex: str = r'([\.\!\?]+[\s])'
) -> List[List[tuple[str, List]]]:

    sentences = sentences.strip()

    if sentences == "":
        return []

    result = []

    sentence_list = __split_sentence(sentences, sep_regex)

    default_analyzer = __get_default_analyzer()
    default_dependency_parser = __get_default_dependency_parser()

    for sentence in sentence_list:
        analyzed_sentence = analyze_sentence(sentence, default_analyzer,
                                             default_dependency_parser, v1=False,
                                             lemma=False, postag=False, informal=is_informal)
        sentence_result = []
        for row in analyzed_sentence.split("\n"):
            _, form, _, _, _, feat, _, _, _, _ = row.split("\t")

            if feat != "_":
                feat = feat.split("|")
                sentence_result.append((form, feat))
            else:
                sentence_result.append((form, []))

        result.append(sentence_result)

    return result

def morphological_analyzer_from_file(
        input_path: str,
        is_informal: bool = False,
        sep_regex: str = r'([\.\!\?]+[\s])'
) -> List[List[tuple[str, List]]]:

    sentences_from_file = ""

    with open(input_path, 'r', encoding="utf-8") as file:
        sentences_from_file = file.read()

    if '\n' not in sep_regex :
        sentences_from_file.replace('\n', '')

    return morphological_analyzer(sentences_from_file, sep_regex=sep_regex,
                                  is_informal=is_informal)

def morphological_analyzer_from_text_to_file(
    text: str,
    output_path: str,
    sep_regex: str = r'([\.\!\?]+[\s])',
    write_mode: Literal["x", "a", "w"] = "w",
    is_informal: bool = False,
) -> str:
    """
    performs morphological analyze on the text,
    then save the result in the file specified by output_path

    parameters
    ----------
    text: str
        the text that will be analyzed

    output_path: str
        path to the file where the morphological analyze result will be saved to

    sep_regex: str
        regex rule that specify end of sentence

    write_mode: str, ['x', 'a', 'w'], default to 'w'
        mode while writing on the file specified by output_path

        'x': create the specified file, throws error FileExistsError if already exists
        'a': append the morphological analyze result at the end of the file,
                create the specified file if not exists
        'w': overwrite the current file content with the morphological analyze result,
                create the specified file if not exists

        NOTE:
        - if write_mode not in ['x', 'a', 'w'] will throws ValueError
        - 'a' write_mode will add '\n\n' before the morphological analyze result.
        - If you plan to use 'a' write_mode in a file that already has
            analyze result on connlu format, the sent_id between
            the old (already in the file) and new analyze result will not ne in sequence.

    is_informal: bool
        tell aksara to treat text as informal one, default to False

    return
    ------
    ReturnType: str
        will return output_path if succesfully analyze and save the result on the given output_path
    """

    all_write_modes = ["x", "a", "w"]

    if write_mode not in all_write_modes:
        raise ValueError(f"write_mode must be in {all_write_modes}")

    sentence_list = __split_sentence(text, sep_regex)
    analyzed_text = morphological_analyzer(text, sep_regex=sep_regex,
                                           is_informal=is_informal)

    with open(output_path, write_mode, encoding="utf-8") as output_file:
        if write_mode == "a" and len(analyzed_text) != 0:
            output_file.writelines("\n\n")

        for i, sentence_feat in enumerate(analyzed_text):
            output_file.writelines(f"# sent_id = {str(i + 1)}\n# text = {sentence_list[i]}")

            for idx, (form, feat) in enumerate(sentence_feat):
                combined_feat = "_"
                if feat != []:
                    combined_feat = "|".join(feat)

                output_file.writelines(f"\n{idx + 1}\t{form}\t{combined_feat}")

            if i < len(analyzed_text) - 1:  # don't add \n at the end of the file
                output_file.writelines("\n\n")

    return os.path.realpath(output_path)

def morphological_analyzer_from_file_to_file(
    input_path: str,
    output_path: str,
    sep_regex: str = r'([\.\!\?]+[\s])',
    write_mode: Literal["x", "a", "w"] = "w",
    is_informal: bool = False,
) -> str:

    if input_path is output_path:
        return "input_path and output_path must be different"

    sentences_from_file = ""

    with open(input_path, 'r', encoding="utf-8") as file:
        sentences_from_file = file.read()

    if '\n' not in sep_regex:
        sentences_from_file.replace('\n', '')

    return morphological_analyzer_from_text_to_file(sentences_from_file, output_path=output_path,
                                                    sep_regex=sep_regex, write_mode=write_mode,
                                                    is_informal=is_informal)

def __split_sentence(text: str, sep_regex: str = r"([.!?]+[\\s])") -> List[str]:
    """
    this method will split a multi sentences text based on separator regex (sep_regex)

    parameters
    ---------

    text: str
        sentences that will be splitted

    sep_regex: str
        regex rule that determine the points where the text will be splitted at.

    return
    ------
    ReturnType: List of string
        splitted text
    """

    splitted_sentences = re.split(codecs.decode(
        sep_regex, 'unicode_escape'), text)
    sentence_list = []
    for i, sentence in enumerate(splitted_sentences):
        if i % 2 == 0:
            sentence_list.append(
                sentence + (splitted_sentences[i +
                                       1] if i != len(splitted_sentences) - 1
                                        else ""
                )
            )

    return sentence_list

def __get_default_analyzer() -> BaseAnalyzer:
    bin_path = os.path.join(os.path.dirname(__file__),
                            "bin", "aksara@v1.2.0.bin")
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser() -> DependencyParser:
    return DependencyParser()
