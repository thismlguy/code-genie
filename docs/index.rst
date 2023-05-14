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
   Genie API <genie>
   Pipeline API <pipeline>
   Arguments API <arguments>
   Sources API <sources>
   Sinks API <sinks>
   Examples <examples>

code-genie will help you bring the power of chatGPT technology to your notebooks.

Look how easy it is to use::

   from code_genie import Genie
   df = load_your_df()
   genie = Genie(data=df)
   gr_miss = genie.plz("create a dataframe with number of missing values per column")
   gr_miss.result  # show the result of computation
   print(gr_miss.code)  # print the code which was generated
   genie.plz("make scatter plot of col1 vs col2").result  # directly make the plot without storing into interim variable

Get started with this `notebook`_.

.. _notebook: https://nbviewer.org/github/thismlguy/code-genie/blob/main/docs/notebooks/Starter.ipynb

Installation
------------

Install code-genie by running:

``pip install code_genie``


Note on Privacy & Security
------------
Privacy of your data is of primte importance. This library has been specifically designed to NOT share any part of your data with the Genie APIs.
Just the metadata about your data like name and types of columns of a pandas dataframe would be shared, which help in generating high quality results.


Features
--------

- Create functions from text and re-use them as you want
- No more spending hours searching for syntax on stack overflow

Contribute
----------

- Issue Tracker: https://github.com/thismlguy/code-genie/issues
- Source Code: https://github.com/thismlguy/code-genie
