import pytest
import os

from rd_data_takehome_himanshu_singhal.sampler import validate_arguments, parse_stratification, sample_data, main

__author__ = "Himanshu Singhal"
__copyright__ = "Himanshu Singhal"
__license__ = "MIT"


def test_validate_arguments():
    """Unit Tests"""
    with pytest.raises(FileNotFoundError):
        validate_arguments('Digi.csv', 10, ['Type', 'Attribute'], [{'Free': 0.7, 'Vaccine': 0.3}, {'Neutral': 0.5, 'Fire': 0.5}])

    with pytest.raises(ValueError):
        validate_arguments('DigiDB_digimonlist.csv', 1000, ['Type', 'Attribute'], [{'Free': 0.7, 'Vaccine': 0.3}, {'Neutral': 0.5, 'Fire': 0.5}])

    with pytest.raises(ValueError):
        validate_arguments('DigiDB_digimonlist.csv', 10, ['Typ', 'Attribute'], [{'Free': 0.7, 'Vaccine': 0.3}, {'Neutral': 0.5, 'Fire': 0.5}])

    with pytest.raises(ValueError):
        validate_arguments('DigiDB_digimonlist.csv', 10, ['Type', 'Attribute'], [{'Free': 0.6, 'Vaccine': 0.3}, {'Neutral': 0.5, 'Fire': 0.5}])

    with pytest.raises(ValueError):
        validate_arguments('DigiDB_digimonlist.csv', 10, ['Type', 'Attribute'], [{'Free': 0.7, 'Vacci': 0.3}, {'Neutral': 0.5, 'Fire': 0.5}])

def test_parse_stratification():
    """Unit Tests"""
    columns, column_weights = parse_stratification('Type: 0.7 Free, 0.3 Vaccine; Attribute: 0.5 Neutral, 0.5 Fire')
    assert columns == ['Type', 'Attribute']
    assert column_weights == [{'Free': 0.7, 'Vaccine': 0.3}, {'Neutral': 0.5, 'Fire': 0.5}]

def test_sample_data():
    sampled_data = sample_data('DigiDB_digimonlist.csv', 10, ['Type', 'Attribute'], [{'Free': 0.7, 'Vaccine': 0.3}, {'Neutral': 0.5, 'Fire': 0.5}])
    assert sampled_data.shape[0] == 10

def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["DigiDB_digimonlist.csv"])
    assert os.path.isfile("Sample_data.csv")
    