from src.problem_bank_helpers import __version__
from src.problem_bank_helpers import problem_bank_helpers as pbh
import pytest 
import random

def test_version():
    assert __version__ == '0.1.3'

@pytest.fixture
def variables():
    inputs = {"sf":[3, # 1sf at index 0
                    3.1, 
                    3.14, 
                    3.141,
                    3.1415, 
                    3.14159,
                    3.141592,
                    3.1415926,
                    3.14159265,
                    3.141592653,
                    3.1415926535,
                    3.14159265358,
                    3.141592653589],
               "between0and1": 
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
                     0.12345678912
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
                "leadingZeroes":[
                    0.1,
                    0.0012,
                    0.000123,
                    0.000001234,
                    0.00000012345,
                    0.000000123456
                ],
                "trailingZeroes":[
                    10,
                    1200,
                    123000,
                    12340000,
                    1234500000,
                    1234560000,
                    1234567000,
                    1234567800,
                    1234567890,
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
    return inputs


# sigfigs tests

def test_sigfigs_upto12dp(variables):
    for i in range (0, len(variables["sf"])):
        variable = str(variables["sf"][i])
        correct_sigfigs = i+1
        assert (pbh.sigfigs(variable) == correct_sigfigs)

def test_sigfigs_negative(variables):
    for i in range (0, len(variables["sf"])):
        variable = str(-1*variables["sf"][i])
        correct_sigfigs = i+1
        assert (pbh.sigfigs(variable) == correct_sigfigs)

def test_sigfigs_between0and1(variables):
    for i in range (0, len(variables["between0and1"])):
        variable = str(variables["between0and1"][i])
        correct_sigfigs = i+1
        assert (pbh.sigfigs(variable) == correct_sigfigs)

def test_sigfigs_single_digits(variables):
    assert (pbh.sigfigs("0") == 1)
    for i in range (1, len(variables["singleDigits"])):
        variable = str(variables["singleDigits"][i])
        correct_sigfigs = 1
        assert (pbh.sigfigs(variable) == correct_sigfigs)


def test_sigfigs_leading_zeroes(variables):
    for i in range (0, len(variables["leadingZeroes"])):
        variable = str(variables["leadingZeroes"][i])
        correct_sigfigs = i+1
        assert (pbh.sigfigs(variable)==correct_sigfigs)

def test_sigfigs_trailing_zeroes(variables):
    for i in range (0, len(variables["trailingZeroes"])):
        variable = str(variables["trailingZeroes"][i])
        correct_sigfigs = i+1
        assert (pbh.sigfigs(variable)==correct_sigfigs)


def test_sigfigs_empty_decimals(variables):
    for i in range (0, len(variables["emptyDecimal"])):
        variable = str(variables["emptyDecimal"][i])
        correct_sigfigs = i+2
        assert (pbh.sigfigs(variable)==correct_sigfigs)


def test_sigfigs_zero_decimals(variables):
    for i in range (0, len(variables["zeroDecimal"])):
        variable = str(variables["zeroDecimal"][i])
        correct_sigfigs = i+2
        assert (pbh.sigfigs(variable)==correct_sigfigs)
        

def test_sigfigs_large_numbers(variables):
    for i in range (0, len(variables["largeNumbers"])):
        variable = str(variables["largeNumbers"][i])
        correct_sigfigs = i+2
        assert (pbh.sigfigs(variable)==correct_sigfigs)


def test_sigfigs_eFormat(variables):
    for i in range (0, len(variables["eFormat"])):
        variable = str(variables["eFormat"][i])
        correct_sigfigs = i+1
        assert (pbh.sigfigs(variable)==correct_sigfigs)


# sign_str test


def test_sign_str_positive_int(variables):
    random_positive_ints = random.sample(range(1,100000000),50)
    for n in random_positive_ints:
        assert (pbh.sign_str(n) == " + ")

def test_sign_str_positive_float(variables):
    random_positive_floats = [ random.uniform(1,100000000) for i in range(50) ]
    for n in random_positive_floats:
        assert (pbh.sign_str(n) == " + ")
        

def test_sign_str_negative_int(variables):
    random_negative_ints = random.sample(range(-100000000,-1),50)
    for n in random_negative_ints:
        assert (pbh.sign_str(n) == " - ")

def test_sign_str_negative_float(variables):
    random_negative_floats = [ random.uniform(-100000000,-1) for i in range(50) ]
    for n in random_negative_floats:
        assert (pbh.sign_str(n) == " - ")

def test_sign_str_zero():
    assert (pbh.sign_str(0) == " + ")


# round_sig tests

def test_round_sig_zero():
    assert (pbh.round_sig(0,1) == 0)

def test_round_sig_trailing_zeroes(variables):
    for i in range (0, len(variables["trailingZeroes"])):
        variable = variables["trailingZeroes"][i]
        correct_sigfigs = i+1
        assert (pbh.round_sig(variable, correct_sigfigs) == variable)

# no way to test until passed as string since python rounds off floating point numbers and remove trailing zeroes
def test_round_sig_trailing_zeroes_decimal(variables):
    pass

def test_round_sig_single_digits(variables):
    for i in range (0, len(variables["singleDigits"])):
        variable = variables["singleDigits"][i]
        correct_sigfigs = i+1
        assert (pbh.round_sig(variable, correct_sigfigs) == variable)


def test_round_sig_multiple_sf_positive(variables):
    for i in range (0, len(variables["sf"])):
        variable = variables["sf"][i]
        correct_sigfigs = i+1
        assert (pbh.round_sig(variable, correct_sigfigs) == variable)

def test_round_sig_multiple_sf_negative(variables):
    for i in range (0, len(variables["sf"])):
        variable = -1*variables["sf"][i]
        correct_sigfigs = i+1
        assert (pbh.round_sig(variable, correct_sigfigs) == variable)


def test_round_sig_numbers_ending_with_n():
    for i in range(1,10):
        helper_test_round_sig_numbers_ending_with_n(i)

def helper_test_round_sig_numbers_ending_with_n(n):
    correction_factor = 10-n
    if(n < 5):
        correction_factor = -n
    start = n+10
    numbers = [i for i in range(start,10000,10)]
    for i in numbers:
        correct_rounded_number = i+correction_factor
        assert (pbh.round_sig(i, len(str(i))-1) == correct_rounded_number)

def test_round_sig_edge_cases():
    n = 4.967489
    answers = [4.967490, 4.967500, 4.968000, 4.970000, 5.000000, 5.000000]
    l = len(answers)
    for i in range(0, l):
        assert (pbh.round_sig(n, l-i) == answers[i])
     

# sigFigCheck tests

@pytest.fixture
def sigFigCheckVariables():
    inputs = { "units": "m/s",
               "var": "x",
    }   
    return inputs

def getCorrectString(correct_answer):
    correct_string = f"In scientific notation, $x =$ {correct_answer}m/s was submitted."   
    return correct_string

def test_sigFigCheck_None(sigFigCheckVariables):
    assert (pbh.sigFigCheck(None, sigFigCheckVariables["var"], sigFigCheckVariables["units"] ) == None)

def test_sigFigCheck_edge_cases(sigFigCheckVariables):
    edge_cases = [1e-4, 1e-3, 1e4, 1e12]
    for n in edge_cases:
        assert (pbh.sigFigCheck(n, sigFigCheckVariables["var"], sigFigCheckVariables["units"]) == None)


def test_sigFigCheck_between_1eMinus3_and_1e4(sigFigCheckVariables):
    for i in range(5,14):
        n = int("1e"+str(i))
        assert (pbh.sigFigCheck(n, sigFigCheckVariables["var"], sigFigCheckVariables["units"]) == None)


def test_sigFigCheck_lessThan1eMinus4(sigFigCheckVariables):
    numbers_lessThan1eMinus4 = [ random.uniform(1.e-100, 1.e-4) for i in range(50) ]
    for i in numbers_lessThan1eMinus4:
        assert (pbh.sigFigCheck(i, sigFigCheckVariables["var"], sigFigCheckVariables["units"]) == None)

def test_sigFigCheck_moreThan1e12(sigFigCheckVariables):
    numbers_moreThan1e12 = [ random.uniform((1.e12) + 1, 1.e100) for i in range(50) ]
    for i in numbers_moreThan1e12:
        assert (pbh.sigFigCheck(i, sigFigCheckVariables["var"], sigFigCheckVariables["units"]) == None)


def test_sigFigCheck_DecimalFormat(sigFigCheckVariables):
    numbers_decimalFormat = {1.5e4: "1.5e+04",
           1.5000e4: "1.5000e+04",
           1.56e5: "1.56e+05",
           15000.: "1.5000e+04"}
    for i in numbers_decimalFormat:
        assert (pbh.sigFigCheck(i, sigFigCheckVariables["var"], sigFigCheckVariables["units"]) == getCorrectString(numbers_decimalFormat[i]))

def test_sigFigCheck_between_1e4And1e12(sigFigCheckVariables):
    pass


def test_sigFigCheck_between_1eMinus3And1eMinus4(sigFigCheckVariables):
    pass





