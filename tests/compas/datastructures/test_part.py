import pytest

from compas.geometry import allclose
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

##############################################################
#  Features
##############################################################


def test_add_feature(mocker, part_polyhedron, feature_polyhedron):
    original_part_geometry = MeshGeometry(part_polyhedron)
    part = Part(geometry=original_part_geometry)
    resulting_geometry = Polyhedron.from_platonicsolid(4)
    feature_geometry = MeshGeometry(feature_polyhedron)
    mocker.patch("compas.datastructures.assembly.part.MeshFeature._apply_feature")
    f1 = MeshFeature(part, feature_geometry, "difference")
    f1._apply_feature.return_value = mocker.Mock(return_value=resulting_geometry)

    part.add_feature(f1)
    f1.apply()

    assert are_mesh_geometries_equal(f1.previous_geometry, original_part_geometry)
    assert are_mesh_geometries_equal(part._part_geometry, MeshGeometry(resulting_geometry))


def test_restore_feature(mocker, part_polyhedron, feature_polyhedron):
    original_part_geometry = MeshGeometry(part_polyhedron)
    part = Part(geometry=original_part_geometry)
    resulting_geometry = Polyhedron.from_platonicsolid(4)
    feature_geometry = MeshGeometry(feature_polyhedron)
    mocker.patch("compas.datastructures.assembly.part.MeshFeature._apply_feature")
    f1 = MeshFeature(part, feature_geometry, "difference")
    f1._apply_feature.return_value = mocker.Mock(return_value=resulting_geometry)

    part.add_feature(f1)
    f1.apply()

    assert are_mesh_geometries_equal(part._part_geometry, MeshGeometry(resulting_geometry))

    f1.restore()

    assert are_mesh_geometries_equal(part._part_geometry, original_part_geometry)


def test_remove_single_feature(mocker, part_polyhedron, feature_polyhedron):
    original_part_geometry = MeshGeometry(part_polyhedron)
    part = Part(geometry=original_part_geometry)
    resulting_geometry = Polyhedron.from_platonicsolid(4)
    feature_geometry = MeshGeometry(feature_polyhedron)
    f1 = MeshFeature(part, feature_geometry, "difference")
    mocker.patch("compas.datastructures.assembly.part.MeshFeature._apply_feature")
    f1._apply_feature.return_value = mocker.Mock(return_value=resulting_geometry)

    part.add_feature(f1)
    f1.apply()

    assert are_mesh_geometries_equal(part._part_geometry, MeshGeometry(resulting_geometry))

    part.clear_features()

    assert are_mesh_geometries_equal(part._part_geometry, original_part_geometry)


def test_operation_unknown_raises_value_error(mocker):
    with pytest.raises(ValueError):
        Part().add_geometry_feature(MeshGeometry(geometry=mocker.Mock()), "convert_mesh_to_brep")

