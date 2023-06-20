# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Aksara'
copyright = '2023, Aksara Team'
author = 'Aksara Team'
release = '1.4'

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'numpydoc',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx.ext.doctest',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
    "sphinx_plotly_directive",
]

templates_path = ['_templates']
exclude_patterns = []

master_doc = 'index'

# -- numpydoc configuration --------------------------------------------------
numpydoc_show_class_members=False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_sidebars = {
    "**": ["search-field.html", "sidebar-nav-bs.html", "sidebar-ethical-ads.html"]
}


# Configuration of sphinx.ext.coverage
coverage_show_missing_items = True

# plotly directive configuration
plotly_include_source = True
