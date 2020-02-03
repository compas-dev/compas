import os

import pytest

import compas
from compas.files import GLTF

compas.PRECISION = '12f'

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def simple_gltf():
    return os.path.join(BASE_FOLDER, 'fixtures', 'SimpleMeshes.gltf')


@pytest.fixture
def embedded_gltf():
    return os.path.join(BASE_FOLDER, 'fixtures', 'SimpleMeshesEmbedded.gltf')


@pytest.fixture
def interleaved_glb():
    return os.path.join(BASE_FOLDER, 'fixtures', 'BoxInterleaved.glb')


@pytest.fixture
def indexless_gltf():
    return os.path.join(BASE_FOLDER, 'fixtures', 'TriangleWithoutIndices.gltf')


@pytest.fixture
def morph_gltf():
    return os.path.join(BASE_FOLDER, 'fixtures', 'SimpleMorph.gltf')


@pytest.fixture
def sparse_gltf():
    return os.path.join(BASE_FOLDER, 'fixtures', 'SimpleSparseAccessor.gltf')


def test_from_gltf_edges_loaded(simple_gltf, embedded_gltf, interleaved_glb, indexless_gltf, morph_gltf, sparse_gltf):
    gltf = GLTF(simple_gltf)
    assert len(gltf.parser.scenes[0].nodes) > 1

    gltf = GLTF(embedded_gltf)
    assert len(gltf.parser.scenes[0].nodes) > 1

    gltf = GLTF(interleaved_glb)
    assert len(gltf.parser.scenes[0].nodes) > 1
    assert len(gltf.parser.scenes[0].nodes[1].mesh_data.vertices) == 24

    gltf = GLTF(indexless_gltf)
    assert len(gltf.parser.scenes[0].nodes[0].mesh_data.vertices) > 0

    gltf = GLTF(morph_gltf)
    assert (0.5, 1.5, 0.0) in gltf.parser.scenes[0].nodes[0].mesh_data.vertices

    gltf = GLTF(sparse_gltf)
    assert (5.0, 4.0, 0.0) in gltf.parser.scenes[0].nodes[0].mesh_data.vertices
