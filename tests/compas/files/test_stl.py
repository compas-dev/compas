import os
import pytest
import compas
from compas.datastructures import Mesh
from compas.files import STL
from compas.tolerance import TOL

# Temporary change the global precision in the TOL class to 12
TOL.precision = 12

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def binary_stl_with_ascii_header():
    return os.path.join(BASE_FOLDER, "fixtures", "stl", "binary-1.stl")


@pytest.fixture
def binary_stl():
    return os.path.join(BASE_FOLDER, "fixtures", "stl", "binary-2.stl")


@pytest.fixture
def ascii_stl():
    return os.path.join(BASE_FOLDER, "fixtures", "stl", "ascii.stl")


def test_binary_detection(ascii_stl, binary_stl, binary_stl_with_ascii_header):
    stl = STL(ascii_stl)
    assert len(stl.parser.vertices) > 0

    stl = STL(binary_stl)
    assert len(stl.parser.vertices) > 0

    stl = STL(binary_stl_with_ascii_header)
    assert len(stl.parser.vertices) > 0


def test_binary_read_write_fidelity():
    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    fp = compas.get("cube_binary_2.stl")
    mesh.to_stl(fp, binary=True)
    mesh_2 = Mesh.from_stl(fp)
    assert mesh.adjacency == mesh_2.adjacency
    assert mesh.vertex == mesh_2.vertex


# Reset the precision to its default value
TOL.precision = TOL.PRECISION
