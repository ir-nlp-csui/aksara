.. _pos_tagging:

***********
POS Tagging
***********

.. currentmodule:: aksara

Aksara provides a part-of-speech tagging (POS Tagging) processor in the form of
the :class:`POSTagger` class. The processor reads text from a string or a file
and outputs the corresponding part-of-speech tag according to the position of each word 
in their sentence. 

The part-of-speech tagging result will be stored as a list of sentences,
with each sentence containing a tuple pair of the original word and its POS tag.
Alternatively, the result could be saved in a text file in `CoNLL-U <https://universaldependencies.org/format.html>`_ format.

POS Tagging from String
-----------------------
If the input text is a string, you can use :meth:`POSTagger.tag` 
with ``input_mode``set to 's', which is the default.

.. ipython:: python
    :okwarning:

    from aksara import POSTagger
    tagger = POSTagger()
    result = tagger.tag("Tidak usah banyak berpikir. Biarlah saja semua terjadi.")
    print(result)

POS Tagging from File
---------------------
If the input text is contained in a file, you can use :meth:`POSTagger.tag` 
with ``input_mode``set to 'f'.

.. ipython:: python
    :okwarning:

    from aksara import POSTagger
    tagger = POSTagger()
    result = tagger.tag("data/formal_text.txt", input_mode='f')
    print(result)

Save POS Tagging Result to File
-------------------------------
To save the POS tagging result to a text file, use the :meth:`POSTagger.tag_to_file` method.
The ``write_path`` parameter is required to determine the path for the output file 
which will be stored in `CoNLL-U <https://universaldependencies.org/format.html>`_
format. The text input can be provided as a string or as a file.

.. ipython:: python
    :okwarning:

    from aksara import POSTagger
    tagger = POSTagger()
    result = tagger.tag_to_file("Tidak usah banyak berpikir. Biarlah saja semua terjadi.", write_path="data/output.txt", write_mode="w")
    with open("data/output.txt") as result_file:
        lines = result_file.readlines()
        for line in lines:
            print(line, end='')

.. ipython:: python
    :suppress:

    import os

    os.remove('data/output.txt')
