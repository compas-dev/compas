import compas
from uuid import uuid4

import pytest  # noqa: F401
from compas.data import Data
from compas.scene import Scene
from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Ellipse
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import Translation
from compas.geometry import Vector
from compas.geometry import Plane
from compas.datastructures import Mesh
from compas.datastructures import Graph
from compas.datastructures import VolMesh
from compas.scene import Group
from compas.scene import SceneItemNotBoundError
from compas.scene import SceneObject
from compas.scene import SceneStateField
from compas.scene import SceneStateError
from compas.scene import SceneNode


@pytest.fixture
def items():
    box = Box.from_width_height_depth(1, 1, 1)
    capsule = Capsule(0.5, 1, Frame.worldXY())
    circle = Circle(1, Frame.worldXY())
    cone = Cone(1, 1, Frame.worldXY())
    cylinder = Cylinder(1, 1, Frame.worldXY())
    line = Line(Point(0, 0, 0), Point(1, 1, 1))
    point = Point(0, 0, 0)
    polygon = Polygon.from_sides_and_radius_xy(5, 1)
    polyhedron = Polyhedron.from_platonicsolid(4)
    polyline = Polyline([[0, 0, 0], [1, 0, 0], [1, 0, 1]])
    sphere = Sphere(1)
    torus = Torus(1, 0.3, Frame.worldXY())
    vector = Vector(0, 0, 1)
    ellipse = Ellipse(1, 0.5, Frame.worldXY())
    frame = Frame.worldXY()
    plane = Plane(Point(0, 0, 0), Vector(0, 0, 1))
    mesh = Mesh.from_polyhedron(8)
    graph = Graph.from_nodes_and_edges([(0, 0, 0), (0, -1.5, 0), (-1, 1, 0), (1, 1, 0)], [(0, 1), (0, 2), (0, 3)])
    volmesh = VolMesh.from_meshgrid(1, 1, 1, 2, 2, 2)
    group = Group(name="My Group")

    return [
        box,
        capsule,
        circle,
        cone,
        cylinder,
        line,
        point,
        polygon,
        polyhedron,
        polyline,
        sphere,
        torus,
        vector,
        ellipse,
        frame,
        plane,
        mesh,
        graph,
        volmesh,
        group,
    ]


def assert_is_data_equal(obj1, obj2, path=""):
    if type(obj1) is not type(obj2):
        print("Type mismatch: {} != {} for {}:{} and {}:{}".format(type(obj1), type(obj2), path, obj1, path, obj2))
        return False

    if isinstance(obj1, (list, tuple)):
        if len(obj1) != len(obj2):
            print("Length mismatch: {} != {} for {} and {}".format(len(obj1), len(obj2), path, path))
            return False

        for i, (item1, item2) in enumerate(zip(obj1, obj2)):
            if not assert_is_data_equal(item1, item2, path="{}[{}]".format(path, i)):
                return False

        return True

    elif isinstance(obj1, dict):
        if set(obj1.keys()) != set(obj2.keys()):
            print("Key mismatch: {} != {} for {} and {}".format(set(obj1.keys()), set(obj2.keys()), path, path))
            return False

        for key in obj1:
            if not assert_is_data_equal(obj1[key], obj2[key], path='{}["{}"]'.format(path, key)):
                return False

        return True

    elif isinstance(obj1, Data):
        return assert_is_data_equal(obj1.__data__, obj2.__data__, path="{}.__data__".format(path))

    else:
        if obj1 != obj2:
            print("Value mismatch: {} != {} for {}:{} and {}:{}".format(obj1, obj2, path, obj1, path, obj2))
            return False
        else:
            return True


def test_scene_serialisation(items):
    scene1 = Scene()
    for item in items:
        scene1.add(item)

    scene2 = Scene.from_jsonstring(scene1.to_jsonstring())
    assert assert_is_data_equal(scene1, scene2)


def test_scene_serialisation_preserves_shared_items():
    box = Box()
    scene = Scene()
    scene.add(box, name="First")
    scene.add(box, name="Second")

    reconstructed = Scene.from_jsonstring(scene.to_jsonstring())
    reconstructed.bind(box)

    assert reconstructed.objects[0].item is reconstructed.objects[1].item


def test_scene_serialisation_reconstructs_world_transform_from_local_transforms():
    scene = Scene()
    parent_box = Box()
    child_box = Box()
    parent = scene.add(parent_box, name="Parent")
    child = scene.add(child_box, name="Child", parent=parent)
    parent.transformation = Translation.from_vector([10.0, 0.0, 0.0])
    child.transformation = Translation.from_vector([0.0, 5.0, 0.0])

    reconstructed = Scene.from_jsonstring(scene.to_jsonstring())
    reconstructed.bind_many([parent_box, child_box])
    reconstructed_parent = reconstructed.find_by_name("Parent")
    reconstructed_child = reconstructed.find_by_name("Child")

    assert reconstructed_parent is not None
    assert reconstructed_child is not None
    assert reconstructed_parent.transformation == parent.transformation
    assert reconstructed_child.transformation == child.transformation
    assert reconstructed_child.worldtransformation == child.worldtransformation


def test_scene_serialisation_empty():
    scene = Scene()
    scene = compas.json_loads(compas.json_dumps(scene))

    assert isinstance(scene, Scene)


def test_group_serialisation():
    scene1 = Scene()
    group = scene1.add_group("TestGroup", show=False)
    box = Box.from_width_height_depth(1, 1, 1)
    group.add(box)

    scene2 = Scene.from_jsonstring(scene1.to_jsonstring())
    scene2.bind(box)

    # Check if group was serialized correctly
    group2 = scene2.find_by_name("TestGroup")
    assert isinstance(group2, Group)
    assert group2.name == "TestGroup"
    assert not group2.show

    # Check if box was serialized correctly
    box2 = group2.children[0]
    assert isinstance(box2.item, Box)
    assert box2.parent is group2


def test_nested_group_serialisation():
    scene1 = Scene()
    parent_group = scene1.add_group("ParentGroup", show=False)
    child_group = parent_group.add(Group("ChildGroup", show=True))
    box = Box.from_width_height_depth(1, 1, 1)
    child_group.add(box)

    scene2 = Scene.from_jsonstring(scene1.to_jsonstring())
    scene2.bind(box)

    # Check parent group
    parent2 = scene2.find_by_name("ParentGroup")
    assert isinstance(parent2, Group)
    assert not parent2.show

    # Check child group
    child2 = parent2.children[0]
    assert isinstance(child2, Group)
    assert child2.name == "ChildGroup"
    assert child2.show
    assert child2.parent is parent2

    # Check box
    box2 = child2.children[0]
    assert isinstance(box2.item, Box)
    assert box2.parent is child2


def test_group_kwargs_serialisation():
    scene1 = Scene()
    group = scene1.add_group("TestGroup", show=False, opacity=0.5)
    box = Box.from_width_height_depth(1, 1, 1)
    group.add(box)

    scene2 = Scene.from_jsonstring(scene1.to_jsonstring())
    scene2.bind(box)

    # Check if group kwargs were serialized correctly
    group2 = scene2.find_by_name("TestGroup")
    assert not group2.show
    assert group2.opacity == 0.5

    # Check if box inherited kwargs correctly
    box2 = group2.children[0]
    assert not box2.show
    assert box2.opacity == 0.5


def test_scene_serialisation_is_reference_only_and_loads_unresolved():
    box = Box(2)
    scene = Scene("Reference only")
    sceneobject = scene.add(box, name="Box reference")

    reconstructed = Scene.from_jsonstring(scene.to_jsonstring())
    node = reconstructed.find_node_by_name("Box reference")

    assert node is not None
    assert node.guid == sceneobject.guid
    assert node.item_guid == box.guid
    assert not reconstructed.item_store
    with pytest.raises(SceneItemNotBoundError, match=f"{node.guid}.*{box.guid}"):
        reconstructed.object(node)

    reconstructed.bind(box)
    assert reconstructed.object(node).item is box


def test_scene_preserves_unknown_namespaced_extensions_without_an_adapter():
    scene = Scene()
    scene.add_reference(
        uuid4(),
        name="External adapter",
        extensions={"org.example.ViewerObject": {"overlay": True}},
    )

    reconstructed = Scene.from_jsonstring(scene.to_jsonstring())
    node = reconstructed.find_node_by_name("External adapter")

    assert node is not None
    assert node.extensions == {"org.example.ViewerObject": {"overlay": True}}


def test_adapter_extension_fields_are_composed_through_the_mro():
    class BaseAdapter(SceneObject):
        __scene_state_namespace__ = "org.example.BaseAdapter"
        __scene_state_fields__ = (SceneStateField("base_value", int),)

        def __init__(self, *args, base_value=1, **kwargs):
            super().__init__(*args, **kwargs)
            self.base_value = base_value

    class DerivedAdapter(BaseAdapter):
        __scene_state_namespace__ = "org.example.DerivedAdapter"
        __scene_state_fields__ = (SceneStateField("derived_value", str),)

        def __init__(self, *args, derived_value="default", **kwargs):
            super().__init__(*args, **kwargs)
            self.derived_value = derived_value

    box = Box()
    scene = Scene()
    adapter = scene.add(
        SceneObject(
            box,
            sceneobject_type=DerivedAdapter,
            base_value=7,
            derived_value="saved",
        )
    )
    reconstructed = Scene.from_jsonstring(scene.to_jsonstring())
    reconstructed.bind(box)
    node = next(node for node in reconstructed.nodes if node.item_guid)
    restored = reconstructed.object(node, object_type=DerivedAdapter)

    assert adapter.node is not None
    assert adapter.node.extensions == {
        "org.example.BaseAdapter": {"base_value": 7},
        "org.example.DerivedAdapter": {"derived_value": "saved"},
    }
    assert isinstance(restored, DerivedAdapter)
    assert restored.base_value == 7
    assert restored.derived_value == "saved"


def test_bound_extension_state_uses_the_node_as_sole_authority():
    box = Box()
    scene = Scene()
    adapter = scene.add(box, pointsize=2.0)
    assert adapter.node is not None

    adapter.pointsize = 3.0
    assert adapter.node.extensions["compas.scene.GeometryObject"]["pointsize"] == 3.0

    adapter.node.extensions["compas.scene.GeometryObject"]["pointsize"] = 4.0
    assert adapter.pointsize == 4.0


def test_bound_extension_writes_preserve_property_setter_side_effects():
    class Adapter(SceneObject):
        __scene_state_namespace__ = "org.example.SetterAdapter"
        __scene_state_fields__ = (SceneStateField("resolution", int, attribute_name="resolution"),)

        def __init__(self, *args, resolution=4, **kwargs):
            super().__init__(*args, **kwargs)
            self.setter_calls = 0
            self.resolution = resolution

        @property
        def resolution(self):
            return self._resolution

        @resolution.setter
        def resolution(self, value):
            self.setter_calls += 1
            self._resolution = value

    adapter = Scene().add(SceneObject(Box(), sceneobject_type=Adapter))
    adapter.resolution = 8

    assert adapter.setter_calls == 2
    assert adapter.resolution == 8
    assert adapter.node is not None
    assert adapter.node.extensions["org.example.SetterAdapter"]["resolution"] == 8


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("name", 1, "name"),
        ("transformation", "invalid", "transformation"),
        ("color", "red", "color"),
        ("opacity", True, "opacity"),
        ("opacity", 2.0, "opacity"),
        ("show", 1, "show"),
        ("extensions", [], "extensions"),
        ("extensions", {"valid": {1: "invalid"}}, "extension fields"),
    ],
)
def test_scene_node_rejects_invalid_closed_schema_types(field, value, message):
    data = SceneNode(kind="group", name="Root").__data__
    data[field] = value

    with pytest.raises((TypeError, ValueError), match=message):
        SceneNode.__from_data__(data)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"unknown": True}, "Unknown scene-node fields"),
        ({"name": None}, "Missing scene-node fields"),
        ({"kind": "invalid"}, "kind"),
        ({"kind": "item"}, "item GUID"),
        ({"item": str(uuid4())}, "group scene node"),
        ({"children": ()}, "children"),
    ],
)
def test_scene_node_rejects_invalid_closed_schema_structure(change, message):
    data = SceneNode(kind="group", name="Root").__data__
    if change == {"name": None}:
        del data["name"]
    else:
        data.update(change)

    with pytest.raises((TypeError, ValueError), match=message):
        SceneNode.__from_data__(data)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"unknown": True}, "Unknown scene fields"),
        ({"name": None}, "Missing scene fields"),
        ({"version": 2}, "Unsupported scene schema version"),
    ],
)
def test_scene_rejects_invalid_closed_schema_structure(change, message):
    data = Scene().__data__
    if change == {"name": None}:
        del data["name"]
    else:
        data.update(change)

    with pytest.raises(ValueError, match=message):
        Scene.__from_data__(data)


def test_scene_rejects_an_item_node_as_its_root():
    data = Scene().__data__
    data["root"] = SceneNode(kind="item", item_guid=uuid4(), name="Item").__data__

    with pytest.raises(ValueError, match="root should be a group"):
        Scene.__from_data__(data)


def test_scene_state_field_supports_attribute_names_defaults_and_omission():
    class Adapter(SceneObject):
        __scene_state_namespace__ = "org.example.Adapter"
        __scene_state_fields__ = (
            SceneStateField(
                "saved-size",
                int,
                attribute_name="size",
                default=5,
                required=False,
                omit_default=True,
            ),
        )

        def __init__(self, *args, size=5, **kwargs):
            super().__init__(*args, **kwargs)
            self.size = size

    box = Box()
    scene = Scene()
    adapter = scene.add(SceneObject(box, sceneobject_type=Adapter))

    assert adapter.node is not None
    assert "org.example.Adapter" not in adapter.node.extensions

    reconstructed = Scene.from_jsonstring(scene.to_jsonstring())
    reconstructed.bind(box)
    node = next(node for node in reconstructed.nodes if node.item_guid)
    restored = reconstructed.object(node, object_type=Adapter)
    assert restored.size == 5
    assert "org.example.Adapter" not in node.extensions


def test_scene_state_field_rejects_missing_required_state_and_attributes():
    class MissingAttributeAdapter(SceneObject):
        __scene_state_namespace__ = "org.example.MissingAttribute"
        __scene_state_fields__ = (SceneStateField("missing", int),)

    box = Box()
    with pytest.raises(SceneStateError, match="Missing adapter attribute"):
        Scene().add(SceneObject(box, sceneobject_type=MissingAttributeAdapter))

    class RequiredAdapter(SceneObject):
        __scene_state_namespace__ = "org.example.Required"
        __scene_state_fields__ = (SceneStateField("required", int),)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.required = 1

    scene = Scene()
    node = scene.add_reference(box.guid, name="Required", extensions={})
    scene.bind(box)
    with pytest.raises(SceneStateError, match="org.example.Required.required"):
        scene.object(node, object_type=RequiredAdapter)


def test_scene_state_field_rejects_conflicting_declarations():
    class Base(SceneObject):
        __scene_state_namespace__ = "org.example.Base"
        __scene_state_fields__ = (SceneStateField("first", int, attribute_name="value"),)

    class Conflict(Base):
        __scene_state_namespace__ = "org.example.Conflict"
        __scene_state_fields__ = (SceneStateField("second", int, attribute_name="value"),)

    with pytest.raises(SceneStateError, match="Duplicate scene-state adapter attribute"):
        Conflict.scene_state_fields()


def test_scene_objects_are_not_independently_serializable():
    adapter = Scene().add(Box())

    with pytest.raises(NotImplementedError):
        compas.json_dumps(adapter)


def test_bind_many_rejects_a_different_falsey_item_with_the_same_guid():
    class FalseyData(Data):
        @property
        def __data__(self):
            return {}

        @classmethod
        def __from_data__(cls, data):
            return cls()

        def __bool__(self):
            return False

    first = FalseyData()
    second = FalseyData()
    second._guid = first.guid
    scene = Scene()
    scene.add_reference(first.guid, name="Falsey")
    scene.bind(first)

    with pytest.raises(ValueError, match="different data item"):
        scene.bind_many([second])
