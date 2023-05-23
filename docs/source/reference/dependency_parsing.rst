.. _dependency_parsing:

==================
Dependency Parsing
==================

.. currentmodule:: aksara

Parse Text
~~~~~~~~~~

Parse a text from a string or file

.. autosummary::
    :toctree: generated/

    DependencyParser

Visualize Dependency Tree
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: generated/

    TreeDrawer

Dependency Tree Drawer Backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While :class:`TreeDrawer` can be regarded as the frontend, that is user only need to set the drawer and call :func:`draw`
and/or :func:`save_image`. The backend, which really draw and/or save the tree, is one of :class:`drawer.MatplotlibDrawer`
, :class:`drawer.PlotlyDrawer`, or subclass of :class:`drawer.AbstractDrawer`.

.. currentmodule:: aksara.dependency_tree
.. autosummary::
    :toctree: generated/

    drawer.AbstractDrawer
    drawer.MatplotlibDrawer
    drawer.PlotlyDrawer