.. _lemmatization:

*************
Lemmatization
*************

.. currentmodule:: aksara

The :class:`Lemmatizer` class in Aksara serves the purpose of extracting the 
Indonesian lemma form from a given Indonesian word string or sentence list input.

:class:`Lemmatizer` has 2 public functions which are :func:`Lemmatizer.lemmatizer` and
:func:`Lemmatizer.lemmatizer_batch`. The :func:`Lemmatizer.lemmatizer` function will
accept a string of word which the function will then extract its lemma form in the form
of a string, or a list of tuple for certain types of words (ex. affixes), Whereas with the
:func:`Lemmatizer.lemmatizer_batch` function, it will accept a sentence in the form of
a list of string which the function will then extract the lemma form from each respective
string in the list. This function then generates a list of tuple, in which each tuple
contains both the original unlemmatized word and the lemmatized word form.

Lemmatize from string
---------------------
If the input is in a string form, then we can use the :func:`Lemmatizer.lemmatize` to
extract the lemmatized form of the input string.

.. ipython:: python
    :okwarning:

    from aksara import Lemmatizer
    lemmatizer = Lemmatizer()
    result = lemmatizer.lemmatize("Mengenakan")
    print(result)

Lemmatize from List
-------------------
If the input is in a list-of-string form, then we can use the :func:`Lemmatizer.lemmatize_batch`
to extract the lemmatized form of the list of string input.

.. ipython:: python
    :okwarning:

    from aksara import Lemmatizer
    lemmatizer = Lemmatizer()
    result = lemmatizer.lemmatize_batch(["Motor", "itu", "melaju", "dengan", "sangat", "kencang"])
    print(result)