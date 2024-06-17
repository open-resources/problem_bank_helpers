import pandas as pd
import pytest
import tempfile
import pathlib
import os

import problem_bank_helpers as pbh

files = sorted(
    [
        file.name
        for file in pathlib.Path(
            "src/problem_bank_helpers/data/"
        ).iterdir()
    ]
)

files = [("src/problem_bank_helpers/data/" + f) for f in files if f != 'empty.csv']


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
        # assert data.shape[1] == expected_num_cols

    except IOError:
        # Handle file loading errors appropriately
        pytest.fail(f"Error loading file: {file_path}")

    except pd.errors.ParserError:
        # Handle CSV parsing errors appropriately
        pytest.fail(f"Error parsing CSV file: {file_path}")


def test_empty_csv():
    try:
        # Create a temporary empty CSV file
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as csvfile:
            pass

        # Call the test_load_csv function with the temporary empty CSV file
        with pytest.raises(pd.errors.EmptyDataError):
            test_load_csv(csvfile.name)

    finally:
        # Clean up the temporary file after the test
        if csvfile:
            csvfile.close()
            os.remove(csvfile.name)


@pytest.mark.parametrize("file_path", files)
def test_missing_values(file_path):
    # Load the CSV file using pandas
    data = pd.read_csv(file_path)

    # Test for missing or null values
    assert data.isnull().sum().sum() == 0


def test_backticks_to_code_simple_invalid_params():
    case = {"params": {"part1": 1, "part2": {"ans1": {1}}}}
    pbh.backticks_to_code_tags(case)

def test_backticks_to_code_skip_invalid_params():
    """Test rounding an int with specified sigfigs"""
    data = {
        "params": {
            "part1": {
                "ans": { # /statement/option
                    "anything": {
                        "value": "This is a test"
                    },
                    "num": 1,
                    "another": {
                        "foo": False,
                    }
                },
                "option": 1,
                "statement": True,
                "something": 2,
            }
        },
    }

    pbh.backticks_to_code_tags(data)
