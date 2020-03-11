import os

import pytest

import compas
from compas.files import STL

compas.PRECISION = '12f'

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def binary_stl_with_ascii_header():
    return os.path.join(BASE_FOLDER, 'fixtures', 'binary-1.stl')


@pytest.fixture
def binary_stl():
    return os.path.join(BASE_FOLDER, 'fixtures', 'binary-2.stl')


@pytest.fixture
def ascii_stl():
    return os.path.join(BASE_FOLDER, 'fixtures', 'ascii.stl')


def test_binary_detection(ascii_stl, binary_stl, binary_stl_with_ascii_header):
    stl = STL(ascii_stl)
    assert len(stl.parser.vertices) > 0

    stl = STL(binary_stl)
    assert len(stl.parser.vertices) > 0

    stl = STL(binary_stl_with_ascii_header)
    assert len(stl.parser.vertices) > 0
