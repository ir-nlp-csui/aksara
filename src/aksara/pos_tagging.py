import os
from conllu import parse

# POS Tagging Satu Kata
# TODO

# POS Tagging Satu Kalimat
# TODO

# POS Tagging Multi-Kalimat
# TODO

# POS Tagging File
# TODO


def pos_tagging(
    input_text: str, input_type: str = "s", informal_bool: bool = False
) -> list[list[list[str]]]:
    input_type = "-f" if input_type.lower() in ["file", "f"] else "-s"
    informal = " --informal" if informal_bool else ""

    cmd = f"python3 src/aksara.py --postag{informal} {input_type} '{input_text}'"

    sentences = os.popen(cmd).read()

    if input_type == "-f":
        sentences = sentences[21:]

    sentences = parse(sentences)

    result = []

    for sentence in sentences:
        sentence_list = []
        for word in sentence:
            sentence_list.append([word["form"], word["lemma"]])
        result.append(sentence_list)

    return result


if __name__ == "__main__":
    # print(
    #     pos_tagging(
    #         "/Users/malikismail/Library/CloudStorage/OneDrive-UNIVERSITASINDONESIA/Documents/Uni/Sem 6/PPL/NLP Aksara/nlp-aksara/src/input_example.txt",
    #         "f",
    #     )
    # )
    print(
        pos_tagging(
            "/Users/malikismail/Library/CloudStorage/OneDrive-UNIVERSITASINDONESIA/Documents/Uni/Sem 6/PPL/NLP Aksara/nlp-aksara/tests/testinput.txt",
            "f",
        )
    )
    # print(
    #     pos_tagging(
    #         '"Meski kebanyakan transisi digital yang terjadi di Amerika Serikat belum pernah terjadi sebelumnya, transisi kekuasaan yang damai tidaklah begitu," tulis asisten khusus Obama, Kori Schulman di sebuah postingan blog pada hari Senin.'
    #     )
    # )
