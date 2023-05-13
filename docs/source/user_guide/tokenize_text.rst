.. _tokenize_text:

*************
Tokenize Text
*************

.. currentmodule:: aksara

To get all tokens from an Indonesian text, Aksara provides 2 classes that can be used depending on
whether you want to split multiword token or not.  

The :class:`BaseTokenizer` class is a tokenizer that does not handle multiword token. While the :class:`MultiwordTokenizer` will split
any multiword tokens. These 2 tokenizer classes are available in ``aksara`` namespace.


Ignore Multiword Token
----------------------

If you does not want to split any multiword token, you can use :class:`BaseTokenizer` class.
The following codes illustrate on how to import and use :class:`BaseTokenizer` class.

.. ipython:: python

    from aksara import BaseTokenizer
    tokenizer = BaseTokenizer()
    tokenizer.tokenize('Biarlah Ani menyelesaikan tugasnya')

Split Multiword Token
---------------------

To split all multiword token, you can use :class:`MultiwordTokenizer`.
In the following example 'Biarlah' is a multiword token. In the previuos example with :class:`BaseTokenizer`
'Biarlah' is not splitted, but :class:`MultiwordTokenizer` will split 'Biarlah' into 'Biar' + 'lah'.

.. ipython:: python 
    :okwarning:

    from aksara import MultiwordTokenizer
    multiword_tokenizer = MultiwordTokenizer()
    multiword_tokenizer.tokenize('Biarlah Ani menyelesaikan tugasnya')
