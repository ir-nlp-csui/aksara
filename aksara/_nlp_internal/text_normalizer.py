import json
import os

from symspellpy import SymSpell, Verbosity

cur_dir_path = os.path.dirname(__file__)

gold_path = os.path.join(
    cur_dir_path,
    "text_normalization",
    "kbbi.txt"
)
json_path = os.path.join(
    cur_dir_path,
    "text_normalization",
    "context_dictionary.json"
)
json_file = open(json_path)
context_dictionary = json.load(json_file)
json_file.close()


class TextNormalizer:
    def __init__(self):
        sym_spell = SymSpell(max_dictionary_edit_distance=3)
        sym_spell.create_dictionary(gold_path)
        self.__sym_spell = sym_spell

    def normalize_symspell(self, sample, *relations):
        sample = sample.strip('\n')

        suggestions = self.__sym_spell.lookup(sample, Verbosity.ALL)
        candidates = [
            suggestion.term for suggestion in suggestions]

        if (not len(candidates)):
            return sample

        best_match = ''

        for candidate in candidates:
            for relation in relations:
                if relation not in context_dictionary:
                    continue

                for freq in context_dictionary[relation]:
                    match = candidate in context_dictionary[relation][freq]
                    if match:
                        best_match = candidate
                        break
                if (best_match):
                    break
            if (best_match):
                break

        return best_match if best_match else sample
