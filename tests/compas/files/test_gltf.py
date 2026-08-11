from pathlib import Path

import pytest

from compas.files import GLTFDocument
from compas.files import GLTFEncoder
from compas.files import read_gltf


FIXTURES = Path(__file__).parent / "fixtures" / "gltf"


@pytest.mark.parametrize(
    ("filename", "collection"),
    [
        ("SimpleMeshes.gltf", "meshes"),
        ("SimpleMeshesEmbedded.gltf", "scenes"),
        ("BoxInterleaved.glb", "nodes"),
        ("TriangleWithoutIndices.gltf", "meshes"),
        ("SimpleMorph.gltf", "meshes"),
        ("SimpleSparseAccessor.gltf", "meshes"),
        ("AnimatedMorphCube.glb", "animations"),
        ("BoxTextured.glb", "materials"),
        ("SpecGlossVsMetalRough.glb", "materials"),
        ("SpecularTest.glb", "materials"),
    ],
)
def test_gltf_fixtures_parse_and_encode(filename, collection):
    document = read_gltf(FIXTURES / filename)
    payload = GLTFEncoder(format="glb").encode(document)

    assert getattr(document, collection)
    assert payload.json[collection]


def test_interleaved_vertices():
    document = read_gltf(FIXTURES / "BoxInterleaved.glb")

    assert len(document.meshes[0].vertices) == 24


def test_morph_and_sparse_vertices():
    morph = read_gltf(FIXTURES / "SimpleMorph.gltf")
    sparse = read_gltf(FIXTURES / "SimpleSparseAccessor.gltf")

    assert (0.5, 1.5, 0.0) in morph.meshes[0].vertices
    assert (5.0, 4.0, 0.0) in sparse.meshes[0].vertices
    assert (5.0, 4.0, 0.0) in sparse.nodes[0].vertices


def test_document_scene_editing():
    document = GLTFDocument()
    scene = document.add_scene()
    node = scene.add_child()
    node.add_child()

    assert len(document.nodes) == 2
    assert len(scene.nodes) == 2

    node.children = []
    document.remove_orphans()

    assert len(document.nodes) == 1
