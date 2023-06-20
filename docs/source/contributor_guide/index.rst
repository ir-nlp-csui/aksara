.. _contributor_guide:

==================
Contributor Guides
==================

Pull/merge requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Getting Aksara Source Code
==========================

You can get Aksara source code from our GitLab repository.

* Go to `https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2023/kelas-a/nlp/nlp-aksara <https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2023/kelas-a/nlp/nlp-aksara>`__. Click the fork button.

* Clone the forked repository to your local computer::

    git clone https:://gitlab.com/<your-username>/aksara.git

* Enter Aksara folder::

    cd aksara

* Add the upstream repository so that you can get the latest update from Aksara main repository::

    git remote add upstream https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2023/kelas-a/nlp/nlp-aksara


Setting Up Local Development
============================

After getting the source code, you need to install Aksara dependencies. Aksara has 3 dependency files: 

1. requirements.txt 
2. doc_requirements.txt
3. build_requirements.txt.

Note: It is strongly RECOMMENDED to use virtual environment to avoid dependency conflicts 
(See `Python venv <https://docs.python.org/3/library/venv.html>`__)

*   requirements.txt contains required dependencies to run all packages from Aksara. 
    If you only want to run Aksara test or import packages from Aksara then installing requirements.txt will be enough.

*   doc_requirements.txt contains dependencies to build Aksara documentation. (requirements.txt also need to be installed)

*   build_requirements.txt contains dependencies to create a Python distribution of Aksara. 

Apart from those 3 dependency files, you also need to install foma. 
    
*   Linux::
    
        apt-get install foma-bin

*   Windows
    
    * Get precompiled foma binary from `foma-zip <https://bitbucket.org/mhulden/foma/downloads/>`__

    * Unzip the precompiled foma binary
    
    * Add the win32 folder path (from precompiled foma zip) to environment variable PATH

*   MacOS::
    
        brew install foma


Testing
=======

All aksara unit tests can be found in tests folder. 
You can use coverage.py to run the test::

    coverage run -m unittest discover
    coverage report -m


Building Documentation
======================

*   Install the required dependencies (doc_requirements.txt and requirements.txt)::
    
        pip install -r requirements.txt
        pip install -r doc_requirements.txt

*   Use make command to build Aksara Docs::
    
        cd docs && make html

    The html version of Aksara docs will be generated in **docs/build/html** folder.
    Open **index.html** in **docs/build/html** with your favorite browser.

*   [Optional] If you want to test that all examples in our documentation are still in accordance 
    with Aksara code base, then you can run doctest using make command (run inside docs folder)::

        make doctest

Contributing to Aksara
======================

In Aksara, you can either contribute to our code base or documentation.

Code Base
~~~~~~~~~

Aksara has NLP and public API code base.

Before editing our code base, make sure all dependencies specified in requirements.txt have been installed.


NLP Code Base
^^^^^^^^^^^^^

NLP Code Base contains Python packages and files that will perform NLP task in Aksara. If you are a NLP developer and want 
to improve the worflow of our NLP Aksara, you can edit our NLP code base.

Aksara NLP code base is placed inside **aksara/_nlp_internal** folder.

Unfortunately, we don't have dedicated unit tests for our NLP code base. For now, you may use our public API unit test to test 
NLP Aksara Code Bases (Unit tests of Aksara public API are in **tests** folder).

IMPORTANT: Currently, majority of our public API depend on **analyze_sentence** function in **aksara/_nlp_internal/core.py**. 
So, if you edit the function signature and/or return value of **analyze_sentence**, 
please make sure that the changes will not break Aksara's public API.


Public API
^^^^^^^^^^

Aksara public APIs are python packages that can be imported directly in a Python program outside of Aksara. 
Almost all Python packages in aksara folder, except for **_nlp_internal** folder, are part of Aksara public API.

If you make changes in our Aksara public API, make sure that all unit tests are passed::

    coverage run unittest discover


Documentation
~~~~~~~~~~~~~

If you find typos or feel that the examples in our documentation are out-of-date, you can edit our documentation and 
create a merge/pull request. We use Sphinx as our documentation builder and reStructuredText. 
In addition, we use numpy-style for our public API documentation.

In general, Aksara has 3 documentations: User Guide, API Reference, and Contributor Guide.


User Guide
^^^^^^^^^^

All our User Guide templates are stored in **docs/source/user_guide**. 

API Reference
^^^^^^^^^^^^^

We use Sphinx autodoc and autosummary to generate our API Reference from docstring. As mentioned earlier, we use NumPy style for 
our public API. So, if you want to edit API Reference, you can edit the doctring in Aksara's functions, methods, or classes.

In addition, we also use custom templates (modified version of Numpy autosummary templates) for autosummary.
The templates can be found in **docs/source/_templates/autosummary**. 
The templates use syntax that similar to Django Templates.


Contributor Guide
^^^^^^^^^^^^^^^^^

If you want to edit this document, you can edit **docs/source/contributor_guide/index.rst**.
