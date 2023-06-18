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
                    1.,
                    10.,
                    100.,
                    1000.,
                    10000.,
                    100000.,
                    1000000.,
                    10000000.,
                    100000000.
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
                    "1e+10",
                    "1.1e+10",
                    "1.12e+20",
                    "1.123e+30"
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
    for i in range (0, len(variables[test_group])):
        test_input = str(variables[test_group][i])
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
            correct_sigfigs = 1
        elif test_group == "zeroDecimal":
            correct_sigfigs = i+2
        elif test_group == "largeNumbers":
            correct_sigfigs = i+1
        elif test_group == "eFormat":
            correct_sigfigs = i+1
        else:
            pytest.fail(f"test group is not defined (got: '{test_group}')")
        assert (pbh.sigfigs(test_input) == correct_sigfigs)


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

# Test num_as_str function
@pytest.mark.parametrize(
    "test_input, expected_output",
    [(123.456789000, ["123", "123.5", "123.46", "123.457", "123.4568", "123.45679", "123.456789", "123.4567890", "123.45678900", "123.456789000"]),
     (0.123456789, [0, 0.1, 0.12, 0.123, 0.1235, 0.12346, 0.123457, 0.1234568, 0.12345679, 0.123456789]),
     (0.000123456, [0, 0, 0, 0, 0.0001, 0.00012, 0.000123, 0.0001234, 0.00012345, 0.000123456]),
     (4.967489, ["5", "5.0", "4.97", "4.967", "4.9675", "4.96749", "4.967489", "4.9674890", "4.96748900", "4.967489000"])]
)
def test_numasstr(test_input, expected_output):
    if abs(test_input >= 1):
        for i in range(10):
            assert (pbh.num_as_str(test_input, i) == str(expected_output[i]))

# Test roundp function
def test_roundp():
    # Test rounding a float with specified sigfigs
    assert pbh.roundp(123.456, sigfigs=2) == 120.0

    # Test rounding an integer with specified decimals
    assert pbh.roundp(987, decimals=2) == 987.0

    # Test rounding a string with default sigfigs
    assert pbh.roundp('99.8765') == '100'

    # Test rounding a float with format='std'
    assert pbh.roundp(0.123, format='std') == 0.12

    # Test rounding a float with format='English'
    assert pbh.roundp(12345.6789, format='English') == 12300.0

    # Test rounding a float with format='sci'
    assert pbh.roundp(0.000123, format='sci') == '1.20e-04'

# Test round_str function
def test_roundstr():
    # Test passing a string as the argument
    assert pbh.round_str('Hello') == 'Hello'

    # Test rounding a float without specifying sigfigs or format
    assert pbh.round_str(123.456) == '123'

    # Test rounding a float with specified sigfigs
    assert pbh.round_str(123.456, sigfigs=2) == 120.0

    # Test rounding a float with specified format='English'
    assert pbh.round_str(12345.6789, format='English') == 12300.0

    # Test rounding a float with specified format='sci'
    assert pbh.round_str(0.000123, format='sci') == '1.20e-04'

    # Test rounding a float with specified sigfigs and format='std'
    assert pbh.round_str(0.123, sigfigs=3, format='std') == 0.120

    # Test rounding an integer with specified decimals and format='sci'
    assert pbh.round_str(987, decimals=2, format='sci') == '9.87e+02'
