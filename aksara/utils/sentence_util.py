import re
from typing import List
import os

from tqdm import tqdm

from aksara._nlp_internal.core import get_num_lines


__all_input_modes = ['s', 'f']

def _get_sentence_list(input_src, input_mode='s', sep_regex=None) -> List[str]:
    """ extracts a list of sentences from text

    If `input_mode` is set to 's', text is provided as string
    in `input_src`. Alternatively, if `input_mode` is set to 'f',
    the path to a file containing the text is provided in `input_src`
    """

    if input_mode == "s":
        return _split_sentence(input_src, sep_regex)

    if input_mode == "f":
        return _sentences_from_file(input_src, sep_regex)

    raise ValueError(
        f"input_mode must be one of {__all_input_modes}, but {input_mode} was given"
    )

def _split_sentence(text: str, sep_regex: str = None) -> List[str]:
    """
    this method will split a multi sentences text based on separator regex (sep_regex)
    """

    if sep_regex is None:
        sep_regex = r"([.!?]+[\s])"

    splitted_sentences = re.split(sep_regex, text)
    sentence_list = []
    for i, sentence in enumerate(splitted_sentences):
        if i % 2 == 0:
            sentence_with_end_mark = sentence + (
                splitted_sentences[i + 1] if i != len(splitted_sentences) - 1 else ""
            )

            sentence_with_end_mark = sentence_with_end_mark.strip()

            if len(sentence_with_end_mark) > 0:
                sentence_list.append(sentence_with_end_mark)

    return sentence_list


def _sentences_from_file(file_path: str, sep_regex: str = None) -> List[str]:
    result = []

    if os.path.getsize(file_path) == 0:
        return []

    with open(file_path, "r", encoding="utf-8") as infile:

        tqdm_setup = tqdm(
            infile,
            total=get_num_lines(infile.name),
            bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}",
        )
        for _, line in enumerate(tqdm_setup, 1):
            sentences = _split_sentence(line.rstrip(), sep_regex)
            for sentence in sentences:
                result.append(sentence.strip())

    return result
