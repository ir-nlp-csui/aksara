#!/usr/bin/python3
from tqdm import tqdm

import os
import re


from .analyzer import (
    BaseAnalyzer,
)

from .core import analyze_sentence, get_num_lines

from dependency_parsing.core import DependencyParser

BIN_FILE = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "bin/aksara@v1.2.0.bin"
)


def pip_parser_string(
    input_str: str, lemma_bool: bool, postag_bool: bool, informal_bool: bool
):
    analyzer = BaseAnalyzer(BIN_FILE)
    dependency_parser = DependencyParser()

    text = input_str
    temp = re.split(r"([.!?]+[\s])", text)
    sentences = []
    for i in range(len(temp)):
        if i % 2 == 0:
            sentences.append(temp[i] + (temp[i + 1] if i != len(temp) - 1 else ""))

    output = ""
    for i in range(len(sentences)):
        output += analyze_sentence(
            sentences[i],
            analyzer,
            dependency_parser,
            v1=False,
            lemma=lemma_bool,
            postag=postag_bool,
            informal=informal_bool,
        )
        output += "\n\n"

    return output.rstrip()


def pip_parser_file(
    input_file: str, lemma_bool: bool, postag_bool: bool, informal_bool: bool
):
    analyzer = BaseAnalyzer(BIN_FILE)
    dependency_parser = DependencyParser()

    file = open(input_file, "r")

    output = ""
    with file as infile:
        tqdm_setup = tqdm(
            infile,
            total=get_num_lines(infile.name),
            bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}",
        )
        for i, line in enumerate(tqdm_setup, 1):
            text = line.rstrip()
            temp = re.split(r"([.!?]+[\s])", text)
            sentences = []
            for i in range(len(temp)):
                if i % 2 == 0:
                    sentences.append(
                        temp[i] + (temp[i + 1] if i != len(temp) - 1 else "")
                    )

            for j in range(len(sentences)):
                temp = analyze_sentence(
                    sentences[j],
                    analyzer,
                    dependency_parser,
                    v1=False,
                    lemma=lemma_bool,
                    postag=postag_bool,
                    informal=informal_bool,
                )
                output += temp + "\n\n"

    file.close()

    return output.rstrip()
