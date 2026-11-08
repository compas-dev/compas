import subprocess
import sys
from uuid import uuid4

import pytest

from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.scene import ArrowAnnotation
from compas.scene import ArrowAnnotationObject
from compas.scene import ComponentAnchor
from compas.scene import DistanceDimension
from compas.scene import DistanceDimensionObject
from compas.scene import PointAnchor
from compas.scene import Scene
from compas.scene import TextAnnotation
from compas.scene import TextAnnotationObject


def test_annotation_roundtrip_is_headless():
    code = """
import sys
from compas.scene import TextAnnotation

item = TextAnnotation('headless', [0, 0, 0])
TextAnnotation.from_jsonstring(item.to_jsonstring())
assert 'compas_viewer' not in sys.modules
"""

    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    "item",
    [
        TextAnnotation("origin", [0, 0, 0], height=18, horizontal_alignment="center"),
        ArrowAnnotation([0, 0, 0], [1, 2, 3]),
        DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([3, 4, 0]), unit="mm", precision=3),
        ComponentAnchor(uuid4(), "edge", component=("a", "b"), parameter=0.25),
        PointAnchor([1, 2, 3]),
    ],
)
def test_annotation_data_roundtrips(item):
    restored = type(item).from_jsonstring(item.to_jsonstring())

    assert restored == item
    assert restored.guid == item.guid
    assert restored.__data__ == item.__data__


@pytest.mark.parametrize(
    ("item", "object_type"),
    [
        (TextAnnotation("A", [0, 0, 0]), TextAnnotationObject),
        (ArrowAnnotation([0, 0, 0], [1, 0, 0]), ArrowAnnotationObject),
        (DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0])), DistanceDimensionObject),
    ],
)
def test_scene_add_returns_stable_annotation_object_types(item, object_type):
    scene = Scene(context=None, _detect_context=False)

    sceneobject = scene.add(item)

    assert type(sceneobject) is object_type
    assert sceneobject.item is item


def test_scene_roundtrip_keeps_annotation_items_reference_only():
    point = Point(1, 2, 3)
    scene = Scene(context=None, _detect_context=False)
    pointobject = scene.add(point)
    dimension = DistanceDimension(
        ComponentAnchor(pointobject.guid, "point"),
        PointAnchor([4, 2, 3]),
    )
    dimensionobject = scene.add(dimension)

    restored_scene = Scene.from_jsonstring(scene.to_jsonstring())
    restored_dimension = DistanceDimension.from_jsonstring(dimension.to_jsonstring())
    restored_point = Point.from_jsonstring(point.to_jsonstring())

    assert restored_scene.item_store == {}
    restored_scene.bind_many([restored_point, restored_dimension])
    restored_object = restored_scene.object(dimensionobject.guid)
    assert isinstance(restored_object, DistanceDimensionObject)
    assert restored_object.dimension is restored_dimension
    assert restored_dimension.distance(restored_scene, restored_object.worldtransformation) == pytest.approx(3.0)


def test_fixed_dimension_derives_distance_and_deterministic_label():
    dimension = DistanceDimension(
        PointAnchor([0, 0, 0]),
        PointAnchor([3, 4, 0]),
        unit="mm",
        precision=3,
    )

    assert dimension.resolve() == (Point(0, 0, 0), Point(3, 4, 0))
    assert dimension.distance() == pytest.approx(5.0)
    assert dimension.formatted_label() == "5.000 mm"
    assert DistanceDimension(dimension.start, dimension.end, precision=0).formatted_label() == "5"
    assert DistanceDimension(dimension.start, dimension.end, label="clearance").formatted_label() == "clearance"


def test_fixed_dimension_uses_owning_object_hierarchy_transformation():
    scene = Scene(context=None, _detect_context=False)
    parent = scene.add_group("Parent", transformation=Translation.from_vector([10, 0, 0]))
    dimension = DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0]))
    dimensionobject = scene.add(
        dimension,
        parent=parent,
        transformation=Scale.from_factors([2, 2, 2]),
    )

    points = dimension.resolve(scene, dimensionobject.worldtransformation)

    assert points == (Point(10, 0, 0), Point(12, 0, 0))
    assert dimension.distance(scene, dimensionobject.worldtransformation) == pytest.approx(2.0)


def test_component_anchors_follow_datastructure_and_scene_transformations():
    mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [2, 0, 0], [0, 1, 0]], [[0, 1, 2]])
    scene = Scene(context=None, _detect_context=False)
    meshobject = scene.add(mesh, transformation=Translation.from_vector([5, 0, 0]))
    start = ComponentAnchor(meshobject.guid, "vertex", component=0)
    end = ComponentAnchor(meshobject.guid, "edge", component=(1, 0), parameter=0.25)
    dimension = DistanceDimension(start, end)

    assert dimension.resolve(scene) == (Point(5, 0, 0), Point(6.5, 0, 0))
    assert dimension.distance(scene) == pytest.approx(1.5)

    mesh.set_vertex_point(1, [4, 0, 0])

    assert dimension.resolve(scene) == (Point(5, 0, 0), Point(8, 0, 0))
    assert dimension.distance(scene) == pytest.approx(3.0)


def test_component_anchor_supports_point_line_and_graph_node_components():
    scene = Scene(context=None, _detect_context=False)
    pointobject = scene.add(Point(1, 2, 3))
    lineobject = scene.add(Line([0, 0, 0], [4, 0, 0]))
    graph = Graph()
    graph.add_node("a", x=0, y=2, z=0)
    graphobject = scene.add(graph)

    assert ComponentAnchor(pointobject.guid, "point").resolve(scene) == Point(1, 2, 3)
    assert ComponentAnchor(lineobject.guid, "line", parameter=0.25).resolve(scene) == Point(1, 0, 0)
    assert ComponentAnchor(graphobject.guid, "node", component="a").resolve(scene) == Point(0, 2, 0)


def test_component_anchor_supports_serializable_tuple_graph_keys():
    graph = Graph()
    graph.add_node(("a", 0), x=0, y=0, z=0)
    graph.add_node(("b", (1, 2)), x=2, y=0, z=0)
    graph.add_edge(("a", 0), ("b", (1, 2)))
    scene = Scene(context=None, _detect_context=False)
    graphobject = scene.add(graph)
    node = ComponentAnchor(graphobject.guid, "node", component=("a", 0))
    edge = ComponentAnchor(
        graphobject.guid,
        "edge",
        component=(("a", 0), ("b", (1, 2))),
        parameter=0.25,
    )

    restored_node = ComponentAnchor.from_jsonstring(node.to_jsonstring())
    restored_edge = ComponentAnchor.from_jsonstring(edge.to_jsonstring())

    assert restored_node.resolve(scene) == Point(0, 0, 0)
    assert restored_edge.resolve(scene) == Point(0.5, 0, 0)


def test_mixed_dimension_transforms_only_its_fixed_anchor():
    scene = Scene(context=None, _detect_context=False)
    pointobject = scene.add(Point(5, 0, 0))
    dimension = DistanceDimension(
        PointAnchor([1, 0, 0]),
        ComponentAnchor(pointobject.guid, "point"),
    )
    dimensionobject = scene.add(dimension, transformation=Translation.from_vector([10, 0, 0]))

    assert dimension.resolve(scene, dimensionobject.worldtransformation) == (Point(11, 0, 0), Point(5, 0, 0))


def test_removed_or_unbound_components_are_explicitly_unresolved():
    graph = Graph()
    graph.add_node("a", x=0, y=0, z=0)
    graph.add_node("b", x=1, y=0, z=0)
    graph.add_edge("a", "b")
    scene = Scene(context=None, _detect_context=False)
    graphobject = scene.add(graph)
    anchor = ComponentAnchor(graphobject.guid, "edge", component=("a", "b"), parameter=0.5)
    dimension = DistanceDimension(PointAnchor([0, 0, 0]), anchor)

    assert anchor.resolve(scene) == Point(0.5, 0, 0)
    graph.delete_edge(("a", "b"))
    assert anchor.resolve(scene) is None
    assert dimension.resolve(scene) is None
    assert dimension.distance(scene) is None
    assert dimension.formatted_label(scene) is None

    restored_anchor = ComponentAnchor.from_jsonstring(anchor.to_jsonstring())
    assert restored_anchor == anchor
    assert restored_anchor.resolve(scene) is None

    unbound_scene = Scene.from_jsonstring(scene.to_jsonstring())
    assert anchor.resolve(unbound_scene) is None
    assert ComponentAnchor(uuid4(), "point").resolve(scene) is None


@pytest.mark.parametrize(
    ("args", "error"),
    [
        ((uuid4(), "point", 0, None), ValueError),
        ((uuid4(), "vertex", None, None), TypeError),
        ((uuid4(), "node", frozenset({0, 1}), None), TypeError),
        ((uuid4(), "line", None, None), TypeError),
        ((uuid4(), "line", None, -0.1), ValueError),
        ((uuid4(), "edge", (0, 1), 1.1), ValueError),
        ((uuid4(), "edge", (0,), 0.5), TypeError),
    ],
)
def test_component_anchor_rejects_invalid_selector_schemas(args, error):
    with pytest.raises(error):
        ComponentAnchor(args[0], args[1], component=args[2], parameter=args[3])


def test_annotation_validation_is_narrow_and_explicit():
    with pytest.raises(ValueError, match="positive"):
        TextAnnotation("A", [0, 0, 0], height=0)
    with pytest.raises(TypeError, match="number"):
        TextAnnotation("A", [0, 0, 0], height=True)
    with pytest.raises(ValueError, match="finite"):
        TextAnnotation("A", [0, 0, 0], height=float("nan"))
    with pytest.raises(ValueError, match="finite"):
        TextAnnotation("A", [0, 0, 0], height=float("inf"))
    with pytest.raises(ValueError, match="height mode"):
        TextAnnotation("A", [0, 0, 0], height_mode="absolute")
    with pytest.raises(ValueError, match="different"):
        ArrowAnnotation([0, 0, 0], [0, 0, 0])
    with pytest.raises(ValueError, match="non-empty"):
        DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0]), unit="")
    with pytest.raises(ValueError, match="non-negative"):
        DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0]), precision=-1)
    with pytest.raises(TypeError, match="integer"):
        DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0]), precision=True)


def test_serialized_annotation_schemas_reject_unknown_fields():
    with pytest.raises(ValueError, match="Unknown text-annotation fields"):
        TextAnnotation.__from_data__(
            {
                "text": "A",
                "anchor": Point(0, 0, 0),
                "height": 12.0,
                "height_mode": "screen",
                "horizontal_alignment": "left",
                "vertical_alignment": "bottom",
                "font": "renderer-specific.ttf",
            }
        )
