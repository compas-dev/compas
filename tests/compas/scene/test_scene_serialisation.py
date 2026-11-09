from uuid import uuid4

import pytest

from compas.geometry import Box
from compas.geometry import Translation
from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.datastructures import VolMesh
from compas.scene import GraphObject
from compas.scene import GeometryObject
from compas.scene import MeshObject
from compas.scene import FrameObject
from compas.scene import PlaneObject
from compas.scene import ShapeObject
from compas.scene import SurfaceObject
from compas.scene import VectorObject
from compas.scene import Scene
from compas.scene import SceneItemNotBoundError
from compas.scene import SceneObject
from compas.scene import SceneStateField
from compas.scene import TextAnnotation
from compas.scene import VolMeshObject


def test_scene_roundtrip_restores_stable_objects_and_hierarchy_without_items():
    scene = Scene("Reference only")
    parent_item = Box(1)
    child_item = Box(2)
    parent = scene.add(parent_item, name="Parent", show=False)
    scene.add(child_item, name="Child", parent=parent)
    parent.transformation = Translation.from_vector([1, 0, 0])

    restored = Scene.from_jsonstring(scene.to_jsonstring())

    restored_parent = restored.find_by_name("Parent")
    restored_child = restored.find_by_name("Child")
    assert isinstance(restored_parent, GeometryObject)
    assert restored_parent.guid == parent.guid
    assert restored_parent.show is False
    assert restored_parent.transformation == parent.transformation
    assert restored_child.parent is restored_parent
    assert restored.item_store == {}
    with pytest.raises(SceneItemNotBoundError, match=str(parent_item.guid)):
        _ = restored_parent.item


def test_independent_items_bind_with_shared_identity():
    box = Box()
    scene = Scene()
    scene.add(box, name="First")
    scene.add(box, name="Second")
    restored = Scene.from_jsonstring(scene.to_jsonstring())

    restored.bind(box)

    assert restored.objects[0].item is restored.objects[1].item is box


def test_scene_serialization_separates_objects_from_hierarchy():
    scene = Scene()
    box = scene.add(Box(), name="Box")
    data = scene.__data__

    assert data["version"] == 3
    assert [obj.guid for obj in data["objects"]] == [scene.root.guid, box.guid]
    assert data["annotations"] == []
    assert data["hierarchy"] == {
        "object": str(scene.root.guid),
        "children": [{"object": str(box.guid), "children": []}],
    }


def test_scene_serialization_keeps_ordered_annotations_outside_hierarchy():
    scene = Scene()
    first = scene.add_annotation(TextAnnotation("First", [0, 0, 0]))
    second = scene.add_annotation(TextAnnotation("Second", [1, 0, 0]), show=False)

    data = scene.__data__
    restored = Scene.from_jsonstring(scene.to_jsonstring())

    assert data["annotations"] == [first, second]
    assert [entry.guid for entry in restored.annotations] == [first.guid, second.guid]
    assert restored.annotations[1].show is False
    assert all(entry.guid not in restored.object_store for entry in restored.annotations)


def test_scene_schema_v3_is_a_clean_break():
    data = Scene().__data__
    data["version"] = 2

    with pytest.raises(ValueError, match="Unsupported scene schema version: 2"):
        Scene.__from_data__(data)


def test_unknown_namespaced_sceneobject_state_roundtrips():
    scene = Scene()
    obj = scene.add_reference(
        uuid4(),
        name="External",
        extensions={"org.example": {"value": 7}},
    )

    restored = Scene.from_jsonstring(scene.to_jsonstring())
    restored_obj = restored.object(obj.guid)

    assert restored_obj.__data__["extensions"] == {"org.example": {"value": 7}}


def test_scene_rejects_duplicate_hierarchy_references():
    scene = Scene()
    obj = scene.add(Box())
    data = scene.__data__
    data["hierarchy"]["children"].append({"object": str(obj.guid), "children": []})

    with pytest.raises(ValueError, match="more than once"):
        Scene.__from_data__(data)


def test_nested_groups_and_world_transform_roundtrip():
    scene = Scene("Nested")
    first = scene.add_group("First", transformation=Translation.from_vector([1, 0, 0]))
    second = scene.add_group("Second", parent=first, transformation=Translation.from_vector([0, 2, 0]))
    child = scene.add(Box(), parent=second, transformation=Translation.from_vector([0, 0, 3]))

    restored = Scene.from_jsonstring(scene.to_jsonstring())

    restored_child = restored.object(child.guid)
    assert restored_child.parent.name == "Second"
    assert restored_child.parent.parent.name == "First"
    assert restored_child.worldtransformation == child.worldtransformation


def test_replace_item_and_shared_item_pruning():
    shared = Box(1)
    replacement = Box(2)
    scene = Scene()
    first = scene.add(shared)
    second = scene.add(shared)

    scene.replace_item(first, replacement)
    assert shared.guid in scene.item_store
    scene.remove(second)

    assert shared.guid not in scene.item_store
    assert first.item is replacement


def test_bind_many_is_atomic():
    first = Box(1)
    second = Box(2)
    unknown = Box(3)
    scene = Scene()
    scene.add(first)
    scene.add(second)
    restored = Scene.from_jsonstring(scene.to_jsonstring())

    with pytest.raises(KeyError):
        restored.bind_many([first, unknown])

    assert restored.item_store == {}


def test_bind_rejects_a_distinct_item_with_the_same_guid():
    item = Box(1)
    duplicate = Box(2)
    duplicate._guid = item.guid
    scene = Scene()
    scene.add(item)
    restored = Scene.from_jsonstring(scene.to_jsonstring())
    restored.bind(item)

    with pytest.raises(ValueError, match="different data item"):
        restored.bind(duplicate)


def test_type_specific_sceneobject_state_roundtrips():
    mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [0, 1, 0]], [[0, 1, 2]])
    graph = Graph()
    graph.add_node(0, x=0, y=0, z=0)
    volmesh = VolMesh.from_vertices_and_cells([[0, 0, 0]], [])
    scene = Scene()
    meshobject = scene.add(
        mesh,
        show_vertices=True,
        vertexsize=3.0,
        hide_coplanaredges=True,
        use_vertexcolors=True,
    )
    graphobject = scene.add(graph, show_nodes=False, edgewidth=2.0)
    volmeshobject = scene.add(volmesh, show_cells=False, vertexsize=4.0)

    restored = Scene.from_jsonstring(scene.to_jsonstring())

    restored_mesh = restored.object(meshobject.guid)
    restored_graph = restored.object(graphobject.guid)
    restored_volmesh = restored.object(volmeshobject.guid)
    assert isinstance(restored_mesh, MeshObject)
    assert restored_mesh.show_vertices is True
    assert restored_mesh.vertexsize == 3.0
    assert restored_mesh.hide_coplanaredges is True
    assert restored_mesh.use_vertexcolors is True
    assert isinstance(restored_graph, GraphObject)
    assert restored_graph.show_nodes is False
    assert restored_graph.edgewidth == 2.0
    assert isinstance(restored_volmesh, VolMeshObject)
    assert restored_volmesh.show_cells is False
    assert restored_volmesh.vertexsize == 4.0


def test_geometry_specific_sceneobject_state_roundtrips():
    from compas.geometry import Box
    from compas.geometry import Frame
    from compas.geometry import Plane
    from compas.geometry import PlanarSurface
    from compas.geometry import Point
    from compas.geometry import Vector

    scene = Scene()
    shapeobject = scene.add(Box(), u=8, v=12)
    surfaceobject = scene.add(PlanarSurface(), u=5, v=7)
    frameobject = scene.add(Frame.worldXY(), size=2.0)
    planeobject = scene.add(Plane.worldXY(), size=3.0)
    vectorobject = scene.add(Vector(1, 2, 3), anchor=Point(4, 5, 6))

    restored = Scene.from_jsonstring(scene.to_jsonstring())

    restored_shape = restored.object(shapeobject.guid)
    restored_surface = restored.object(surfaceobject.guid)
    restored_frame = restored.object(frameobject.guid)
    restored_plane = restored.object(planeobject.guid)
    restored_vector = restored.object(vectorobject.guid)
    assert isinstance(restored_shape, ShapeObject)
    assert (restored_shape.u, restored_shape.v) == (8, 12)
    assert isinstance(restored_surface, SurfaceObject)
    assert (restored_surface.u, restored_surface.v) == (5, 7)
    assert isinstance(restored_frame, FrameObject)
    assert restored_frame.size == 2.0
    assert isinstance(restored_plane, PlaneObject)
    assert restored_plane.size == 3.0
    assert isinstance(restored_vector, VectorObject)
    assert restored_vector.anchor == Point(4, 5, 6)


def test_scene_state_fields_compose_defaults_and_omitted_defaults():
    class BaseObject(SceneObject):
        __scene_state_namespace__ = "test.base"
        __scene_state_fields__ = (SceneStateField("size", int, default=1, required=False, omit_default=True),)

        def __init__(self, size=1, **kwargs):
            super().__init__(**kwargs)
            self.size = size

    class DerivedObject(BaseObject):
        __scene_state_namespace__ = "test.derived"
        __scene_state_fields__ = (SceneStateField("label", str, default="default", required=False),)

        def __init__(self, label="default", **kwargs):
            super().__init__(**kwargs)
            self.label = label

    original = DerivedObject(item_guid=uuid4(), label="kept")
    data = original.__data__
    assert data["extensions"] == {"test.derived": {"label": "kept"}}

    restored = DerivedObject.__from_data__(data)

    assert restored.size == 1
    assert restored.label == "kept"


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"unknown": True}, "Unknown scene fields"),
        ({"version": 999}, "Unsupported scene schema version"),
        ({"objects": ()}, "objects should be a list"),
        ({"name": None}, "name"),
    ],
)
def test_scene_rejects_invalid_closed_schema(change, message):
    data = Scene().__data__
    data.update(change)

    with pytest.raises((TypeError, ValueError), match=message):
        Scene.__from_data__(data)
