.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/RD-Data-Takehome-Himanshu-Singhal.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/RD-Data-Takehome-Himanshu-Singhal
    .. image:: https://readthedocs.org/projects/RD-Data-Takehome-Himanshu-Singhal/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://RD-Data-Takehome-Himanshu-Singhal.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/RD-Data-Takehome-Himanshu-Singhal/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/RD-Data-Takehome-Himanshu-Singhal
    .. image:: https://img.shields.io/pypi/v/RD-Data-Takehome-Himanshu-Singhal.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/RD-Data-Takehome-Himanshu-Singhal/
    .. image:: https://img.shields.io/conda/vn/conda-forge/RD-Data-Takehome-Himanshu-Singhal.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/RD-Data-Takehome-Himanshu-Singhal
    .. image:: https://pepy.tech/badge/RD-Data-Takehome-Himanshu-Singhal/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/RD-Data-Takehome-Himanshu-Singhal
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/RD-Data-Takehome-Himanshu-Singhal

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=================================
RD-Data-Takehome-Himanshu-Singhal
=================================


    Reality Defender Take Home test


Your task is to design and build a dataset sampling mechanism for creating small custom datasets from a larger data lake according to given specifications

SETUP
====

After cd-ing into your new project and creating (or activating) an isolated development environment (with virtualenv, conda or your preferred tool), you can do the usual editable install:

pip install -e .

We also recommend using tox, so you can take advantage of the automation tasks we have setup for you, like:

tox -e build  # to build package distribution

tox -e publish  # to test project uploads correctly in test.pypi.org

tox -e publish -- --repository pypi  # to release package to PyPI

tox -av  # to list all the tasks available

USAGE
====

The following command can be executed to run the program.

python -m sampler.py <arguments>

EXAMPLE
====

Below is an example command to execute the code.

python3 sampler.py DigiDB_digimonlist.csv -s 10 -strat 'Type: 0.7 Free, 0.3 Vaccine; Attribute: 0.5 Neutral, 0.5 Fire' -o Sampled_data.csv

CLI ARGUMENTS
====

The list below describes all the arguments that can be passed to the CLI.
usage: sampler.py [-h] [-s SIZE] [-strat STRATIFICATION] [-o OUTPUT_FILE] file

Argument parser for Sampler

positional arguments:
  file                  csv file containing metadata of all items in data lake

options:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  size of the dataset after sampling
  -strat STRATIFICATION, --stratification STRATIFICATION
                        stratification to be applied for sampling
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        output file where the sampled data is to be stored in
                        
TESTING
====

The command below can be used to execute the test cases.

pytest


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
