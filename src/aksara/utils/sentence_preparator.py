
from typing import List

from aksara.core import split_sentence


def _preprocess_text(text: str, ssplit: bool=True, sep_regex: str=None) -> List[str]:
    """
    Preprocess text. By default will split multi sentence in the text and remove whitespace only sentence.
    
    Set ssplit=False to disable multi sentence splitting.
    """

    if not ssplit:
        return [text.strip()]

    sentence_lists: List[str] = split_sentence(text, sep_regex)
    sentence_lists = map(lambda sentence: sentence.strip(), sentence_lists)

    stripped_sentences = list(filter(lambda sentence: len(sentence) > 0, sentence_lists))

    return stripped_sentences