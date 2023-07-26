from src.problem_bank_helpers import __version__
from src.problem_bank_helpers import problem_bank_helpers as pbh
import pytest

def test_version():
    assert __version__ == '0.1.14'

def idfn(input):
    if str(input)[0:3] == "id_":
        return input
    return ""

test_values = {"between0and1": 
                    ["0.1",
                     "0.12",
                     "0.123",
                     "0.1234",
                     "0.12345",
                     "0.123456",
                     "0.1234567",
                     "0.12345678",
                     "0.123456789",
                     "0.1234567891",
                     "0.12345678912",
                     "0.123456789123"
                    ],
                "singleDigits":[
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9"
                    ],
                "leadingZeros":[
                    "0.1",
                    "0.012",
                    "0.00123",
                    "0.0001234"
                ],
                "trailingZeros":[
                    "10",
                    "1200",
                    "123000",
                    "12340000",
                    "1234500000",
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
                    "1",
                    "11",
                    "111",
                    "1111",
                    "11111",
                    "111111",
                    "1111111",
                    "11111111",
                    "111111111",
                    "1111111111",
                    "11111111111",
                    "111111111111"
                ]
                , "eFormat":[
                    "1e10",
                    "1.1e10",
                    "1.12e10",
                    "1.123e10",
                    "1.1234e10",
                    "1.12345e10"]
                }

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
    """test many inputs for sigfig calculation"""
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
        assert (pbh.sigfigs(test_input) == correct_sigfigs), f"input: {test_input}, output: {pbh.sigfigs(test_input)}"

def test_sigfigs_floatinput_fail():
    with pytest.raises(Exception):
        pbh.sigfigs(float(1))


# Test round_sig function
@pytest.mark.parametrize('id, input, sigfigs, expected_result', [
    ('id_positive float',3.14159, 3, 3.14),  # Test rounding a positive float to 3 sigfigs
    ('id_negative float',-2.71828, 3, -2.72),  # Test rounding a negative float to 3 sigfigs
    ('id_zero float',0, 3, 0.00),  # Test rounding zero to 3 sigfigs
    ('id_float to 0 dp',123.456, 3, 123),  # Test rounding a float to 0 digits after decimal
    ('id_float with many digits',7.7777777, 3, 7.78),  # Test rounding a float with many digits after decimal
    ('id_same dp',9.99, 3, 9.99),  # Test rounding a float that is already correct
    ('id_more dp',2.555, 4, 2.5550),  # Test rounding a float with fewer digits after decimal than specified
    ('id_to fewer dp',1.23456789, 7, 1.234568),  # Test rounding a float with more digits after decimal than specified
    ('id_large positive float',1e18, 1, 1e18),  # Test rounding a very large positive float
    ('id_small positive float',1e-18, 1, 1e-18),  # Test rounding a very small positive float (close to zero)
    ('id_large negative float',-1e18, 1, -1e18),  # Test rounding a very large negative float
    ('id_small negative float',-1e-18, 1, -1e-18),  # Test rounding a very small negative float (close to zero)
    ('id_round up',1.999, 3, 2.00),  # Test rounding up
    ('id_round down',2.001, 3, 2.00),  # Test rounding down
    ('id_halfway between rounded values',1.555, 3, 1.56),  # Test rounding halfway between two rounded values
    ('id_halfway between negative values',-1.555, 3, -1.56),  # Test rounding halfway between negative and positive values
    ('id_many digits',1234567890.123456789, 18, 1234567890.12345679),  # Test rounding a float with a large number of digits before and after decimal
    ('id_same dp zeros',10.00, 2, 10),  # Test rounding a float that is already rounded to specified digits after decimal
    ],
    ids=idfn
)
def test_roundsig(id, input, sigfigs, expected_result):
    assert (pbh.round_sig(input, sigfigs) == expected_result)


#test num_as_str function
@pytest.mark.parametrize('id, input, digits_after_decimal, expected_result', [
    ('id_positive float',3.14159, 2, '3.14'),  # Test rounding a positive float to 2 digits after decimal
    ('id_negative float',-2.71828, 2, '-2.72'),  # Test rounding a negative float to 2 digits after decimal
    ('id_zero float',0, 2, '0.00'),  # Test rounding zero to 2 digits after decimal
    ('id_float to 0 dp',123.456, 0, '123'),  # Test rounding a float to 0 digits after decimal
    ('id_float with many digits',7.7777777, 2, '7.78'),  # Test rounding a float with more than 2 digits after decimal
    ('id_same dp',9.99, 2, '9.99'),  # Test rounding a float with exactly 2 digits after decimal
    ('id_more dp',2.555, 4, '2.5550'),  # Test rounding a float with fewer digits after decimal than specified
    ('id_to fewer dp',1.23456789, 6, '1.234568'),  # Test rounding a float with more digits after decimal than specified
    ('id_large positive float',1e18, 2, '1000000000000000000.00'),  # Test rounding a very large positive float
    ('id_small positive float',1e-18, 2, '0.00'),  # Test rounding a very small positive float (close to zero)
    ('id_large negative float',-1e18, 2, '-1000000000000000000.00'),  # Test rounding a very large negative float
    ('id_small negative float',-1e-18, 2, '-0.00'),  # Test rounding a very small negative float (close to zero)
    ('id_round up',1.999, 2, '2.00'),  # Test rounding up
    ('id_round down',2.001, 2, '2.00'),  # Test rounding down
    ('id_halfway between rounded values',1.555, 2, '1.56'),  # Test rounding halfway between two rounded values
    ('id_halfway between negative values',-1.555, 2, '-1.56'),  # Test rounding halfway between negative and positive values
    ('id_same dp zeros',10.00, 2, '10.00'),  # Test rounding a float that is already rounded to specified digits after decimal
    ],
    ids=idfn
)
def test_num_as_str(id, input, digits_after_decimal, expected_result):
    assert pbh.num_as_str(input, digits_after_decimal) == expected_result

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
    """Test rounding a float with specified decimals"""
    assert pbh.roundp(123.456, decimals=2) == 123.45

def test_roundp_with_overriden_sigfig_settings():
    """Test rounding an integer with specified decimals"""
    assert pbh.roundp(987, sigfigs=2) == 990

def test_roundp_with_overriden_decimal_settings():
    """Test rounding an integer with specified decimals"""
    assert pbh.roundp(987, decimals=2) == 987.00

def test_roundp_with_overriden_sigfig_settings():
    """Test rounding a string with default sigfigs"""
    assert pbh.roundp('99.8765', sigfigs=4) == '99.88'

def test_roundp_with_overriden_decimal_settings():
    """Test rounding a string with default sigfigs"""
    assert pbh.roundp('99.8765', decimals=2) == '99.88'

def test_roundp_with_default_settings():
    """Test rounding a string with default sigfigs"""
    assert pbh.roundp('99.8765') == '99.9'

def test_roundp_with_notation_std():
    """Test rounding a float with notation='std'"""
    assert pbh.roundp(0.123, notation='std') == 0.123

def test_roundp_notation_sci_default():
    """Test rounding a float with notation='sci'"""
    assert pbh.roundp('3679.14159', notation='scientific') == '3.68E3'

def test_roundp_notation_sci_sigfig():
    """Test rounding a float with notation='sci' and specified sigfigs"""
    assert pbh.roundp('3679.14159', sigfigs=6, notation='scientific') == '3.67914E3'

def test_roundp_notation_sci_dp():
    """Test rounding a float with notation='sci' and specified dps"""
    assert pbh.roundp('3679.14159', decimals=2, notation='scientific') == '3.67914E3'

@pytest.mark.parametrize('id, input, sigfigs, expected_result', [
    ('id_positive float',3.14159, 3, 3.14),  # Test rounding a positive float to 3 sigfigs
    ('id_negative float',-2.71828, 3, -2.72),  # Test rounding a negative float to 3 sigfigs
    ('id_zero float',0, 3, 0.00),  # Test rounding zero to 3 sigfigs
    ('id_float to 0 dp',123.456, 3, 123),  # Test rounding a float to 0 digits after decimal
    ('id_float with many digits',7.7777777, 3, 7.78),  # Test rounding a float with many digits after decimal
    ('id_same dp',9.99, 3, 9.99),  # Test rounding a float that is already correct
    ('id_more dp',2.555, 4, 2.5550),  # Test rounding a float with fewer digits after decimal than specified
    ('id_to fewer dp',1.23456789, 7, 1.234568),  # Test rounding a float with more digits after decimal than specified
    ('id_large positive float',1e30, 1, 1e30),  # Test rounding a very large positive float
    ('id_small positive float',1e-30, 1, 1e-30),  # Test rounding a very small positive float (close to zero)
    ('id_large negative float',-1e30, 1, -1e30),  # Test rounding a very large negative float
    ('id_small negative float',-1e-30, 1, -1e-30),  # Test rounding a very small negative float (close to zero)
    ('id_round up',1.999, 3, 2.00),  # Test rounding up
    ('id_round down',2.001, 3, 2.00),  # Test rounding down
    ('id_halfway between rounded values',1.555, 3, 1.56),  # Test rounding halfway between two rounded values
    ('id_halfway between negative values',-1.555, 3, -1.56),  # Test rounding halfway between negative and positive values
    ('id_many digits',1234567890.123456789, 18, 1234567890.12345679),  # Test rounding a float with a large number of digits before and after decimal
    ('id_same dp zeros',10.00, 2, 10),  # Test rounding a float that is already rounded to specified digits after decimal
    ],
    ids=idfn
)
def test_roundp_rigorous_sigfig(id, input, sigfigs, expected_result):
    assert pbh.roundp(input, sigfigs=sigfigs) == expected_result


# Test round_str function
def test_roundstr_str():
    """Test passing a string as the argument"""
    assert pbh.round_str('Hello') == 'Hello'

def test_roundstr_default_float():
    """Test rounding a float without specifying sigfigs or notation"""
    assert pbh.round_str(123.456) == 120

def test_roundstr_overridden_sigfig_setting():
    """Test rounding a float with specified sigfigs"""
    assert pbh.round_str(123.456, sigfigs=3) == 123.0

def test_roundstr_with_notation_sci():
    """Test rounding a float with specified notation='sci'"""
    assert pbh.round_str(0.000123, notation='sci') == 0.00012

def test_roundstr_with_sigfig_std_notation():
    """Test rounding a float with specified sigfigs and notation='std'"""
    assert pbh.round_str(0.1234, sigfigs=3, notation='std') == 0.123

def test_roundstr_with_decimal_sci_notation_dp():
    """Test rounding an integer with specified decimals and notation='sci'"""
    assert pbh.round_str(98767, decimals=2, notation='sci') == 99000

@pytest.mark.parametrize('id, input, sigfigs, expected_result', [
    ('id_positive float',3.14159, 3, 3.14),  # Test rounding a positive float to 3 sigfigs
    ('id_negative float',-2.71828, 3, -2.72),  # Test rounding a negative float to 3 sigfigs
    ('id_zero float',0, 3, 0.00),  # Test rounding zero to 3 sigfigs
    ('id_float to 0 dp',123.456, 3, 123),  # Test rounding a float to 0 digits after decimal
    ('id_float with many digits',7.7777777, 3, 7.78),  # Test rounding a float with many digits after decimal
    ('id_same dp',9.99, 3, 9.99),  # Test rounding a float that is already correct
    ('id_more dp',2.555, 4, 2.5550),  # Test rounding a float with fewer digits after decimal than specified
    ('id_to fewer dp',1.23456789, 7, 1.234568),  # Test rounding a float with more digits after decimal than specified
    ('id_large positive float',1e30, 1, 1e30),  # Test rounding a very large positive float
    ('id_small positive float',1e-30, 1, 1e-30),  # Test rounding a very small positive float (close to zero)
    ('id_large negative float',-1e30, 1, -1e30),  # Test rounding a very large negative float
    ('id_small negative float',-1e-30, 1, -1e-30),  # Test rounding a very small negative float (close to zero)
    ('id_round up',1.999, 3, 2.00),  # Test rounding up
    ('id_round down',2.001, 3, 2.00),  # Test rounding down
    ('id_halfway between rounded values',1.555, 3, 1.56),  # Test rounding halfway between two rounded values
    ('id_halfway between negative values',-1.555, 3, -1.56),  # Test rounding halfway between negative and positive values
    ('id_many digits',1234567890.123456789, 18, 1234567890.12345679),  # Test rounding a float with a large number of digits before and after decimal
    ('id_same dp zeros',10.00, 2, 10),  # Test rounding a float that is already rounded to specified digits after decimal
    ],
    ids=idfn
)
def test_roundstr_rigorous_sigfig(id, input, sigfigs, expected_result):
    assert pbh.round_str(input, sigfigs=sigfigs) == expected_result