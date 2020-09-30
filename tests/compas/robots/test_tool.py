import os
import pytest

import compas
from compas.datastructures import Mesh
from compas.geometry import allclose
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas.robots import ToolModel


@pytest.fixture
def mesh():
    return Mesh.from_stl(compas.get('cone.stl'))


@pytest.fixture
def frame():
    return Frame([0.14, 0, 0], [0, 1, 0], [0, 0, 1])


def test_basic_tool_model(mesh, frame):
    tool = ToolModel(mesh, frame)
    assert tool.name == 'attached_tool'


def test_from_json():
    filepath = os.path.join(compas.DATA, "cone_tool.json")
    tool = ToolModel.from_json(filepath)
    assert tool.name == 'attached_tool'
    assert [link    .name for link in tool.iter_links()] == ['attached_tool_link']


def test_from_t0cf_to_tcf(mesh, frame):
    tool = ToolModel(mesh, frame)
    frames_t0cf = [Frame((-0.363, 0.003, -0.147), (0.388, -0.351, -0.852), (0.276, 0.926, -0.256))]
    result = tool.from_t0cf_to_tcf(frames_t0cf)
    expected = [Frame(Point(-0.309, -0.046, -0.266), Vector(0.276, 0.926, -0.256), Vector(0.879, -0.136, 0.456))]
    assert allclose(result[0], expected[0], tol=1e-03)


def test_from_tcf_to_t0cf(mesh, frame):
    tool = ToolModel(mesh, frame)
    frames_tcf = [Frame((-0.309, -0.046, -0.266), (0.276, 0.926, -0.256), (0.879, -0.136, 0.456))]
    result = tool.from_tcf_to_t0cf(frames_tcf)
    expected = [Frame(Point(-0.363, 0.003, -0.147), Vector(0.388, -0.351, -0.852), Vector(0.276, 0.926, -0.256))]
    assert allclose(result[0], expected[0], tol=1e-03)
