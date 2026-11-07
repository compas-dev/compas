from uuid import uuid4

import pytest

from compas.data import Data
from compas.datastructures import Graph
from compas.datastructures import VolMesh
from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Translation
from compas.scene import GraphObject
from compas.scene import GeometryObject
from compas.scene import Scene
from compas.scene import SceneNode
from compas.scene import SceneObject
from compas.scene import SceneOperationNotRegisteredError
from compas.scene import SceneStateError
from compas.scene import SceneStateField
from compas.scene import VolMeshObject
from compas.scene import get_sceneobject_cls
from compas.scene import register_scene_operation
from compas.scene.context import SCENEOBJECT_TYPES
from compas.scene.context import SCENE_OPERATIONS
import compas.scene.context as scene_context


@pytest.fixture
def operation_registry():
    original = {context: {cls: dict(operations) for cls, operations in types.items()} for context, types in SCENE_OPERATIONS.items()}
    discovered = scene_context._OPERATIONS_DISCOVERED
    SCENE_OPERATIONS.clear()
    scene_context._OPERATIONS_DISCOVERED = True
    yield
    SCENE_OPERATIONS.clear()
    SCENE_OPERATIONS.update(original)
    scene_context._OPERATIONS_DISCOVERED = discovered


def test_scene_add_returns_a_stable_semantic_type():
    box = Box()
    scene = Scene(context="Viewer")

    sceneobject = scene.add(box)

    assert type(sceneobject) is GeometryObject
    assert get_sceneobject_cls(box) is GeometryObject
    assert sceneobject.item is box


def test_scene_node_contains_hierarchy_only():
    scene = Scene()
    sceneobject = scene.add(Box(), name="Box", show=False)

    assert sceneobject.node.__data__ == {"object": str(sceneobject.guid), "children": []}
    assert not hasattr(sceneobject.node, "item_guid")
    assert not hasattr(sceneobject.node, "show")


def test_scene_uses_sceneobject_guid_as_sole_hierarchy_key():
    scene = Scene()
    parent = scene.add(Box())
    child = scene.add(Box(), parent=parent)

    assert scene.node(parent.guid).object_guid == parent.guid
    assert scene.node(child.guid).parent.object_guid == parent.guid
    assert child.parent is parent
    assert parent.children == (child,)


def test_scene_rejects_a_second_node_for_one_object():
    scene = Scene()
    sceneobject = scene.add(Box())

    with pytest.raises(ValueError, match="already belongs"):
        scene.add_object(sceneobject)


def test_remove_and_explicit_reattach_preserve_identity_and_state():
    scene = Scene()
    sceneobject = scene.add(Box(), name="Box", opacity=0.25, show=False)
    guid = sceneobject.guid

    scene.remove(sceneobject)
    assert sceneobject.scene is None
    assert sceneobject.guid == guid
    assert sceneobject.name == "Box"
    assert sceneobject.opacity == 0.25
    assert sceneobject.show is False

    other = Scene()
    other.add_object(sceneobject)
    assert sceneobject.scene is other
    assert sceneobject.guid == guid


def test_group_children_use_only_explicit_state():
    scene = Scene()
    group = scene.add_group("Group", show=False)
    child = group.add(Box())

    assert group.show is False
    assert child.show is True


def test_draw_and_clear_resolve_context_operations_by_mro(operation_registry):
    calls = []

    def draw(scene, sceneobject, runtime):
        calls.append(("draw", sceneobject.guid, runtime))
        return ["handle"]

    def clear(scene, sceneobject, runtime, resources):
        calls.append(("clear", sceneobject.guid, runtime, resources))

    register_scene_operation("Test", SceneObject, "draw", draw)
    register_scene_operation("Test", SceneObject, "clear", clear)
    scene = Scene(context="Test")
    sceneobject = scene.add(Box())

    assert sceneobject.draw(runtime="runtime") == ["handle"]
    sceneobject.clear(runtime="runtime")
    assert calls == [
        ("draw", sceneobject.guid, "runtime"),
        ("clear", sceneobject.guid, "runtime", ("handle",)),
    ]


def test_context_changes_do_not_replace_scene_objects(operation_registry):
    def draw(scene, sceneobject, runtime):
        return []

    register_scene_operation("A", SceneObject, "draw", draw)
    register_scene_operation("B", SceneObject, "draw", draw)
    scene = Scene(context="A")
    sceneobject = scene.add(Box())

    scene.draw(context="A")
    scene.draw(context="B")

    assert scene.object(sceneobject.guid) is sceneobject


def test_duplicate_scene_operation_registration_fails(operation_registry):
    def first(*args):
        return []

    def second(*args):
        return []

    register_scene_operation("Test", SceneObject, "draw", first)
    with pytest.raises(ValueError, match="already registered"):
        register_scene_operation("Test", SceneObject, "draw", second)


def test_missing_scene_operation_names_context_type_and_operation(operation_registry):
    scene = Scene(context="Missing")
    sceneobject = scene.add(Box())

    with pytest.raises(SceneOperationNotRegisteredError, match="draw.*GeometryObject.*Missing"):
        sceneobject.draw()


def test_scene_node_rejects_invalid_data():
    with pytest.raises(ValueError, match="UUID string"):
        SceneNode.__from_data__({"object": "invalid", "children": []})
    with pytest.raises(TypeError, match="children"):
        SceneNode.__from_data__({"object": str(uuid4()), "children": ()})


def test_remove_clears_resources_for_every_context(operation_registry):
    calls = []

    def draw(scene, sceneobject, runtime):
        return [f"{runtime}-handle"]

    def clear(scene, sceneobject, runtime, resources):
        calls.append((sceneobject.guid, runtime, resources))

    for context in ("A", "B"):
        register_scene_operation(context, SceneObject, "draw", draw)
        register_scene_operation(context, SceneObject, "clear", clear)
    scene = Scene(context=None, _detect_context=False)
    sceneobject = scene.add(Box())
    sceneobject.draw(context="A", runtime="a")
    sceneobject.draw(context="B", runtime="b")

    scene.remove(sceneobject)

    assert calls == [
        (sceneobject.guid, "a", ("a-handle",)),
        (sceneobject.guid, "b", ("b-handle",)),
    ]


def test_repeated_draw_clears_the_previous_resource_before_replacing_it(operation_registry):
    calls = []

    def draw(scene, sceneobject, runtime):
        calls.append(("draw", runtime))
        return [f"{runtime}-handle"]

    def clear(scene, sceneobject, runtime, resources):
        calls.append(("clear", runtime, resources))

    register_scene_operation("Test", SceneObject, "draw", draw)
    register_scene_operation("Test", SceneObject, "clear", clear)
    scene = Scene(context="Test")
    sceneobject = scene.add(Box())

    sceneobject.draw(runtime="first")
    sceneobject.draw(runtime="second")
    sceneobject.clear()

    assert calls == [
        ("draw", "first"),
        ("clear", "first", ("first-handle",)),
        ("draw", "second"),
        ("clear", "second", ("second-handle",)),
    ]


def test_clear_without_a_context_or_resources_is_backend_neutral():
    scene = Scene(context=None, _detect_context=False)
    scene.add(Box())

    scene.clear()

    assert scene.objects == []


def test_world_transformation_and_frame_setter_preserve_local_coordinates():
    scene = Scene()
    parent = scene.add(Box(), transformation=Translation.from_vector([1, 0, 0]))
    child = scene.add(Box(), parent=parent, transformation=Translation.from_vector([0, 2, 0]))
    assert child.frame.point == [1, 2, 0]

    child.frame = Frame([4, 5, 6], [1, 0, 0], [0, 1, 0])

    assert child.transformation.translation_vector == [3, 5, 6]
    assert child.frame.point == [4, 5, 6]


def test_graph_and_volmesh_coordinates_invalidate_on_ancestor_transform():
    graph = Graph()
    graph.add_node(0, x=0, y=0, z=0)
    volmesh = VolMesh.from_vertices_and_cells([[0, 0, 0]], [])
    scene = Scene()
    parent = scene.add_group("Parent")
    graphobject = scene.add(graph, parent=parent)
    volmeshobject = scene.add(volmesh, parent=parent)
    assert isinstance(graphobject, GraphObject)
    assert isinstance(volmeshobject, VolMeshObject)
    assert graphobject.node_xyz[0] == [0, 0, 0]
    assert volmeshobject.vertex_xyz[0] == [0, 0, 0]

    parent.transformation = Translation.from_vector([1, 2, 3])

    assert graphobject.node_xyz[0] == [1, 2, 3]
    assert volmeshobject.vertex_xyz[0] == [1, 2, 3]


def test_scene_state_field_declarations_are_fully_validated():
    class InvalidDefault(SceneObject):
        __scene_state_namespace__ = "test.invalid.default"
        __scene_state_fields__ = (SceneStateField("value", int, default=1),)

    class InvalidOmission(SceneObject):
        __scene_state_namespace__ = "test.invalid.omission"
        __scene_state_fields__ = (SceneStateField("value", int, required=False, omit_default=True),)

    class DuplicateAttribute(SceneObject):
        __scene_state_namespace__ = "test.duplicate.attribute"
        __scene_state_fields__ = (
            SceneStateField("one", int, attribute_name="value"),
            SceneStateField("two", int, attribute_name="value"),
        )

    with pytest.raises(SceneStateError, match="default and be required"):
        InvalidDefault.scene_state_fields()
    with pytest.raises(SceneStateError, match="undeclared default"):
        InvalidOmission.scene_state_fields()
    with pytest.raises(SceneStateError, match="Duplicate scene-state adapter attribute"):
        DuplicateAttribute.scene_state_fields()


def test_sceneobject_discovery_is_not_inferred_from_registry_emptiness(monkeypatch):
    class Item(Data):
        pass

    class ItemObject(SceneObject):
        pass

    original = dict(SCENEOBJECT_TYPES)
    discovered = scene_context._SCENEOBJECTS_DISCOVERED
    SCENEOBJECT_TYPES.clear()
    SCENEOBJECT_TYPES[Box] = GeometryObject
    scene_context._SCENEOBJECTS_DISCOVERED = False

    def discover():
        SCENEOBJECT_TYPES[Item] = ItemObject

    monkeypatch.setattr(scene_context, "register_scene_objects", discover)
    try:
        assert get_sceneobject_cls(Item()) is ItemObject
    finally:
        SCENEOBJECT_TYPES.clear()
        SCENEOBJECT_TYPES.update(original)
        scene_context._SCENEOBJECTS_DISCOVERED = discovered
