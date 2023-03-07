
def lemmatization_satu_kata(
    input_text: str, input_type: str = "s", informal_bool: bool = False
) -> list[list[list[str]]]:
    result = []

    input_type = "-f" if input_type.lower() in ["file", "f"] else "-s"
    informal = " --informal" if informal_bool else ""

    cmd = f"python3 src/aksara.py --postag{informal} {input_type} '{input_text}'"

    sentences = os.popen(cmd).read()

    if input_type == "-f":
        sentences = sentences[21:]

    sentences = parse(sentences)

    for sentence in sentences:
        sentence_list = []
        for word in sentence:
            sentence_list.append([word["form"], word["lemma"]])
        result.append(sentence_list)

    return result

