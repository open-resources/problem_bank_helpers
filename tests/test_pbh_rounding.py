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


@pytest.mark.parametrize(
    "test_input, expected_output",
    []
)
def test_sigfigs(test_input, expected_output):
    assert pbh.sigfigs(test_input) == expected_output, "input: {" + test_input + "} did not match expected output: {" + expected_output + "}"


@pytest.mark.parametrize(
    "test_input, expected_output",
    []
)
def test_round_sig(test_input, expected_output):
    assert pbh.round_sig(test_input) == expected_output, "input: {" + test_input + "} did not match expected output: {" + expected_output + "}"


@pytest.mark.parametrize(
    "test_input, expected_output",
    []
)
def test_roundp(test_input, expected_output):
    assert pbh.roundp(test_input) == expected_output, "input: {" + test_input + "} did not match expected output: {" + expected_output + "}"


@pytest.mark.parametrize(
    "test_input, expected_output",
    []
)
def test_round_str(test_input, expected_output):
    assert pbh.round_str(test_input) == expected_output, "input: {" + test_input + "} did not match expected output: {" + expected_output + "}"


@pytest.mark.parametrize(
    "test_input, expected_output",
    []
)
def test_num_as_str(test_input, expected_output):
    assert pbh.num_as_str(test_input) == expected_output, "input: {" + test_input + "} did not match expected output: {" + expected_output + "}"