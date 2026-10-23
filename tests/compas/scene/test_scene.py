import pytest  # noqa: F401
from compas.scene import context
from compas.scene import register
from compas.scene import Scene
from compas.scene import SceneObject
from compas.scene import SceneObjectNotRegisteredError
from compas.data import Data
from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Translation
from compas.geometry import Transformation
from compas.scene import Group
from compas.datastructures import Tree
from compas.datastructures import Graph
from compas.datastructures import VolMesh


@pytest.fixture(autouse=True)
def reset_sceneobjects_registration():
    # before each test
    yield
    # after each test, reset scene objects
    context.ITEM_SCENEOBJECT.clear()


def register_fake_context():
    register(FakeItem, FakeSceneObject, context="fake")


class FakeSceneObject(SceneObject):
    def draw(self):
        pass

    def clear(self):
        pass


class FakeSubSceneObject(SceneObject):
    def draw(self):
        pass

    def clear(self):
        pass


class FakeItem(Data):
    pass


class FakeSubItem(FakeItem):
    pass


def test_get_sceneobject_cls_with_orderly_registration():
    register(FakeItem, FakeSceneObject, context="fake")
    register(FakeSubItem, FakeSubSceneObject, context="fake")
    item = FakeItem()
    sceneobject = SceneObject(item, context="fake")
    assert isinstance(sceneobject, FakeSceneObject)

    item = FakeSubItem()
    sceneobject = SceneObject(item, context="fake")
    assert isinstance(sceneobject, FakeSubSceneObject)


def test_get_sceneobject_cls_with_out_of_order_registration():
    register(FakeSubItem, FakeSubSceneObject, context="fake")
    register(FakeItem, FakeSceneObject, context="fake")
    item = FakeItem()
    sceneobject = SceneObject(item, context="fake")
    assert isinstance(sceneobject, FakeSceneObject)

    item = FakeSubItem()
    sceneobject = SceneObject(item, context="fake")
    assert isinstance(sceneobject, FakeSubSceneObject)


def test_sceneobject_auto_context_discovery():
    register_fake_context()

    item = FakeItem()
    sceneobject = SceneObject(item)

    assert isinstance(sceneobject, FakeSceneObject)


def test_sceneobject_auto_context_discovery_no_context():
    with pytest.raises(SceneObjectNotRegisteredError):
        item = FakeSubItem()
        _ = SceneObject(item)


def test_explicit_sceneobject_type_is_only_a_factory_option():
    sceneobject = SceneObject(FakeItem(), sceneobject_type=FakeSceneObject)

    assert isinstance(sceneobject, FakeSceneObject)
    assert "sceneobject_type" not in sceneobject.attributes


def test_context_detection_does_not_guess_between_registered_contexts():
    register(FakeItem, FakeSceneObject, context="first")
    register(FakeItem, FakeSceneObject, context="second")

    assert context.detect_current_context() is None


def test_sceneobject_transform():
    scene = Scene()
    sceneobj1 = scene.add(Box())
    sceneobj1.transformation = Translation.from_vector([10.0, 0.0, 0.0])
    assert sceneobj1.worldtransformation == sceneobj1.transformation
    assert sceneobj1.worldtransformation == Translation.from_vector([10.0, 0.0, 0.0])
    assert sceneobj1.frame == Frame([10.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    assert sceneobj1.frame.to_transformation() == Translation.from_vector([10.0, 0.0, 0.0])

    sceneobj2 = scene.add(Box(), parent=sceneobj1)
    sceneobj2.transformation = Translation.from_vector([10.0, 10.0, 0.0])
    assert sceneobj2.worldtransformation == sceneobj1.transformation * sceneobj2.transformation
    assert sceneobj2.worldtransformation == Translation.from_vector([20.0, 10.0, 0.0])
    assert sceneobj2.frame == Frame([20.0, 10.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    assert sceneobj2.frame.to_transformation() == Translation.from_vector([20.0, 10.0, 0.0])

    sceneobj3 = scene.add(Box(), parent=sceneobj2)
    sceneobj3.transformation = Translation.from_vector([10.0, 10.0, 10.0])
    assert sceneobj3.worldtransformation == sceneobj1.transformation * sceneobj2.transformation * sceneobj3.transformation
    assert sceneobj3.worldtransformation == Translation.from_vector([30.0, 20.0, 10.0])
    assert sceneobj3.frame == Frame([30.0, 20.0, 10.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    assert sceneobj3.frame.to_transformation() == Translation.from_vector([30.0, 20.0, 10.0])


def test_sceneobject_settings_store_only_local_transformation():
    scene = Scene()
    parent = scene.add(Box())
    child = scene.add(Box(), parent=parent)
    parent.transformation = Translation.from_vector([10.0, 0.0, 0.0])
    child.transformation = Translation.from_vector([0.0, 5.0, 0.0])

    assert "frame" not in parent.settings
    assert "frame" not in child.settings
    assert parent.settings["transformation"] == parent.transformation
    assert child.settings["transformation"] == child.transformation


def test_sceneobject_frame_and_worldtransformation_setters():
    """Test that frame and worldtransformation setters work correctly."""
    scene = Scene()

    # Test on root object
    root_obj = scene.add(Box())
    test_frame = Frame([10.0, 20.0, 30.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    root_obj.frame = test_frame
    assert root_obj.frame == test_frame
    assert root_obj.worldtransformation == Transformation.from_frame(test_frame)

    # Test worldtransformation setter on root object
    test_transform = Translation.from_vector([5.0, 10.0, 15.0])
    root_obj.worldtransformation = test_transform
    assert root_obj.worldtransformation == test_transform
    assert root_obj.transformation == test_transform

    # Test with parent-child relationship
    parent_obj = scene.add(Box())
    child_obj = scene.add(Box(), parent=parent_obj)
    parent_obj.transformation = Translation.from_vector([10.0, 0.0, 0.0])

    # Test frame setter with parent
    child_frame = Frame([30.0, 20.0, 10.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    child_obj.frame = child_frame
    assert child_obj.frame == child_frame
    expected_local = parent_obj.worldtransformation.inverse() * Transformation.from_frame(child_frame)
    assert child_obj.transformation == expected_local

    # Test worldtransformation setter with parent
    child_world_transform = Translation.from_vector([50.0, 30.0, 20.0])
    child_obj.worldtransformation = child_world_transform
    assert child_obj.worldtransformation == child_world_transform
    expected_local = parent_obj.worldtransformation.inverse() * child_world_transform
    assert child_obj.transformation == expected_local


def test_graphobject_coordinate_cache_tracks_ancestor_transformations():
    scene = Scene()
    parent = scene.add_group("Parent")
    graph = Graph.from_nodes_and_edges([(0, 0, 0)], [])
    graphobject = scene.add(graph, parent=parent)

    assert graphobject.node_xyz[0] == [0.0, 0.0, 0.0]

    parent.transformation = Translation.from_vector([1.0, 2.0, 3.0])

    assert graphobject.node_xyz[0] == [1.0, 2.0, 3.0]


def test_graphobject_explicit_coordinates_are_not_ancestor_transform_cache():
    scene = Scene()
    parent = scene.add_group("Parent")
    graph = Graph.from_nodes_and_edges([(0, 0, 0)], [])
    graphobject = scene.add(graph, parent=parent)
    graphobject.node_xyz = {0: [4.0, 5.0, 6.0]}

    parent.transformation = Translation.from_vector([1.0, 2.0, 3.0])

    assert graphobject.node_xyz[0] == [4.0, 5.0, 6.0]


def test_graphobject_invalidate_refreshes_coordinates_after_graph_mutation():
    scene = Scene()
    graph = Graph.from_nodes_and_edges([(0, 0, 0)], [])
    graphobject = scene.add(graph)

    assert graphobject.node_xyz[0] == [0.0, 0.0, 0.0]

    graph.node_attributes(0, ["x", "y", "z"], [1.0, 2.0, 3.0])
    assert graphobject.node_xyz[0] == [0.0, 0.0, 0.0]

    graphobject.invalidate()

    assert graphobject.node_xyz[0] == [1.0, 2.0, 3.0]


def test_volmeshobject_coordinate_cache_tracks_ancestor_transformations():
    scene = Scene()
    parent = scene.add_group("Parent")
    volmesh = VolMesh.from_meshgrid(1, 1, 1, 1, 1, 1)
    volmeshobject = scene.add(volmesh, parent=parent)
    vertex = next(volmesh.vertices())
    xyz = volmeshobject.vertex_xyz[vertex]

    parent.transformation = Translation.from_vector([1.0, 2.0, 3.0])

    assert volmeshobject.vertex_xyz[vertex] == [xyz[0] + 1.0, xyz[1] + 2.0, xyz[2] + 3.0]


def test_volmeshobject_invalidate_refreshes_coordinates_after_volmesh_mutation():
    scene = Scene()
    volmesh = VolMesh.from_meshgrid(1, 1, 1, 1, 1, 1)
    volmeshobject = scene.add(volmesh)
    vertex = next(volmesh.vertices())
    _ = volmeshobject.vertex_xyz

    volmesh.vertex_attributes(vertex, ["x", "y", "z"], [1.0, 2.0, 3.0])
    volmeshobject.invalidate()

    assert volmeshobject.vertex_xyz[vertex] == [1.0, 2.0, 3.0]


def test_scene_clear():
    scene = Scene()
    sceneobj1 = scene.add(Box())
    sceneobj2 = scene.add(Box(), parent=sceneobj1)
    sceneobj3 = scene.add(Box(), parent=sceneobj2)  # noqa: F841

    assert len(scene.objects) == 3

    scene.clear(clear_context=False, clear_scene=True)

    assert len(scene.objects) == 0


def test_scene_owns_tree_with_group_root():
    scene = Scene()

    assert not isinstance(scene, Tree)
    assert isinstance(scene.tree, Tree)
    assert isinstance(scene.root, Group)
    assert scene.root.tree is scene.tree


def test_group_creation():
    scene = Scene()
    group = scene.add_group("TestGroup")
    assert isinstance(group, Group)
    assert group.name == "TestGroup"
    assert group.parent == scene.root


def test_group_add_item():
    scene = Scene()
    group = scene.add_group("TestGroup")
    box = Box()
    box_obj = group.add(box)
    assert isinstance(box_obj, SceneObject)
    assert box_obj.parent is group
    assert box_obj.item is box


def test_group_add_from_list():
    scene = Scene()
    group = scene.add_group("TestGroup")
    boxes = [Box() for _ in range(3)]
    box_objs = group.add_from_list(boxes)
    assert len(box_objs) == 3
    for box_obj in box_objs:
        assert isinstance(box_obj, SceneObject)
        assert box_obj.parent is group


def test_group_kwargs_inheritance():
    scene = Scene()
    group = scene.add_group("TestGroup", show=False)
    box = Box()
    box_obj = group.add(box)
    assert not box_obj.show  # Should inherit show=False from group


def test_group_hierarchy():
    scene = Scene()
    parent_group = scene.add_group("ParentGroup")
    child_group = parent_group.add(Group("ChildGroup"))
    box = Box()
    box_obj = child_group.add(box)

    assert box_obj.parent is child_group
    assert child_group.parent is parent_group
    assert parent_group.parent is scene.root
