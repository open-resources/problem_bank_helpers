from src.problem_bank_helpers import __version__
from src.problem_bank_helpers import problem_bank_helpers as pbh
from collections import defaultdict
import numpy as np
import pandas as pd
import os
import pytest
import pathlib
import csv

def test_version():
    assert __version__ == '0.1.13'

files = sorted(
    [
        file.name
        for file in pathlib.Path(
            "data/"
        ).iterdir()
    ]
)

files = [("data/" + f) for f in files if f != 'empty.csv']


@pytest.mark.parametrize("file_path", files)
def test_load_csv(file_path):
    try:
        # Load the CSV file using pandas
        data = pd.read_csv(file_path)

        # Assert that data is loaded successfully
        assert data is not None

        assert type(data) is pd.DataFrame

        # number of rows and columns:
        # assert data.shape[0] == expected_num_rows
        assert data.shape[1] == 1

    except IOError:
        # Handle file loading errors appropriately
        pytest.fail(f"Error loading file: {file_path}")

    except pd.errors.ParserError:
        # Handle CSV parsing errors appropriately
        pytest.fail(f"Error parsing CSV file: {file_path}")


def test_empty_csv():
    # Test loading an empty CSV file
    file_path = "data/empty.csv"

    # Create an empty CSV file
    with open(file_path, 'w') as csvfile:
        pass

    with pytest.raises(pd.errors.EmptyDataError):
        test_load_csv(file_path)


@pytest.mark.parametrize("file_path", files)
def test_missing_values(file_path):
    # Load the CSV file using pandas
    data = pd.read_csv(file_path)

    # Test for missing or null values
    assert data.isnull().sum().sum() == 0