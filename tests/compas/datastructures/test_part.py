import pytest
from pytest import MonkeyPatch

from numpy import allclose

from compas.datastructures import Part
from compas.datastructures.assembly.part import Feature
from compas.geometry import Polyhedron


RESULTING_POLYHEDRONS = [
    Polyhedron.from_platonicsolid(4),
    Polyhedron.from_platonicsolid(6),
    Polyhedron.from_platonicsolid(8),
]


class TestOperation(object):
    """
    Used to mock a boolean mesh on mesh operation.

    """
    def __init__(self):
        self.mesh_a = None
        self.mesh_b = None

        self.result_index = 0

        self.resulting_geometries = [
            (poly.vertices, poly.faces) for poly in RESULTING_POLYHEDRONS
        ]

    def __call__(self, *args, **kwargs):
        self.mesh_a, self.mesh_b = args[:2]
        result = self.resulting_geometries[self.result_index]
        self.result_index = (self.result_index + 1) % len(self.resulting_geometries)
        return result


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


@pytest.fixture
def test_operation():
    return TestOperation()


def test_part_creation():
    _ = Part()


def test_add_feature(part_polyhedron, feature_polyhedron, test_operation, monkeypatch):
    part = Part(shape=part_polyhedron)
    monkeypatch.setitem(Part.operations, 'difference', test_operation)
    resulting_polyhedron = RESULTING_POLYHEDRONS[0]

    f1 = part.add_feature(feature_polyhedron, 'difference')

    assert f1._shape == feature_polyhedron
    assert f1._operation == test_operation
    assert are_polyhedrons_equal(f1.previous_geometry, part_polyhedron)
    assert are_polyhedrons_equal(part._geometry, resulting_polyhedron)
    assert test_operation.mesh_a


def test_restore_feature(part_polyhedron, feature_polyhedron, test_operation, monkeypatch):
    part = Part(shape=part_polyhedron)
    monkeypatch.setitem(Part.operations, 'difference', test_operation)
    resulting_polyhedron = RESULTING_POLYHEDRONS[0]

    f1 = part.add_feature(shape=feature_polyhedron, operation='difference')

    assert are_polyhedrons_equal(part._geometry, resulting_polyhedron)

    f1.restore()

    assert are_polyhedrons_equal(part._geometry, part_polyhedron)


def test_remove_single_feature(part_polyhedron, feature_polyhedron, test_operation, monkeypatch):
    part = Part(shape=part_polyhedron)
    monkeypatch.setitem(Part.operations, 'difference', test_operation)
    resulting_polyhedron = RESULTING_POLYHEDRONS[0]

    _ = part.add_feature(shape=feature_polyhedron, operation='difference')

    assert are_polyhedrons_equal(part._geometry, resulting_polyhedron)

    part.clear_features()

    assert are_polyhedrons_equal(part._geometry, part_polyhedron)


def test_remove_multiple_features_all(part_polyhedron, feature_polyhedron, test_operation, monkeypatch):
    part = Part(shape=part_polyhedron)
    monkeypatch.setitem(Part.operations, 'difference', test_operation)
    resulting_polyhedron = RESULTING_POLYHEDRONS[2]

    f1 = part.add_feature(shape=feature_polyhedron, operation='difference')
    f2 = part.add_feature(shape=feature_polyhedron, operation='difference')
    f3 = part.add_feature(shape=feature_polyhedron, operation='difference')

    assert are_polyhedrons_equal(part._geometry, resulting_polyhedron)
    assert len(part.features) == 3

    part.clear_features()

    assert are_polyhedrons_equal(part._geometry, part_polyhedron)
    assert len(part.features) == 0


def test_remove_multiple_features_first_two(part_polyhedron, feature_polyhedron, test_operation, monkeypatch):
    part = Part(shape=part_polyhedron)
    monkeypatch.setitem(Part.operations, 'difference', test_operation)
    f1_result = RESULTING_POLYHEDRONS[0]
    f2_result = RESULTING_POLYHEDRONS[1]
    f3_result = RESULTING_POLYHEDRONS[2]

    # operation is called for a total of 4 times (3 when first adding the features and once again when replaying f3 [after removing f1 and f2])
    # 0 because index wraps (index % 3)
    result_after_removing = RESULTING_POLYHEDRONS[0]

    f1 = part.add_feature(shape=feature_polyhedron, operation='difference')
    f2 = part.add_feature(shape=feature_polyhedron, operation='difference')
    f3 = part.add_feature(shape=feature_polyhedron, operation='difference')

    assert are_polyhedrons_equal(part._geometry, f3_result)
    assert len(part.features) == 3
    assert are_polyhedrons_equal(f3.previous_geometry, f2_result)

    part.clear_features(features_to_clear=[f1, f2])

    assert are_polyhedrons_equal(part._geometry, result_after_removing)
    assert len(part.features) == 1
    assert are_polyhedrons_equal(f3.previous_geometry, part_polyhedron)


def test_remove_middle_feature(part_polyhedron, feature_polyhedron, test_operation, monkeypatch):
    part = Part(shape=part_polyhedron)
    monkeypatch.setitem(Part.operations, 'difference', test_operation)
    f1_result = RESULTING_POLYHEDRONS[0]
    f2_result = RESULTING_POLYHEDRONS[1]
    f3_result = RESULTING_POLYHEDRONS[2]

    # operation is called for a total of 4 times (3 when first adding the features and once again when replaying f3 [after removing f2])
    # 0 because index wraps (index % 3)
    result_after_removing = RESULTING_POLYHEDRONS[0]

    f1 = part.add_feature(shape=feature_polyhedron, operation='difference')
    f2 = part.add_feature(shape=feature_polyhedron, operation='difference')
    f3 = part.add_feature(shape=feature_polyhedron, operation='difference')

    assert are_polyhedrons_equal(f3.previous_geometry, f2_result)

    part.clear_features(features_to_clear=[f2])

    assert are_polyhedrons_equal(part._geometry, result_after_removing)
    assert are_polyhedrons_equal(f3.previous_geometry, f1_result)


def test_operation_unknown_raises_value_error():
    with pytest.raises(ValueError):
        Part().add_feature(None, "convert_mesh_to_brep")

