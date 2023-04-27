.. code-genie documentation master file, created by
   sphinx-quickstart on Tue Apr 25 12:55:04 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to code-genie's documentation!
======================================

.. toctree::
   :maxdepth: 1
   :hidden:

   Home <self>
   API <api>
   Examples <examples>

code-genie will help you bring the power of chatGPT technology to your notebooks.

Look how easy it is to use::

   from code_genie import PandasGenie
   df = load_your_df()
   genie = PandasGenie(instructions="create a dataframe with number of missing values per column")
   df_missing = genie(df)

Find more examples in the `examples` folder.

Installation
------------

Install code-genie by running:

``pip install code_genie``

Features
--------

- Create functions from text and re-use them as you want
- No more spending hours searching for syntax on stack overflow

Contribute
----------

- Issue Tracker: https://github.com/thismlguy/code-genie/issues
- Source Code: https://github.com/thismlguy/code-genie
