from src.problem_bank_helpers import __version__
from src.problem_bank_helpers import problem_bank_helpers as pbh
from collections import defaultdict
import numpy as np
import sigfig
import pandas as pd
import os
import pytest

def test_version():
    assert __version__ == '0.1.13'

test_values = {"between0and1": 
                    [0.1,
                     0.12,
                     0.123,
                     0.1234,
                     0.12345,
                     0.123456,
                     0.1234567,
                     0.12345678,
                     0.123456789,
                     0.1234567891,
                     0.12345678912,
                     0.123456789123
                    ],
                "singleDigits":[
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9
                    ],
                "leadingZeros":[
                    0.1,
                    0.012,
                    0.00123,
                    0.0001234
                ],
                "trailingZeros":[
                    10,
                    1200,
                    123000,
                    12340000,
                    1234500000,
                ],
                "emptyDecimal":[
                    "1.",
                    "10.",
                    "100.",
                    "1000.",
                    "10000.",
                    "100000.",
                    "1000000.",
                    "10000000.",
                    "100000000."
                ],
                "zeroDecimal":[
                    "1.0",
                    "1.00",
                    "1.000",
                    "1.0000",
                    "1.00000",
                    "1.000000",
                    "1.0000000",
                    "1.00000000",
                    "1.000000000",
                    "1.0000000000"
                ],
                "largeNumbers":[
                    5,
                    55,
                    555,
                    5555,
                    11111,
                    111111,
                    1111111,
                    11111111
                ],
                "eFormat":[
                    "1e10",
                    "1.1e10",
                    "1.12e20",
                    "1.123e30"
                ]}

group_names = list(test_values.keys())

@pytest.fixture
def variables():
    inputs = test_values
    return inputs

# Test sigfigs function
@pytest.mark.parametrize(
    "test_group",
    group_names
)
def test_sigfigs(test_group, variables):
    for i, test_input in enumerate(variables[test_group]):
        test_input = str(test_input)
        if test_group == "sf":
            correct_sigfigs = i+1
        elif test_group == "between0and1":
            correct_sigfigs = i+1
        elif test_group == "singleDigits":
            correct_sigfigs = 1
        elif test_group == "leadingZeros":
            correct_sigfigs = i+1
        elif test_group == "trailingZeros":
            correct_sigfigs = i+1
        elif test_group == "emptyDecimal":
            correct_sigfigs = i+1
        elif test_group == "zeroDecimal":
            correct_sigfigs = i+2
        elif test_group == "largeNumbers":
            correct_sigfigs = i+1
        elif test_group == "eFormat":
            correct_sigfigs = i+1
        else:
            pytest.fail(f"test group is not defined (got: '{test_group}')")
        assert (pbh.sigfigs(test_input) == correct_sigfigs), f"input: {test_input}"
def test_sigfigsfail():
    with pytest.raises(Exception):
        pbh.sigfigs(float(1))


# Test round_sig function
@pytest.mark.parametrize(
    "test_input, expected_output",
    [(123456789, [100000000, 120000000, 123000000, 123500000, 123460000, 123457000, 123456800, 123456790, 123456789]),
     (0.123456789, [0.1, 0.12, 0.123, 0.1235, 0.12346, 0.123457, 0.1234568, 0.12345679, 0.123456789]),
     (0.1, [0.1, 0.10, 0.100, 0.1000, 0.10000, 0.100000, 0.1000000, 0.10000000, 0.100000000])]
)
def test_roundsig(test_input, expected_output):
    for i in range(9):
        assert (pbh.round_sig(test_input, i + 1) == expected_output[i])


@pytest.mark.parametrize('num, digits_after_decimal, expected_result', [
    (3.14159, 2, '3.14'),  # Test rounding a positive float to 2 digits after decimal
    (-2.71828, 2, '-2.72'),  # Test rounding a negative float to 2 digits after decimal
    (0, 2, '0.00'),  # Test rounding zero to 2 digits after decimal
    (123.456, 0, '123'),  # Test rounding a float to 0 digits after decimal
    (7.7777777, 2, '7.78'),  # Test rounding a float with more than 2 digits after decimal
    (9.99, 2, '9.99'),  # Test rounding a float with exactly 2 digits after decimal
    (2.555, 4, '2.5550'),  # Test rounding a float with fewer digits after decimal than specified
    (1.23456789, 6, '1.234568'),  # Test rounding a float with more digits after decimal than specified
    (1e18, 2, '1000000000000000000.00'),  # Test rounding a very large positive float
    (1e-18, 2, '0.00'),  # Test rounding a very small positive float (close to zero)
    (-1e18, 2, '-1000000000000000000.00'),  # Test rounding a very large negative float
    (-1e-18, 2, '-0.00'),  # Test rounding a very small negative float (close to zero)
    (1.999, 2, '2.00'),  # Test rounding up
    (2.001, 2, '2.00'),  # Test rounding down
    (1.555, 2, '1.56'),  # Test rounding halfway between two rounded values
    (-1.5, 2, '-2.00'),  # Test rounding halfway between negative and positive values
    (1234567890.123456789, 8, '1234567890.12345679'),  # Test rounding a float with a large number of digits before and after decimal
    (987.654321, -2, '1000.00'),  # Test rounding a float with a negative number of digits after decimal
    (42.123, 0, '42'),  # Test rounding a float with zero value for digits_after_decimal
    (True, 2, '1.00'),  # Test rounding a non-numeric input
    (10.00, 2, '10.00'),  # Test rounding a float that is already rounded to specified digits after decimal
])
def test_num_as_str(num, digits_after_decimal, expected_result):
    assert pbh.num_as_str(num, digits_after_decimal) == expected_result

def test_num_as_str_default_dp():
    """test default decimal places"""
    assert pbh.num_as_str(3.14159) == '3.14'

def test_num_as_str_invalid_args_kwargs():
    with pytest.raises(TypeError):
        pbh.num_as_str(123.45, 2, "args")  # Function should not accept *args

    with pytest.raises(TypeError):
        pbh.num_as_str(123.45, 2, digits_after_decimal=2)  # Function should not accept **kwargs


# Test roundp function
def test_roundp_with_overriden_sigfig_settings():
    """Test rounding a float with specified sigfigs"""
    assert pbh.roundp(123.456, sigfigs=2) == 120.0

def test_roundp_with_overriden_decimal_settings():
    """Test rounding an integer with specified decimals"""
    assert pbh.roundp(987, decimals=2) == 987.0

def test_roundp_with_default_settings():
    """Test rounding a string with default sigfigs"""
    assert pbh.roundp('99.8765') == '100'

def test_roundp_with_format_std():
    """Test rounding a float with format='std'"""
    assert pbh.roundp(0.123, format='std') == 0.12

def test_roundp_with_format_english():
    """Test rounding a float with format='English'"""
    assert pbh.roundp(12345.6789, format='English') == 12300.0

def test_roundp_format_sci():
    """Test rounding a float with format='sci'"""
    assert pbh.roundp(0.000123, format='sci') == '1.20e-04'

# Test round_str function
def test_roundstr():
    """Test passing a string as the argument"""
    assert pbh.round_str('Hello') == 'Hello'

def test_roundstr_default():
    """Test rounding a float without specifying sigfigs or format"""
    assert pbh.round_str(123.456) == '123'

def test_roundstr_overridden_sigfig_setting():
    """Test rounding a float with specified sigfigs"""
    assert pbh.round_str(123.456, sigfigs=2) == 120.0

def test_roundstr_with_format_english():
    """Test rounding a float with specified format='English'"""
    assert pbh.round_str(12345.6789, format='English') == 12300.0

def test_roundstr_with_format_sci():
    """Test rounding a float with specified format='sci'"""
    assert pbh.round_str(0.000123, format='sci') == '1.20e-04'

def test_roundstr_with_sigfig_std_format():
    """Test rounding a float with specified sigfigs and format='std'"""
    assert pbh.round_str(0.123, sigfigs=3, format='std') == 0.120

def test_roundstr_with_decimal_sci_format():
    """Test rounding an integer with specified decimals and format='sci'"""
    assert pbh.round_str(987, decimals=2, format='sci') == '9.87e+02'
