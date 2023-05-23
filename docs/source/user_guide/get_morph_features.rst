.. _get_morph_features:

**************************
Get Morphological Features
**************************

.. currentmodule:: aksara

:class:`MorphologicalFeature` class can be used to get all morphological features of each token in an 
Indonesian text. :class:`MorphologicalFeature` has 2 public functions: :func:`MorphologicalFeature.get_feature` and
:func:`MorphologicalFeature.get_feature_to_file`. These 2 methods only differ on their output format.
:func:`get_feature` will return a list of list of tuple, whereas :func:`get_feature_to_file` will save the morphological features
in a file and return the file's absolute path. 

Both :class:`MorphologicalFeature` methods can get the text from a Python str or file.

.. change working directory from docs/ to docs/data/

.. ipython:: python
    :suppress:

    import os
    os.chdir('data')


Text as Python str
------------------
If the text is in Python str, then we can directly pass it to :func:`get_feature` to get the morphological features of each tokens in 
the text.

.. ipython:: python
    :okwarning:

    from aksara import MorphologicalFeature
    features_getter = MorphologicalFeature()
    features_getter.get_feature('besok pagi aku harus bekerja')


Text is in file
---------------
If the text is in a file, you can pass ``input_mode='f'`` in :func:`get_feature`. Suppose we want to get all morphological Features
in a ``formal_text.txt`` file.

This is the text inside ``formal_text.txt`` file.

.. ipython:: python
    :okwarning:

    with open('formal_text.txt', 'r') as file:
        print(file.read())

Next, we pass the file path (``formal_text.txt``) and ``input_mode='f'`` in :func:`get_feature`.

.. ipython:: python
    :okwarning:

    features_getter.get_feature('formal_text.txt', input_mode='f')



Save the result in a file
-------------------------
If the result want to be saved in a file, then :func:`get_feature_to_file` can be used. In term of parameters,
:func:`get_feature_to_file` is pretty similar to :func:`get_feature`. The only the difference between them is :func:`get_feature_to_file`
requires a file path to save the result.

The following example show how to use :func:`get_feature_to_file`.

Suppose we will save the result in ``out.txt`` file.

.. ipython:: python 
    :okwarning:

    from aksara import MorphologicalFeature
    features_getter = MorphologicalFeature()
    features_getter.get_feature_to_file('Biarlah Ani menyelesaikan tugasnya', 'out.txt')

This is the ``out.txt`` content.

.. ipython:: python
    :okwarning:

    with open('out.txt', 'r') as file:
        print(file.read())


If the text is in a file, then you can use ``input_mode='f'`` similar to :func:`get_feature` function.

.. ipython:: python 
    :okwarning:

    # read the text from 'formal_text.txt' then save the result in 'out2.txt'
    features_getter.get_feature_to_file(
        'formal_text.txt',
        'out2.txt',
        input_mode='f'
    )


Handle Informal Text
--------------------
If some words in the text are informal, you can tell :func:`get_feature` and :func:`get_feature_to_file` to handle informal words.
This can be done by setting the keyword argument ``is_informal`` to True.

.. ipython:: python
    :okwarning:

    from aksara import MorphologicalFeature
    features_getter = MorphologicalFeature()
    features_getter.get_feature('gw pengen pergi sekolah', is_informal=True)


.. cleanup generated file

.. ipython:: python
    :suppress:

    import os
    os.remove('out.txt')
    os.remove('out2.txt')

.. ipython:: python
    :suppress:

    import os
    os.chdir('..')
