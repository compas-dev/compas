import os
import json
import pytest
import compas


if not compas.IPY:
    import jsonschema


if not compas.IPY:

    @pytest.fixture
    def resolver():
        path = os.path.join(compas.HERE, 'data', 'schemas', 'compas.json')
        with open(path) as f:
            definitions = json.load(f)
        return jsonschema.RefResolver.from_schema(definitions)

    @pytest.fixture
    def point_validator(resolver):
        path = os.path.join(compas.HERE, 'data', 'schemas', 'point.json')
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def vector_validator(resolver):
        path = os.path.join(compas.HERE, 'data', 'schemas', 'vector.json')
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def line_validator(resolver):
        path = os.path.join(compas.HERE, 'data', 'schemas', 'line.json')
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def plane_validator(resolver):
        path = os.path.join(compas.HERE, 'data', 'schemas', 'plane.json')
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def circle_validator(resolver):
        path = os.path.join(compas.HERE, 'data', 'schemas', 'circle.json')
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def ellipse_validator(resolver):
        path = os.path.join(compas.HERE, 'data', 'schemas', 'ellipse.json')
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def frame_validator(resolver):
        path = os.path.join(compas.HERE, 'data', 'schemas', 'frame.json')
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator


if not compas.IPY:

    @pytest.mark.parametrize("point", [
        [0, 0, 0],
        [0.0, 0, 0],
        [0.0, 0.0, 0.0]])
    def test_schema_point_valid(point_validator, point):
        point_validator.validate(point)

    @pytest.mark.parametrize("point", [
        [0, 0],
        [0, 0, 0, 0],
        [0, 0, '0']])
    def test_schema_point_invalid(point_validator, point):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            point_validator.validate(point)

    @pytest.mark.parametrize("vector", [
        [0, 0, 0],
        [0.0, 0, 0],
        [0.0, 0.0, 0.0]])
    def test_schema_vector_valid(vector_validator, vector):
        vector_validator.validate(vector)

    @pytest.mark.parametrize("vector", [
        [0, 0],
        [0, 0, 0, 0],
        [0, 0, '0']])
    def test_schema_vector_invalid(vector_validator, vector):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            vector_validator.validate(vector)

    @pytest.mark.parametrize("line", [
        {'start': [0, 0, 0], 'end': [0, 0, 0]},
        {'start': [0, 0, 0], 'end': [0, 0, 0], 'extra': 0}])
    def test_schema_line_valid(line_validator, line):
        line_validator.validate(line)

    @pytest.mark.parametrize("line", [
        [[0, 0, 0], [0, 0, 0]],
        {'START': [0, 0, 0], 'END': [0, 0, 0]}
    ])
    def test_schema_line_invalid(line_validator, line):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            line_validator.validate(line)

    @pytest.mark.parametrize("plane", [
        {'point': [0, 0, 0], 'normal': [0, 0, 1]}
    ])
    def test_schema_plane_valid(plane_validator, plane):
        plane_validator.validate(plane)

    @pytest.mark.parametrize("plane", [
        [[0, 0, 0], [0, 0, 1]],
        {'POINT': [0, 0, 0], 'NORMAL': [0, 0, 1]}
    ])
    def test_schema_plane_invalid(plane_validator, plane):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            plane_validator.validate(plane)

    @pytest.mark.parametrize("circle", [
        {'plane': {'point': [0, 0, 0], 'normal': [0, 0, 1]}, 'radius': 1.0}
    ])
    def test_schema_circle_valid(circle_validator, circle):
        circle_validator.validate(circle)

    @pytest.mark.parametrize("circle", [
        {'plane': {'point': [0, 0, 0], 'normal': [0, 0, 1]}, 'radius': 0.0},
        {'plane': [[0, 0, 0], [0, 0, 1]], 'radius': 1.0},
        {'PLANE': {'point': [0, 0, 0], 'normal': [0, 0, 1]}, 'RADIUS': 1.0}
    ])
    def test_schema_circle_invalid(circle_validator, circle):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            circle_validator.validate(circle)

    @pytest.mark.parametrize("ellipse", [
        {'plane': {'point': [0, 0, 0], 'normal': [0, 0, 1]}, 'major': 1.0, 'minor': 0.5}
    ])
    def test_schema_ellipse_valid(ellipse_validator, ellipse):
        ellipse_validator.validate(ellipse)

    @pytest.mark.parametrize("ellipse", [
        {'plane': {'point': [0, 0, 0], 'normal': [0, 0, 1]}, 'major': 1.0, 'minor': 0.0},
        {'plane': {'point': [0, 0, 0], 'normal': [0, 0, 1]}, 'major': 0.0, 'minor': 0.5},
        {'plane': {'point': [0, 0, 0], 'normal': [0, 0, 1]}, 'major': 0.0, 'minor': 0.0},
        {'plane': [[0, 0, 0], [0, 0, 1]], 'major': 1.0, 'minor': 0.5},
        {'PLANE': {'point': [0, 0, 0], 'normal': [0, 0, 1]}, 'MAJOR': 1.0, 'MINOR': 0.5}
    ])
    def test_schema_ellipse_invalid(ellipse_validator, ellipse):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            ellipse_validator.validate(ellipse)

    @pytest.mark.parametrize("frame", [
        {'point': [0, 0, 0], 'xaxis': [1, 0, 0], 'yaxis': [0, 1, 0]},
        {'point': [0, 0, 0], 'yaxis': [0, 1, 0], 'xaxis': [1, 0, 0]},
        {'point': [0, 0, 0], 'xaxis': [1, 0, 0], 'yaxis': [0, 1, 0], 'zaxis': [0, 0, 1]},
        {'point': [0, 0, 0], 'xaxis': [1, 0, 0], 'zaxis': [0, 0, 1], 'yaxis': [0, 1, 0]}
    ])
    def test_schema_frame_valid(frame_validator, frame):
        frame_validator.validate(frame)

    @pytest.mark.parametrize("frame", [
        {'point': [0, 0, 0], 'yaxis': [0, 1, 0], 'zaxis': [0, 0, 1]},
        {'point': [0, 0, 0], 'xaxis': [1, 0, 0], 'zaxis': [0, 0, 1]}
    ])
    def test_schema_frame_invalid(frame_validator, frame):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            frame_validator.validate(frame)
