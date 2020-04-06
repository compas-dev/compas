import json
import os

import pytest

import compas
from compas.files import GLTF
from compas.files import GLTFContent

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


def test_simple_gltf(simple_gltf):
    gltf = GLTF(simple_gltf)
    gltf.read()
    assert len(gltf.content.scenes[0].children) == 2

    exporter = gltf.exporter
    json.dumps(exporter._gltf_dict)
    assert len(exporter._gltf_dict['nodes']) == 2
    assert len(exporter._gltf_dict['meshes']) == 1
    assert len(exporter._buffer) == exporter._gltf_dict['buffers'][0]['byteLength']


def test_embedded_gltf(embedded_gltf):
    gltf = GLTF(embedded_gltf)
    gltf.read()
    assert len(gltf.content.scenes[0].children) > 1

    exporter = gltf.exporter
    exporter.embed_data = True
    exporter.load()
    json.dumps(exporter._gltf_dict)
    assert exporter._gltf_dict['buffers'][0]['uri'].startswith('data')
    assert 'animations' not in exporter._gltf_dict
    assert 'materials' not in exporter._gltf_dict


def test_interleaved_glb(interleaved_glb):
    gltf = GLTF(interleaved_glb)
    gltf.read()
    assert len(gltf.content.nodes) == 2
    assert len(gltf.content.meshes[0].vertices) == 24


def test_indexless_gltf(indexless_gltf):
    gltf = GLTF(indexless_gltf)
    gltf.read()
    assert len(gltf.content.meshes[0].vertices) > 0


def test_morph_gltf(morph_gltf):
    gltf = GLTF(morph_gltf)
    gltf.read()
    assert (0.5, 1.5, 0.0) in gltf.content.meshes[0].vertices


def test_sparse_gltf(sparse_gltf):
    gltf = GLTF(sparse_gltf)
    gltf.read()
    assert (5.0, 4.0, 0.0) in gltf.content.meshes[0].vertices
    assert len(gltf.content.meshes[0].faces) > 0
    assert (5.0, 4.0, 0.0) in gltf.content.nodes[0].vertices


def test_animated_gltf(animated_gltf):
    gltf = GLTF(animated_gltf)
    gltf.read()
    assert len(gltf.content.animations) > 0

    exporter = gltf.exporter
    json.dumps(exporter._gltf_dict)
    assert len(exporter._gltf_dict['animations']) > 0
    assert 'images' not in exporter._gltf_dict


def test_textured_gltf(textured_gltf):
    gltf = GLTF(textured_gltf)
    gltf.read()
    assert len(gltf.content.materials) > 0

    exporter = gltf.exporter
    json.dumps(exporter._gltf_dict)
    assert len(exporter._gltf_dict['materials']) > 0
    assert len(exporter._gltf_dict['samplers']) > 0
    assert len(exporter._gltf_dict['images']) > 0
    assert len(exporter._gltf_dict['textures']) > 0
    assert 'animations' not in exporter._gltf_dict


def test_gltf_content():
    content = GLTFContent()
    scene = content.add_scene()
    assert len(content.scenes) == 1

    node_0 = scene.add_child()
    assert len(content.nodes) == 1
    assert len(scene.children) == 1
    assert len(node_0.children) == 0

    node_0.add_child()
    assert len(content.nodes) == 2
    assert len(node_0.children) == 1
    assert len(scene.nodes) == 2
    assert len(scene.positions_and_edges[0]) == 3

    node_0.children = []
    content.remove_orphans()
    assert len(node_0.children) == 0
    assert len(content.nodes) == 1
    assert len(scene.nodes) == 1
