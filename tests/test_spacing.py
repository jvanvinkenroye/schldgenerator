import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from schildGenerator import SchildGenerator


def test_calculate_spacing_single_column():
    gen = SchildGenerator()
    gen.config['spalten'] = 1
    h, v = gen._calculate_spacing()
    assert h == 0


def test_calculate_spacing_single_row():
    gen = SchildGenerator()
    gen.config['zeilen'] = 1
    h, v = gen._calculate_spacing()
    assert v == 0
