.. _analyze_text:

************
Analyze Text
************

.. currentmodule:: aksara

:class:`MorphologicalAnalyzer` class can be used to get morphological analysis of
each token in an Indonesian text.

:class:`MorphologicalAnalyzer` has 2 public functions: :func:`MorphologicalAnalyzer.analyze` and
:func:`MorphologicalAnalyzer.analyze_to_file`. Both methods can get the text from a Python str or file.
The only difference between these two public functions is their output. The former method will return
a list of list of tuples, whereas the letter will save the result of morphological analysis to a file
and return the file's absolute path.

.. change working directory from docs/ to docs/data/

.. ipython:: python
    :suppress:

    import os
    os.chdir('data')


Analyze from string
-------------------
If the text is in string, then we can directly pass it to :func:`analyze` to get the analysis result of each token in
the text.

.. ipython:: python
    :okwarning:

    from aksara import MorphologicalAnalyzer
    analyzer = MorphologicalAnalyzer()
    analyzer.analyze('besok pagi aku harus bekerja')

Analyze from file
-----------------


If the text is in a file, you can pass the file path with ``input_mode='f'`` in :func:`analyze`.

Suppose we want the analysis results of the text in the ``formal_text.txt`` file.

This shows the text inside ``formal_text.txt`` file.

.. ipython:: python
    :okwarning:

    with open('formal_text.txt', 'r') as file:
        print(file.read())

Next, we pass the file path (``formal_text.txt``) and ``input_mode='f'`` in :func:`analyze`.

.. ipython:: python
    :okwarning:

    analyzer.analyze('formal_text.txt', input_mode='f')


Save analysis result to a file
------------------------------

If the analysis result wants to be saved to a file, then :func:`analyze_to_file` can be used. Regarding parameters,
:func:`analyze_to_file` is pretty similar to :func:`analyze`. The only difference between them is :func:`analyze_to_file`
requires an output file path to save the result.

The following example shows how to use :func:`analyze_to_file`.

Suppose we will save the result to ``out.txt`` file.

.. ipython:: python
    :okwarning:

    from aksara import MorphologicalAnalyzer
    analyzer = MorphologicalAnalyzer()
    analyzer.analyze_to_file('Biarlah Ani menyelesaikan tugasnya', 'out.txt')

This shows the ``out.txt`` content.

.. ipython:: python
    :okwarning:

    with open('out.txt', 'r') as file:
        print(file.read())


If the text is in a file, you can add the ``input_mode='f'`` parameter, similar to using the :func:`analyze` function with a file.

.. ipython:: python
    :okwarning:

    # read the text from 'formal_text.txt' then save the result to 'out2.txt'


    analyzer.analyze_to_file(
        'formal_text.txt',
        'out2.txt',
        input_mode='f'
    )

.. ipython:: python
    :suppress:

    import os
    os.remove('out.txt')
    os.remove('out2.txt')


Handle Informal Text
--------------------

If some words in the text are informal, then you can tell :func:`analyze` and :func:`analyze_to_file` to handle
informal words by setting the parameter ``is_informal`` to True.

.. ipython:: python
    :okwarning:

    from aksara import MorphologicalAnalyzer
    analyzer = MorphologicalAnalyzer()
    analyzer.analyze('gw pengen pergi sekolah', is_informal=True)

.. ipython:: python
    :suppress:

    import os
    os.chdir('..')