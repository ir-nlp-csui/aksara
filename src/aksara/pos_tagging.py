import os
from conllu import parse

from src.aksara.core_pip import pip_parser_string, pip_parser_file


def pos_tagging(
    input_text: str, input_type: str = "s", informal: bool = False
) -> list[list[list[str]]]:
    result = []

    if input_type == "f":
        sentences = parse(pip_parser_file(input_text, False, True, informal))
    else:
        sentences = parse(pip_parser_string(input_text, False, True, informal))

    for sentence in sentences:
        sentence_list = []
        for word in sentence:
            sentence_list.append([word["form"], word["lemma"]])
        result.append(sentence_list)

    return result


# if __name__ == "__main__":
# print(
#     pos_tagging(
#         "/Users/malikismail/Library/CloudStorage/OneDrive-UNIVERSITASINDONESIA/Documents/Uni/Sem 6/PPL/NLP Aksara/nlp-aksara/src/input_example.txt",
#         "f",
#     )
# )
# print(
#     pos_tagging(
#         "/Users/malikismail/Library/CloudStorage/OneDrive-UNIVERSITASINDONESIA/Documents/Uni/Sem 6/PPL/NLP Aksara/nlp-aksara/tests/testinput.txt",
#         "f",
#     )
# )
# print(
#     pos_tagging(
#         '"Meski kebanyakan transisi digital yang terjadi di Amerika Serikat belum pernah terjadi sebelumnya, transisi kekuasaan yang damai tidaklah begitu," tulis asisten khusus Obama, Kori Schulman di sebuah postingan blog pada hari Senin.'
#     )
# )
# print(
#     pos_tagging(
#         "Pengeluaran baru ini dipasok oleh rekening bank gemuk Clinton. Uang yang hilang pada tahun itu sangat banyak."
#     )
# )
