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
        {'sp': [0, 0, 0], 'ep': [0, 0, 0]}
    ])
    def test_schema_line_invalid(line_validator, line):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            line_validator.validate(line)
