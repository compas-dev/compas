import pytest

from compas.files import GLTFDocument
from compas.files.gltf.gltf_node import GLTFNode
from compas.files.gltf.data_classes import TextureData


def test_children_sequence_returns_values_and_respects_zero_index():
    content = GLTFDocument()
    scene = content.add_scene()
    first = scene.add_child("first")
    second = scene.add_child("second")

    assert scene.children.index(first.key) == 0
    assert scene.children.count(second.key) == 1
    assert scene.children.pop(0) == first.key
    assert list(scene.children) == [second.key]


def test_node_skin_validates_against_document_skins():
    content = GLTFDocument()
    node = GLTFNode(content)
    content.skins[3] = object()

    node.skin = 3

    assert node.skin == 3
    with pytest.raises(ValueError, match="skin 4"):
        node.skin = 4


def test_document_validation_rejects_cycles():
    content = GLTFDocument()
    first = GLTFNode(content)
    second = GLTFNode(content)
    first.children.append(second.key)
    second.children.append(first.key)

    with pytest.raises(ValueError, match="cycle"):
        content.validate()


def test_document_validation_rejects_multiple_parents():
    content = GLTFDocument()
    first = GLTFNode(content)
    second = GLTFNode(content)
    child = GLTFNode(content)
    first.children.append(child.key)
    second.children.append(child.key)

    with pytest.raises(ValueError, match="multiple parents"):
        content.validate()


def test_without_orphans_returns_cleaned_copy():
    content = GLTFDocument()
    scene = content.add_scene()
    scene.add_child("reachable")
    orphan = GLTFNode(content, "orphan")

    cleaned = content.without_orphans()

    assert orphan.key in content.nodes
    assert orphan.key not in cleaned.nodes


def test_document_validation_rejects_invalid_texture_references():
    content = GLTFDocument()
    content.textures[0] = TextureData(source=7)

    with pytest.raises(ValueError, match="image 7"):
        content.validate()


def test_document_validation_requires_required_extensions_to_be_used():
    content = GLTFDocument()
    content.extensions_required = ["EXT_example"]

    with pytest.raises(ValueError, match="extensionsUsed"):
        content.validate()
