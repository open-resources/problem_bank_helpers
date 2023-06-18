from src.problem_bank_helpers import __version__
from src.problem_bank_helpers import problem_bank_helpers as pbh
from collections import defaultdict
import numpy as np
import pandas as pd
import os
import pytest
import csv

def test_version():
    assert __version__ == '0.1.13'

def validate_csv_file(csv_file):
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file)

    # Perform validation checks using pandas and csv module
    # Add your validation logic here
    # You can use pandas functions and csv module functions to perform the required checks

    # Example checks:
    # 1. Check if all required columns are present
    required_columns = ['column1', 'column2', 'column3']
    missing_columns = [col for col in required_columns if col not in df.columns]
    assert len(missing_columns) == 0, f"Missing columns: {missing_columns}"

    # 2. Check data types of specific columns
    expected_data_types = {'column1': int, 'column2': float}
    for column, data_type in expected_data_types.items():
        assert df[column].dtype == data_type, f"Invalid data type for column '{column}'"

    # Add more validation checks as needed

    # If all checks pass, return True indicating that the CSV file is valid
    return True

# Validate csv files
@pytest.mark.parametrize('name, columns',
    [('animals',[]),
     ('names',[]),
     ('jumpers',[]),
     ('manual_vehicles',[]),
     ('vehicles',[]),
     ('metals',[]),
])
def test_validate_csv():
    csv_file = 'path/to/test.csv'  # Path to the test CSV file

    # Call the validation function and assert that it returns True
    assert validate_csv_file(csv_file) == True

@pytest.mark.parametrize(
    "test_group",
    # perhaps group all csv imports in pbh in a list for maintainability
    [pbh.animals, pbh.names, pbh.jumpers, pbh.vehicles, pbh.manual_vehicles, pbh.metals, pbh.T_c]
)
def test_csv_imports(test_group):
    assert type(test_group) is list, f"this test group is not a list type"
