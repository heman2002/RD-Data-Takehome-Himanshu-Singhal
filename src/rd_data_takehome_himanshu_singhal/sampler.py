"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = rd_data_takehome_himanshu_singhal.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
#import logging
import sys
import pandas as pd
import numpy as np
import os.path
import re
#from rd_data_takehome_himanshu_singhal import __version__

__author__ = "Himanshu Singhal"
__copyright__ = "Himanshu Singhal"
__license__ = "MIT"

#_logger = logging.getLogger(__name__)


np.random.seed(0)

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from rd_data_takehome_himanshu_singhal.sampler import sample_data`,
# when using this Python module as a library.

def validate_arguments(dataset_file, dataset_size, columns, column_weights):
    """This function takes the dataset_file containing the metadata, the size of the data to be returned, 
    the columns for stratification and the weights of the labels corresponding to each column and checks for validaity of the arguments
    Arguments:
        dataset_file: file containing the metadata of all files in the data lake
        dataset_size: size of the sampled data to be generated
        columns: list of columns that have the constraint for stratification
        column_weights: list of dictionaries containing the label weightage pairs provided for stratification constraint 
    """
    file_ext = dataset_file.split('.')[-1]
    
    if not os.path.isfile(dataset_file) and file_ext == 'csv':
        raise FileNotFoundError('Invalid file path or type')
    
    df = pd.read_csv(dataset_file)
    if dataset_size > df.shape[0]:
        raise ValueError('Sampling size greater than dataset size')
    
    for col, weight in zip(columns, column_weights):
        total_w = 0
        if col not in df.columns:
            raise ValueError('Invalid column provided for stratification')
        for label, w in weight.items():
            if label not in df[col].unique():
                raise ValueError('Invalid label column provided for stratification')
            total_w += w

        if total_w != 1.0:
            raise ValueError('Weights for column stratification are invalid')

def parse_stratification(stratification):
    """This function takes stratification as an argument and parses the string to identify the columns and the corresponding label value pairs to sample the data

    Arguments:

        stratification: string containing all the stratification constraints given in the format
        <column>: <weightage> <label>, <weightage> <label>; <column>: <weightage> <label>, <weightage> <label>

    Returns:
        columns: list of columns parsed
        column_weights: list of dictionaries with labels as the key and their corresponding weightage as the value
    """

    if stratification == "":
        return [],[]
    
    columns = []
    column_weights = []

    try:
        semicolon_split = stratification.strip().split(';')
        for semi_split in semicolon_split:
            colon_split = semi_split.strip().split(':')
            column = colon_split[0].strip()
            weights_split = colon_split[1].strip().split(',')
            weights = {}
            for sp in weights_split:
                label_split = sp.strip().split(' ')
                weight = float(label_split[0])
                label = label_split[1]
                weights[label] = weight
            
            columns.append(column)
            column_weights.append(weights)
    except:
        raise ValueError("Invalid stratification provided")
    
    #print(weights)
    return columns, column_weights


def sample_data_col(dataset_file, dataset_size, column, weights):
    """
    This function works only for one column leveraging group by functionality and does not work for multiple columns, hence not used.
    This function takes the dataset_file containing the metadata, the size of the data to be returned, 
    the column for stratification and the weights of the labels corresponding to the column
    Arguments:
        dataset_file: file containing the metadata of all files in the data lake
        dataset_size: size of the sampled data to be generated
        column: column that has the constraint for stratification
        weights: dictionary containing the label weightage pairs provided for stratification constraint

    Returns:
        sampled_data: csv file containing the data that has been sampled for the given dataset size
    """
    df = pd.read_csv(dataset_file)

    sampled_data = df.groupby(column, group_keys=False).apply(lambda x: x.sample(n=int(dataset_size*weights.get(x[column].iloc[0], 0)), random_state=0))

    return sampled_data


def sample_data(dataset_file, dataset_size, columns, column_weights):
    """This function takes the dataset_file containing the metadata, the size of the data to be returned, 
    the columns for stratification and the weights of the labels corresponding to each column and samples the data
    Arguments:
        dataset_file: file containing the metadata of all files in the data lake
        dataset_size: size of the sampled data to be generated
        columns: list of columns that have the constraint for stratification
        column_weights: list of dictionaries containing the label weightage pairs provided for stratification constraint

    Returns:
        sampled_data: csv file containing the data that has been sampled for the given dataset size
    """
    df = pd.read_csv(dataset_file)
    
    # Business logic to assign weights based on each column weightage provided by the user. Initially each record has an equal weight of 1.
    # For each record the weight is calculated by multiplying individual column label weights to achieve an overall weight.

    weights = np.ones(df.shape[0])
    for ind in range(df.shape[0]):
        for col_ind, col in enumerate(columns):
            col_weight = column_weights[col_ind]
            if df[col].iloc[ind] in col_weight:
                weights[ind] *= col_weight[df[col].iloc[ind]]
            else:
                weights[ind] = 0
    
    probabilities = weights / weights.sum()
    
    try:
        sampled_indices = np.random.choice(df.index, size=dataset_size, replace=False, p=probabilities)
        sampled_data = df.loc[sampled_indices]
    except:
        raise ValueError('Given stratification constraints cannot be satisfied for the given dataset')    

    # sampled_data = df.groupby(columns, group_keys=False).apply(lambda x: print(((x, [weights.get(x[column].iloc[0], 0) for column, weights in zip(columns, column_weights)]))))
    return sampled_data


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Argument parser for Sampler")
    parser.add_argument("file", type=str, help="csv file containing metadata of all items in data lake")
    parser.add_argument("-s", "--size", type=int, help="size of the dataset after sampling", default=100)
    parser.add_argument("-strat", "--stratification", type=str, help="stratification to be applied for sampling, expected format is <column>: <weightage> <label>, <weightage> <label>; <column>: <weightage> <label>, <weightage> <label>", default="")
    parser.add_argument("-o", "--output_file", type=str, help="output file where the sampled data is to be stored in", default="Sample_data.csv")
    return parser.parse_args(args)


def main(args):
    """Wrapper allowing :func:`sample_data` to be called with string arguments in a CLI fashion

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    columns, column_weights = parse_stratification(args.stratification)
    validate_arguments(args.file, args.size, columns, column_weights)
    sampled_data = sample_data(args.file, args.size, columns, column_weights)
    sampled_data.to_csv(args.output_file)
    #print(sampled_data)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m rd_data_takehome_himanshu_singhal.sampler
    #
    run()
