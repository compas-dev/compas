import subprocess
import sys
from importlib import import_module
from uuid import uuid4

import pytest

from compas.colors import Color
from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Translation
from compas.geometry import Vector
from compas.scene import ArrowAnnotation
from compas.scene import ComponentAnchor
from compas.scene import DimensionStyle
from compas.scene import DistanceDimension
from compas.scene import DistanceDimensionLayout
from compas.scene import PointAnchor
from compas.scene import Scene
from compas.scene import SceneAnnotation
from compas.scene import TextAnnotation


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


def test_legacy_annotation_sceneobject_module_is_removed():
    with pytest.raises(ModuleNotFoundError):
        import_module("compas.scene.annotationobject")


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
    "item",
    [
        TextAnnotation("A", [0, 0, 0]),
        ArrowAnnotation([0, 0, 0], [1, 0, 0]),
        DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0])),
    ],
)
def test_annotations_use_the_flat_collection_only(item):
    scene = Scene(context=None, _detect_context=False)

    with pytest.raises(TypeError, match="add_annotation"):
        scene.add(item)
    entry = scene.add_annotation(item)

    assert type(entry) is SceneAnnotation
    assert entry.item is item
    assert scene.annotations == (entry,)
    assert entry not in scene.objects
    assert not hasattr(entry, "node")
    assert not hasattr(entry, "transformation")


def test_scene_roundtrip_keeps_annotation_items_reference_only():
    point = Point(1, 2, 3)
    scene = Scene(context=None, _detect_context=False)
    pointobject = scene.add(point)
    dimension = DistanceDimension(
        ComponentAnchor(pointobject.guid, "point"),
        PointAnchor([4, 2, 3]),
    )
    dimensionentry = scene.add_annotation(dimension)

    restored_scene = Scene.from_jsonstring(scene.to_jsonstring())
    restored_dimension = DistanceDimension.from_jsonstring(dimension.to_jsonstring())
    restored_point = Point.from_jsonstring(point.to_jsonstring())

    assert restored_scene.item_store == {}
    restored_scene.bind_many([restored_point, restored_dimension])
    restored_entry = restored_scene.annotation(dimensionentry.guid)
    assert restored_entry.item is restored_dimension
    assert restored_dimension.distance(restored_scene) == pytest.approx(3.0)


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


def test_dimension_format_reassignment_updates_derived_label_without_changing_geometry():
    start = PointAnchor([0, 0, 0])
    end = PointAnchor([3, 4, 0])
    dimension = DistanceDimension(start, end, unit="mm", precision=2)

    dimension.unit = "  cm  "
    dimension.precision = 4

    assert dimension.unit == "  cm  "
    assert dimension.precision == 4
    assert dimension.formatted_label() == "5.0000   cm  "
    assert dimension.start is start
    assert dimension.end is end
    assert dimension.resolve() == (Point(0, 0, 0), Point(3, 4, 0))
    assert dimension.distance() == pytest.approx(5.0)

    dimension.unit = None

    assert dimension.formatted_label() == "5.0000"


@pytest.mark.parametrize("precision", [0, 15])
def test_dimension_precision_boundaries_roundtrip(precision):
    dimension = DistanceDimension(
        PointAnchor([0, 0, 0]),
        PointAnchor([1, 0, 0]),
        precision=precision,
    )

    restored = DistanceDimension.from_jsonstring(dimension.to_jsonstring())

    assert dimension.precision == precision
    assert restored == dimension
    assert restored.precision == precision


@pytest.mark.parametrize(
    ("attribute", "value", "error"),
    [
        ("unit", 1, TypeError),
        ("unit", "", ValueError),
        ("unit", " \t ", ValueError),
        ("precision", True, TypeError),
        ("precision", 1.5, TypeError),
        ("precision", "3", TypeError),
        ("precision", -1, ValueError),
        ("precision", 16, ValueError),
    ],
)
def test_dimension_format_reassignment_rejects_invalid_values_atomically(attribute, value, error):
    dimension = DistanceDimension(
        PointAnchor([0, 0, 0]),
        PointAnchor([3, 4, 0]),
        unit="mm",
        precision=3,
    )
    start = dimension.start
    end = dimension.end

    with pytest.raises(error):
        setattr(dimension, attribute, value)

    assert dimension.unit == "mm"
    assert dimension.precision == 3
    assert dimension.formatted_label() == "5.000 mm"
    assert dimension.start is start
    assert dimension.end is end
    assert dimension.distance() == pytest.approx(5.0)


def test_dimension_precision_above_limit_is_rejected_during_construction_and_deserialization():
    start = PointAnchor([0, 0, 0])
    end = PointAnchor([1, 0, 0])

    with pytest.raises(ValueError, match="at most 15"):
        DistanceDimension(start, end, precision=16, label="clearance")

    data = DistanceDimension(start, end, label="clearance").__data__
    data["precision"] = 16

    with pytest.raises(ValueError, match="at most 15"):
        DistanceDimension.__from_data__(data)


def test_dimension_format_reassignment_preserves_explicit_label_and_serialization_contract():
    dimension = DistanceDimension(
        PointAnchor([0, 0, 0]),
        PointAnchor([3, 4, 0]),
        label="clearance",
    )

    dimension.unit = " cm "
    dimension.precision = 5
    with pytest.raises(ValueError, match="at most 15"):
        dimension.precision = 16
    restored = DistanceDimension.from_jsonstring(dimension.to_jsonstring())

    assert dimension.formatted_label() == "clearance"
    assert set(dimension.__data__) == {"start", "end", "unit", "precision", "label"}
    assert restored == dimension
    assert restored.unit == " cm "
    assert restored.precision == 5
    assert restored.label == "clearance"
    assert restored.formatted_label() == "clearance"


def test_fixed_dimension_points_are_world_coordinates_outside_the_hierarchy():
    scene = Scene(context=None, _detect_context=False)
    dimension = DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0]))
    entry = scene.add_annotation(dimension)

    assert entry not in scene.objects
    assert dimension.resolve(scene) == (Point(0, 0, 0), Point(1, 0, 0))
    assert dimension.distance(scene) == pytest.approx(1.0)


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


def test_mixed_dimension_keeps_fixed_anchor_in_world_coordinates():
    scene = Scene(context=None, _detect_context=False)
    pointobject = scene.add(Point(5, 0, 0))
    dimension = DistanceDimension(
        PointAnchor([1, 0, 0]),
        ComponentAnchor(pointobject.guid, "point"),
    )
    scene.add_annotation(dimension)

    assert dimension.resolve(scene) == (Point(1, 0, 0), Point(5, 0, 0))


def test_dimension_style_roundtrips_and_mutates_independently():
    style = DimensionStyle(
        color=Color.red(),
        line_width=2,
        extension_line_width=1.5,
        text_size=14,
        arrow_size=9,
        label_offset=-4,
    )
    restored = DimensionStyle.from_jsonstring(style.to_jsonstring())

    assert restored == style
    assert style.__data__["version"] == DimensionStyle.STYLE_SCHEMA_VERSION
    assert restored.color == Color.red()
    assert restored.line_width == 2.0
    assert restored.extension_line_width == 1.5
    restored.line_width = 5
    assert restored.line_width == 5.0
    restored.extension_line_width = 0.5
    assert restored.extension_line_width == 0.5


def test_dimension_style_defaults_to_magenta():
    style = DimensionStyle()
    restored = DimensionStyle.from_jsonstring(style.to_jsonstring())

    assert style.color == Color.magenta()
    assert style.line_width == 3.0
    assert style.extension_line_width == 1.0
    assert restored.color == Color.magenta()
    assert restored.extension_line_width == 1.0


def test_distance_dimension_layout_roundtrips_signed_offset_and_exact_normal():
    layout = DistanceDimensionLayout(offset=-2.5, plane_normal=Vector(0, 0, 4))

    restored = DistanceDimensionLayout.from_jsonstring(layout.to_jsonstring())

    assert restored == layout
    assert restored.offset == -2.5
    assert restored.plane_normal == Vector(0, 0, 4)
    normal = restored.plane_normal
    normal.x = 9
    assert restored.plane_normal == Vector(0, 0, 4)
    with pytest.raises(AttributeError):
        setattr(restored, "offset", 1.0)


@pytest.mark.parametrize(
    ("kwargs", "error"),
    [
        ({"offset": True}, TypeError),
        ({"offset": float("inf")}, ValueError),
        ({"offset": float("nan")}, ValueError),
        ({"plane_normal": [0, 0, 1]}, TypeError),
        ({"plane_normal": Vector(float("nan"), 0, 1)}, ValueError),
    ],
)
def test_distance_dimension_layout_rejects_invalid_values(kwargs, error):
    with pytest.raises(error):
        DistanceDimensionLayout(**kwargs)


def test_distance_dimension_layout_uses_closed_serialized_schema():
    layout = DistanceDimensionLayout()

    with pytest.raises(ValueError, match="Unknown distance-dimension-layout fields"):
        DistanceDimensionLayout.__from_data__({**layout.__data__, "camera": "current"})
    with pytest.raises(ValueError, match="Missing distance-dimension-layout fields"):
        DistanceDimensionLayout.__from_data__({"offset": 0.0})


def test_distance_entry_defaults_layout_and_other_annotations_reject_it():
    scene = Scene(context=None, _detect_context=False)
    dimension = DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0]))

    entry = scene.add_annotation(dimension)

    assert entry.layout == DistanceDimensionLayout()
    entry.layout = None
    assert entry.layout == DistanceDimensionLayout()
    with pytest.raises(ValueError, match="only for DistanceDimension"):
        scene.add_annotation(TextAnnotation("A", [0, 0, 0]), layout=DistanceDimensionLayout(offset=1, plane_normal=Vector(0, 0, 1)))
    with pytest.raises(TypeError, match="DistanceDimensionLayout or None"):
        SceneAnnotation(dimension, layout=Vector(0, 0, 1))  # type: ignore[arg-type]


def test_distance_entries_receive_default_style_and_other_annotations_reject_it():
    scene = Scene(context=None, _detect_context=False)
    dimension = DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0]))

    entry = scene.add_annotation(dimension)

    assert entry.style == DimensionStyle()
    entry.style = None
    assert entry.style == DimensionStyle()
    with pytest.raises(ValueError, match="only for DistanceDimension"):
        scene.add_annotation(TextAnnotation("A", [0, 0, 0]), style=DimensionStyle())


@pytest.mark.parametrize(
    "background",
    [None, Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 1.0, 0.0, 0.5), Color(0.0, 0.0, 1.0, 0.0)],
)
@pytest.mark.parametrize("padding", [0, 2.0, 7.5])
def test_label_background_presentation_roundtrips(background, padding):
    item = TextAnnotation("A", [0, 0, 0])
    entry = SceneAnnotation(item, label_background=background, label_background_padding=padding)

    restored = SceneAnnotation.from_jsonstring(entry.to_jsonstring())

    assert restored.label_background == background
    assert restored.label_background_padding == padding
    assert restored.item_guid == item.guid


def test_scene_annotation_current_payload_requires_versioned_layout_field():
    item = TextAnnotation("A", [0, 0, 0])
    entry = SceneAnnotation(item)
    data = entry.__data__

    assert data["version"] == SceneAnnotation.ENTRY_SCHEMA_VERSION
    del data["layout"]
    with pytest.raises(ValueError, match="Missing scene-annotation fields: layout"):
        SceneAnnotation.__from_data__(data)

    unsupported = entry.__data__
    unsupported["version"] = 999
    with pytest.raises(ValueError, match="Unsupported scene-annotation schema version: 999"):
        SceneAnnotation.__from_data__(unsupported)


def test_scene_annotation_legacy_unversioned_payload_allows_missing_layout_for_scene_v4_loading():
    item = TextAnnotation("A", [0, 0, 0])
    data = SceneAnnotation(item).__data__
    del data["version"]
    del data["layout"]

    restored = SceneAnnotation.__from_data__(data)

    assert restored.layout is None
    assert restored.item_guid == item.guid


@pytest.mark.parametrize("value", [True, "2", float("inf"), float("nan"), -1])
def test_label_background_padding_rejects_invalid_values(value):
    with pytest.raises((TypeError, ValueError)):
        SceneAnnotation(TextAnnotation("A", [0, 0, 0]), label_background_padding=value)


def test_label_background_rejects_non_color_values():
    with pytest.raises(TypeError, match="Color or None"):
        SceneAnnotation(TextAnnotation("A", [0, 0, 0]), label_background="blue")  # type: ignore[arg-type]


def test_arrow_entries_accept_only_default_label_background_presentation():
    arrow = ArrowAnnotation([0, 0, 0], [1, 0, 0])
    entry = SceneAnnotation(arrow)

    assert entry.label_background is None
    assert entry.label_background_padding == 2.0
    with pytest.raises(ValueError, match="do not support"):
        entry.label_background = Color.red()
    with pytest.raises(ValueError, match="default"):
        entry.label_background_padding = 0.0
    with pytest.raises(ValueError, match="default label-background"):
        SceneAnnotation(arrow, label_background=Color.red())
    with pytest.raises(ValueError, match="default label-background"):
        SceneAnnotation(arrow, label_background_padding=3.0)


@pytest.mark.parametrize(
    ("background", "padding"),
    [(Color.red(), 2.0), (None, 3.0)],
)
def test_unresolved_arrow_binding_rejects_nondefault_label_background_atomically(background, padding):
    arrow = ArrowAnnotation([0, 0, 0], [1, 0, 0])
    scene = Scene(context=None, _detect_context=False)
    entry = scene.add_annotation_reference(
        arrow.guid,
        name="Arrow",
        label_background=background,
        label_background_padding=padding,
    )

    with pytest.raises(ValueError, match="default label-background"):
        scene.bind(arrow)

    assert scene.item_store == {}
    with pytest.raises(LookupError):
        _ = entry.item


@pytest.mark.parametrize(
    ("background", "padding"),
    [(Color.red(), 2.0), (None, 3.0)],
)
def test_unresolved_arrow_entry_rejects_nondefault_background_before_attachment(background, padding):
    arrow = ArrowAnnotation([0, 0, 0], [1, 0, 0])
    scene = Scene(context=None, _detect_context=False)
    attached = scene.add_annotation(arrow)
    entry = SceneAnnotation(
        item_guid=arrow.guid,
        name="Invalid Arrow",
        label_background=background,
        label_background_padding=padding,
    )

    with pytest.raises(ValueError, match="default label-background"):
        scene.add_annotation_entry(entry)

    assert scene.annotations == (attached,)
    assert scene.item_store == {arrow.guid: arrow}
    assert entry.scene is None
    with pytest.raises(LookupError):
        _ = entry.item


def test_already_bound_distance_reference_attaches_and_normalizes_default_style():
    dimension = DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0]))
    scene = Scene(context=None, _detect_context=False)
    attached = scene.add_annotation(dimension, name="Existing")
    entry = SceneAnnotation(item_guid=dimension.guid, name="Reference")

    assert entry.style is None

    result = scene.add_annotation_entry(entry)

    assert result is entry
    assert scene.annotations == (attached, entry)
    assert entry.scene is scene
    assert entry.item is dimension
    assert entry.style == DimensionStyle()
    assert attached.item is dimension
    assert attached.style == DimensionStyle()
    assert scene.item_store == {dimension.guid: dimension}


def test_scene_add_annotation_exposes_label_background_presentation():
    scene = Scene(context=None, _detect_context=False)
    background = Color(0.1, 0.2, 0.3, 0.4)

    entry = scene.add_annotation(
        TextAnnotation("A", [0, 0, 0]),
        label_background=background,
        label_background_padding=4.0,
    )

    assert entry.label_background == background
    assert entry.label_background_padding == 4.0


def test_annotation_remove_and_explicit_reattach_preserve_identity_and_state():
    item = TextAnnotation("A", [0, 0, 0])
    scene = Scene(context=None, _detect_context=False)
    entry = scene.add_annotation(item, name="Label", show=False)
    guid = entry.guid

    scene.remove_annotation(entry)

    assert entry.scene is None
    assert entry.item is item
    assert entry.guid == guid
    assert entry.name == "Label"
    assert entry.show is False
    assert item.guid not in scene.item_store

    other = Scene(context=None, _detect_context=False)
    other.add_annotation_entry(entry)
    assert other.annotation(guid) is entry
    assert entry.item is item


def test_shared_annotation_item_is_pruned_after_last_entry():
    item = TextAnnotation("Shared", [0, 0, 0])
    scene = Scene(context=None, _detect_context=False)
    first = scene.add_annotation(item)
    second = scene.add_annotation(item)

    scene.remove_annotation(first)
    assert scene.item_store[item.guid] is item

    scene.remove_annotation(second)
    assert item.guid not in scene.item_store


def test_unresolved_distance_reference_normalizes_style_when_bound():
    dimension = DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0]))
    scene = Scene(context=None, _detect_context=False)
    entry = scene.add_annotation_reference(dimension.guid, name="Distance")

    assert entry.style is None
    assert entry.layout is None
    scene.bind(dimension)

    assert entry.item is dimension
    assert entry.style == DimensionStyle()
    assert entry.layout == DistanceDimensionLayout()
    entry.style = None
    assert entry.style == DimensionStyle()
    entry.layout = None
    assert entry.layout == DistanceDimensionLayout()


def test_unresolved_reference_preserves_layout_until_binding_validates_item_type():
    layout = DistanceDimensionLayout(offset=3, plane_normal=Vector(0, 0, 2))
    dimension = DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0]))
    text = TextAnnotation("A", [0, 0, 0])
    distance_scene = Scene(context=None, _detect_context=False)
    distance_entry = distance_scene.add_annotation_reference(dimension.guid, name="Distance", layout=layout)
    text_scene = Scene(context=None, _detect_context=False)
    text_entry = text_scene.add_annotation_reference(text.guid, name="Text", layout=layout)

    assert distance_entry.layout is layout
    distance_scene.bind(dimension)
    assert distance_entry.layout is layout
    with pytest.raises(ValueError, match="only for DistanceDimension"):
        text_scene.bind(text)
    assert text_entry.layout is layout
    assert text_scene.item_store == {}


def test_annotation_and_spatial_bindings_reject_wrong_item_domains():
    text = TextAnnotation("A", [0, 0, 0])
    point = Point(0, 0, 0)
    scene = Scene(context=None, _detect_context=False)
    scene.add_annotation_reference(point.guid, name="Invalid annotation")
    scene.add_reference(text.guid, name="Invalid spatial item")

    with pytest.raises(TypeError, match="scene-annotation item"):
        scene.bind(point)
    with pytest.raises(TypeError, match="Scene.annotations"):
        scene.bind(text)

    assert scene.item_store == {}


def test_bound_text_reference_rejects_later_dimension_style_assignment():
    text = TextAnnotation("A", [0, 0, 0])
    scene = Scene(context=None, _detect_context=False)
    entry = scene.add_annotation_reference(text.guid, name="Text")
    scene.bind(text)

    with pytest.raises(ValueError, match="only for DistanceDimension"):
        entry.style = DimensionStyle()


def test_scene_rejects_guid_collision_between_object_and_annotation():
    scene = Scene(context=None, _detect_context=False)
    sceneobject = scene.add(Point(0, 0, 0))
    entry = SceneAnnotation(TextAnnotation("A", [0, 0, 0]))
    entry._guid = sceneobject.guid

    with pytest.raises(ValueError, match="already stored"):
        scene.add_annotation_entry(entry)


@pytest.mark.parametrize("field", ["line_width", "extension_line_width", "text_size", "arrow_size"])
@pytest.mark.parametrize("value", [True, 0, -1, float("inf"), float("nan")])
def test_dimension_style_rejects_invalid_positive_fields(field, value):
    kwargs = {field: value}
    with pytest.raises((TypeError, ValueError)):
        DimensionStyle(**kwargs)


@pytest.mark.parametrize("value", [True, float("inf"), float("nan")])
def test_dimension_style_rejects_invalid_label_offset(value):
    with pytest.raises((TypeError, ValueError)):
        DimensionStyle(label_offset=value)


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

    with pytest.raises(ValueError, match="Unknown dimension-style fields"):
        DimensionStyle.__from_data__(
            {
                **DimensionStyle().__data__,
                "opacity": 0.5,
            }
        )

    entry = SceneAnnotation(TextAnnotation("A", [0, 0, 0]))
    with pytest.raises(ValueError, match="Unknown scene-annotation fields"):
        SceneAnnotation.__from_data__(
            {
                **entry.__data__,
                "parent": None,
            }
        )


def test_dimension_style_current_payload_requires_extension_line_width():
    data = DimensionStyle().__data__
    del data["extension_line_width"]

    with pytest.raises(ValueError, match="Missing dimension-style fields: extension_line_width"):
        DimensionStyle.__from_data__(data)


def test_dimension_style_legacy_payload_rejects_current_only_fields():
    data = DimensionStyle().__data__
    del data["version"]

    with pytest.raises(ValueError, match="Unknown dimension-style fields: extension_line_width"):
        DimensionStyle.__from_data__(data)
