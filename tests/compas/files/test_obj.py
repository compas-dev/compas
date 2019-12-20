import os

import pytest

import compas
from compas.files.obj import OBJ, OBJParser, OBJReader

REPO_ROOT = os.path.join(os.path.dirname(compas.__file__), '../..')


@pytest.fixture
def boxes_obj():
    return os.path.join(REPO_ROOT, 'data', 'boxes.obj')


@pytest.fixture
def faces_obj():
    return os.path.join(REPO_ROOT, 'data', 'faces.obj')


def test_OBJReader(faces_obj):
    obj = OBJReader(faces_obj)

    assert obj.is_binary is False


def test_OBJParser(boxes_obj):
    obj = OBJParser(OBJReader(boxes_obj))

    assert len(obj.faces) == 48


def test_OBJ(boxes_obj):
    obj = OBJ(boxes_obj)

    assert len(obj.reader.vertices) == 192
