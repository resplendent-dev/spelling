.. spelling documentation master file, created by
   sphinx-quickstart on Tue Jul 23 07:42:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation for Spelling - spell checker for CI!
================================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Running spelling
================

Running spelling should be as easy as:

.. code-block:: bash

   python -m pip install spelling
   cd <your_project>
   python -m spelling

Hopefully it will locate some valid spelling mistakes and perhaps some others
which whilst perhaps not dictionary words you would like to keep. See the
section on exemptions for how to deal with these so that you can get a
completely passing spell check to add as part of your CI process.

Exemptions
==========

If the spelling checker reports a spelling mistake which is actually a
deliberate choice an exemption can be made in a few ways:

* Words containing uppercase characters are assumed to be proper nouns and ignored.
* Escaping can be achieved through the use of back ticks \` around the word.
* Adding to a custom wordlist wordlist.txt or spelling\_wordlist.txt found in any sub-directory.
* Adding to the global wordlist https://github.com/resplendent-dev/unanimous

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

