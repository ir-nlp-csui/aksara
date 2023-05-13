.. _tokenization:

============
Tokenization
============

.. currentmodule:: aksara

Abstract Tokenizer
~~~~~~~~~~~~~~~~~~

Serves as a template for tokenizer. If you want to create your own tokenizer, you can subclassing this
class and implement ``tokenize`` method.

.. autosummary::
    :toctree: generated/

    AbstractTokenizer


Base Tokenizer
~~~~~~~~~~~~~~

Tokenize a text without splitting multiword tokens

.. autosummary::
    :toctree: generated/

    BaseTokenizer

Multiword Tokenizer
~~~~~~~~~~~~~~~~~~~

Tokenize a text and split multiword tokens (if exists)

.. autosummary::
    :toctree: generated/

    MultiwordTokenizer
    