import os
import re
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

    with file as infile:
        tqdm_setup = tqdm(
            infile,
            total=get_num_lines(infile.name),
            bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}",
        )

        for _, line in enumerate(tqdm_setup, 1):
            sentences_inline = re.split(r"([.!?]+[\s])", line.rstrip())
            sentences = []
            for i in range(len(sentences_inline)):
                if i % 2 == 0:
                    sentences.append(
                        sentences_inline[i]
                        + (
                            sentences_inline[i + 1]
                            if i != len(sentences_inline) - 1
                            else ""
                        )
                    )

            for j in range(len(sentences)):
                analyzed_sentence = []
                analyzed = analyze_sentence(
                    sentences[j],
                    analyzer,
                    dependency_parser,
                    v1=False,
                    lemma=False,
                    postag=True,
                    informal=is_informal,
                )
                for token in analyzed.split("\n"):
                    _, word, postag = token.split("\t")
                    analyzed_sentence.append((word, postag))

                result.append(analyzed_sentence)

    file.close()

    return result


def __get_default_analyzer():
    bin_path = os.path.join(
        os.path.join(os.path.dirname(__file__), ".."), "bin/aksara@v1.2.0.bin"
    )

    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser():
    return DependencyParser()
