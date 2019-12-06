import os

import pytest

import compas
from compas.files import STL

compas.PRECISION = '12f'

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def binary_stl_with_ascii_header():
    return os.path.join(BASE_FOLDER, 'fixtures', 'binary_w_ascii_header.stl')


@pytest.fixture
def cube_binary():
    return os.path.join(BASE_FOLDER, 'fixtures', 'cube_binary.stl')


@pytest.fixture
def cube_ascii():
    return os.path.join(BASE_FOLDER, 'fixtures', 'cube_ascii.stl')


def test_parse_binary_stl(cube_binary):
    stl = STL(cube_binary)
    assert len(stl.parser.vertices) > 0


def test_parse_ascii_stl(cube_ascii):
    stl = STL(cube_ascii)
    assert len(stl.parser.vertices) > 0


def test_parse_binary_w_ascii_header(binary_stl_with_ascii_header):
    stl = STL(binary_stl_with_ascii_header)
    assert len(stl.parser.vertices) > 0
