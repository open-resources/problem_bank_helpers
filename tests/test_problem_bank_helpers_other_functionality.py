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
    "test_group",
    # perhaps group all csv imports in pbh in a list for maintainability
    [pbh.animals, pbh.names, pbh.jumpers, pbh.vehicles, pbh.manual_vehicles, pbh.metals, pbh.T_c]
)
def test_csv_imports(test_group):
    assert type(test_group) is list, f"this test group is not a list type"
