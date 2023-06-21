.. Aksara documentation master file, created by
   sphinx-quickstart on Sun May  7 23:29:50 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Aksara's documentation!
==================================

:mod:`Aksara` is an Indonesian NLP tool that conforms to the `Universal Dependencies (UD) v2 <https://universaldependencies.org/>`__ annotation guidelines.
Aksara can perform **five tasks**:

.. hlist::
   :columns: 1

   * Word segmentation (tokenization)
   * Lemmatization
   * POS tagging
   * Morphological features analysis
   * Dependency Parsing

.. grid:: 2

    .. grid-item-card::

        User Guide
        ^^^^^^^^^^

        The user guide provides in-depth information on the key concepts of Aksara.

        +++

        .. button-ref:: user_guide
            :expand:
            :color: secondary
            :click-parent:

            To the user guide

    .. grid-item-card::

        API Reference
        ^^^^^^^^^^^^^

        The API reference provides a detailed description on the public API of Aksara library. The reference will 
        describes how the methods works and which parameters can be used.

        +++

        .. button-ref:: reference
            :expand:
            :color: secondary
            :click-parent:

            To the API reference

    .. grid-item-card::
        :margin: auto
        :padding: 3 0 0 0

        Contributor Guide
        ^^^^^^^^^^^^^^^^^^

        Find bugs and want to fix it? or want to improve Aksara Model or public API? This guide will provides information
        on how to improve Aksara.

        +++

        .. button-ref:: contributor_guide
            :expand:
            :color: secondary
            :click-parent:

            To the Contibutor Guide

.. toctree::
    :maxdepth: 3
    :hidden:
    :titlesonly:

    user_guide/index
    reference/index
    contributor_guide/index
