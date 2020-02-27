import json
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


@pytest.fixture
def animated_gltf():
    return os.path.join(BASE_FOLDER, 'fixtures', 'AnimatedMorphCube.glb')


@pytest.fixture
def textured_gltf():
    return os.path.join(BASE_FOLDER, 'fixtures', 'BoxTextured.glb')


def test_from_gltf_edges_loaded(
    simple_gltf,
    embedded_gltf,
    interleaved_glb,
    indexless_gltf,
    morph_gltf,
    sparse_gltf,
    animated_gltf,
    textured_gltf,
):
    gltf = GLTF(simple_gltf)
    assert len(gltf.parser.scenes[0].nodes) == 3

    exporter = gltf.exporter
    json.dumps(exporter._gltf_dict)
    assert len(exporter._gltf_dict['nodes']) == 2
    assert len(exporter._gltf_dict['meshes']) == 2
    assert len(exporter._buffer) == exporter._gltf_dict['buffers'][0]['byteLength']

    gltf = GLTF(embedded_gltf)
    assert len(gltf.parser.scenes[0].nodes) > 1

    exporter = gltf.exporter
    exporter.embed_data = True
    exporter.load()
    json.dumps(exporter._gltf_dict)
    assert exporter._gltf_dict['buffers'][0]['uri'].startswith('data')
    assert 'animations' not in exporter._gltf_dict
    assert 'materials' not in exporter._gltf_dict

    gltf = GLTF(interleaved_glb)
    assert len(gltf.parser.scenes[0].nodes) > 1
    assert len(gltf.parser.scenes[0].nodes[1].mesh_data.vertices) == 24

    gltf = GLTF(indexless_gltf)
    assert len(gltf.parser.scenes[0].nodes[0].mesh_data.vertices) > 0

    gltf = GLTF(morph_gltf)
    assert (0.5, 1.5, 0.0) in gltf.parser.scenes[0].nodes[0].mesh_data.vertices

    gltf = GLTF(sparse_gltf)
    assert (5.0, 4.0, 0.0) in gltf.parser.scenes[0].nodes[0].mesh_data.vertices

    gltf = GLTF(animated_gltf)
    gltf.read()
    assert len(gltf.ancillaries['animations']) > 0

    exporter = gltf.exporter
    json.dumps(exporter._gltf_dict)
    assert len(exporter._gltf_dict['animations']) > 0
    assert 'images' not in exporter._gltf_dict

    gltf = GLTF(textured_gltf)
    gltf.read()
    assert len(gltf.ancillaries['materials']) > 0

    exporter = gltf.exporter
    json.dumps(exporter._gltf_dict)
    assert len(exporter._gltf_dict['materials']) > 0
    assert len(exporter._gltf_dict['samplers']) > 0
    assert len(exporter._gltf_dict['images']) > 0
    assert len(exporter._gltf_dict['textures']) > 0
    assert 'animations' not in exporter._gltf_dict
