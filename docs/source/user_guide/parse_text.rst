.. _parse_text:

**********
Parse Text
**********

.. currentmodule:: aksara

To parse an Indonesian text, Aksara provides two options for input: you can either give
the text as a string or read text from a file. Additionally, Aksara provides two
to get the result as list of lists of :class:`ConlluData` or save it to a file in the
CoNLL-U format.

The :class:`DependencyParser` class is a parser that available in ``aksara`` namespace
that can be used to parse text with specified model. Currently, there are eight models, such as
FR_GSD-ID_CSUI (default), FR_GSD-ID_GSD, IT_ISDT-ID_CSUI, IT_ISDT-ID_GSD, EN_GUM-ID_CSUI, EN_GUM-ID_GSD.

Parse Text from String
----------------------
If you have the text as a string, you can use :meth:`DependencyParse.parse` with ``input_mode``
which is by default is set to 's'.

.. ipython:: python
    :okwarning:

    from aksara import DependencyParser
    parser = DependencyParser()
    result = parser.parse("Apa yang kamu inginkan? Saya ingin makan.")
    for sentence in result:
        for conllu_word in sentence:
            print(conllu_word)

Parse Text from File
--------------------
If you have file containing text that want to be parsed, you can use :meth:`DependencyParse.parse`
with ``input_mode`` is set to 'f'.

.. ipython:: python
    :okwarning:

    from aksara import DependencyParser
    parser = DependencyParser()
    result = parser.parse("data/formal_text.txt", input_mode='f')
    for sentence in result:
        for conllu_word in sentence:
            print(conllu_word)

Save Parsing Result to File
---------------------------
To save the result of dependency parsing a text to a file, use the :meth:`DependencyParse.parse_to_file`
and provide the file path for the output in ``write_path``. The result will be saved in `CoNLL-U <https://universaldependencies.org/format.html>`_
format. The text input can be provided as a string or read from a file.

.. ipython:: python
    :okwarning:

    from aksara import DependencyParser
    parser = DependencyParser()
    result = parser.parse_to_file("Apa yang kamu inginkan? Saya ingin makan.", write_path="data/output.txt", write_mode="w")
    with open("data/output.txt") as result_file:
        lines = result_file.readlines()
        for line in lines:
            print(line, end='')

.. ipython:: python
    :suppress:
    import os
    os.remove("data/output.txt")
