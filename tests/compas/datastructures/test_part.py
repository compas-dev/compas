import pytest

from numpy import allclose

from compas.datastructures import Part
from compas.datastructures.assembly.part import MeshGeometry, MeshFeature
from compas.geometry import Polyhedron


def are_mesh_geometries_equal(mesh_geo_a, mesh_geo_b):
    return are_polyhedrons_equal(mesh_geo_a.geometry, mesh_geo_b.geometry)


def are_polyhedrons_equal(poly_a, poly_b):
    return are_geometries_equal(poly_a.faces, poly_a.vertices, poly_b.faces, poly_b.vertices)


def are_geometries_equal(faces_a, vertices_a, faces_b, vertices_b):
    return faces_a == faces_b and allclose(vertices_a, vertices_b)


@pytest.fixture
def feature_polyhedron():
    return Polyhedron.from_platonicsolid(8)


@pytest.fixture
def part_polyhedron():
    return Polyhedron.from_platonicsolid(4)


def test_part_creation():
    _ = Part()


def test_add_feature(mocker, monkeypatch, part_polyhedron, feature_polyhedron):
    original_part_geometry = MeshGeometry(part_polyhedron)
    part = Part(geometry=original_part_geometry)
    resulting_geometry = Polyhedron.from_platonicsolid(4)
    feature_geometry = MeshGeometry(feature_polyhedron)
    mock_difference_operation = mocker.Mock(return_value=resulting_geometry)
    monkeypatch.setitem(MeshFeature.ALLOWED_OPERATIONS, "difference", mock_difference_operation)

    f1 = part.add_feature(feature_geometry, "difference")

    assert are_mesh_geometries_equal(f1.previous_geometry, original_part_geometry)
    assert are_mesh_geometries_equal(part._part_geometry, MeshGeometry(resulting_geometry))


def test_restore_feature(mocker,monkeypatch, part_polyhedron, feature_polyhedron):
    original_part_geometry = MeshGeometry(part_polyhedron)
    part = Part(geometry=original_part_geometry)
    resulting_geometry = Polyhedron.from_platonicsolid(4)
    feature_geometry = MeshGeometry(feature_polyhedron)
    mock_difference_operation = mocker.Mock(return_value=resulting_geometry)
    monkeypatch.setitem(MeshFeature.ALLOWED_OPERATIONS, "difference", mock_difference_operation)

    f1 = part.add_feature(feature_geometry, "difference")

    assert are_mesh_geometries_equal(part._part_geometry, MeshGeometry(resulting_geometry))

    f1.restore()

    assert are_mesh_geometries_equal(part._part_geometry, original_part_geometry)


def test_remove_single_feature(mocker, monkeypatch, part_polyhedron, feature_polyhedron):
    original_part_geometry = MeshGeometry(part_polyhedron)
    part = Part(geometry=original_part_geometry)
    resulting_geometry = Polyhedron.from_platonicsolid(4)
    feature_geometry = MeshGeometry(feature_polyhedron)
    mock_difference_operation = mocker.Mock(return_value=resulting_geometry)
    monkeypatch.setitem(MeshFeature.ALLOWED_OPERATIONS, "difference", mock_difference_operation)

    _ = part.add_feature(feature_geometry, "difference")

    assert are_mesh_geometries_equal(part._part_geometry, MeshGeometry(resulting_geometry))

    part.clear_features()

    assert are_mesh_geometries_equal(part._part_geometry, original_part_geometry)


def test_remove_multiple_features_all(mocker, monkeypatch, part_polyhedron, feature_polyhedron):
    original_part_geometry = MeshGeometry(part_polyhedron)
    part = Part(geometry=original_part_geometry)
    resulting_shapes = [Polyhedron.from_platonicsolid(4), Polyhedron.from_platonicsolid(8), Polyhedron.from_platonicsolid(12)]
    feature_geometries = [MeshGeometry(shape) for shape in resulting_shapes]
    mock_difference_operation = mocker.Mock(side_effect=resulting_shapes)
    monkeypatch.setitem(MeshFeature.ALLOWED_OPERATIONS, "difference", mock_difference_operation)
    cumulative_resulting_geometry = MeshGeometry(resulting_shapes[-1])

    for geometry in feature_geometries:
        part.add_feature(geometry, operation="difference")

    assert are_mesh_geometries_equal(part._part_geometry, cumulative_resulting_geometry)
    assert len(part.features) == 3

    part.clear_features()

    assert are_mesh_geometries_equal(part._part_geometry, original_part_geometry)
    assert len(part.features) == 0


def test_remove_multiple_features_first_two(mocker, monkeypatch, part_polyhedron, feature_polyhedron):
    original_part_geometry = MeshGeometry(part_polyhedron)
    part = Part(geometry=original_part_geometry)

    # 3 results, one for each feature, plus one for the re-application of feature #3
    resulting_shapes = [Polyhedron.from_platonicsolid(4), Polyhedron.from_platonicsolid(6), Polyhedron.from_platonicsolid(8)] + [Polyhedron.from_platonicsolid(12)]
    feature_geometries = [MeshGeometry(shape) for shape in resulting_shapes]
    mock_difference_operation = mocker.Mock(side_effect=resulting_shapes)
    monkeypatch.setitem(MeshFeature.ALLOWED_OPERATIONS, "difference", mock_difference_operation)
    result_of_third_feature = MeshGeometry(resulting_shapes[2])
    result_after_removing_features = MeshGeometry(resulting_shapes[-1])

    features = []
    for geometry in feature_geometries[:3]:
        features.append(part.add_feature(geometry, operation="difference"))

    assert are_mesh_geometries_equal(part._part_geometry, result_of_third_feature)
    # third feature saves geometry resulting form second feature
    assert are_mesh_geometries_equal(features[-1].previous_geometry, MeshGeometry(resulting_shapes[1]))
    assert len(part.features) == 3

    # remove first two, third is re-applied
    part.clear_features(features_to_clear=features[:2])

    assert are_mesh_geometries_equal(part._part_geometry, result_after_removing_features)

    # third feature is applied directly onto original shape
    assert are_mesh_geometries_equal(features[-1].previous_geometry, original_part_geometry)
    assert len(part.features) == 1


def test_remove_middle_feature(mocker, monkeypatch, part_polyhedron, feature_polyhedron):
    part = Part(shape=part_polyhedron)
    resulting_shapes = [Polyhedron.from_platonicsolid(4), Polyhedron.from_platonicsolid(6), Polyhedron.from_platonicsolid(8)] + [Polyhedron.from_platonicsolid(12)]
    feature_geometries = [MeshGeometry(shape) for shape in resulting_shapes]
    mock_difference_operation = mocker.Mock(side_effect=resulting_shapes)
    monkeypatch.setitem(MeshFeature.ALLOWED_OPERATIONS, "difference", mock_difference_operation)
    result_of_third_feature = MeshGeometry(resulting_shapes[2])
    result_after_removing_features = MeshGeometry(resulting_shapes[-1])

    features = [part.add_feature(geometry, operation="difference") for geometry in feature_geometries[:3]]

    assert are_mesh_geometries_equal(part._part_geometry, result_of_third_feature)
    assert are_mesh_geometries_equal(features[-1].previous_geometry, MeshGeometry(resulting_shapes[1]))
    assert len(part.features) == 3

    middle_feature = features[1]
    part.clear_features(features_to_clear=[middle_feature])

    # features #1 and #3 are being re-applied

    assert are_mesh_geometries_equal(part._part_geometry, result_after_removing_features)
    last_feature = features[-1]
    assert are_mesh_geometries_equal(last_feature.previous_geometry, feature_geometries[0])


def test_operation_unknown_raises_value_error():
    with pytest.raises(ValueError):
        Part().add_feature(None, "convert_mesh_to_brep")

