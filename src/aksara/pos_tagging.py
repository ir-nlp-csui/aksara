import os
import re
from conllu import parse
from tqdm import tqdm

from aksara.core import analyze_sentence, get_num_lines
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser


def pos_tagging_file(
    input_file: str, is_informal: bool = False
) -> list[list[tuple[str]]]:
    result = []

    analyzer = __get_default_analyzer()
    dependency_parser = __get_default_dependency_parser()

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
                    lemma=False,
                    postag=True,
                    informal=is_informal,
                )
                output += temp + "\n\n"

    file.close()

    sentences = parse(output.rstrip())

    for sentence in sentences:
        sentence_list = []
        for word in sentence:
            sentence_list.append((word["form"], word["lemma"]))
        result.append(sentence_list)

    return result


def __get_default_analyzer():
    bin_path = os.path.join(
        os.path.join(os.path.dirname(__file__), ".."), "bin/aksara@v1.2.0.bin"
    )

    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser():
    return DependencyParser()
