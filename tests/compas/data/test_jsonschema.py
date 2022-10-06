import os
import json
import pytest
import compas

if not compas.IPY:
    import jsonschema


if not compas.IPY:

    @pytest.fixture
    def resolver():
        path = os.path.join(compas.HERE, "data", "schemas", "compas.json")
        with open(path) as f:
            definitions = json.load(f)
        return jsonschema.RefResolver.from_schema(definitions)

    @pytest.fixture
    def point_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "point.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def vector_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "vector.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def line_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "line.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def plane_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "plane.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def circle_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "circle.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def ellipse_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "ellipse.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def frame_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "frame.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def quaternion_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "quaternion.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def polygon_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "polygon.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def polyline_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "polyline.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def box_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "box.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def capsule_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "capsule.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def cone_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "cone.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def cylinder_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "cylinder.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def polyhedron_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "polyhedron.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def sphere_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "sphere.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def torus_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "torus.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def pointcloud_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "pointcloud.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def graph_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "graph.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def halfedge_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "halfedge.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator

    @pytest.fixture
    def halfface_validator(resolver):
        path = os.path.join(compas.HERE, "data", "schemas", "halfface.json")
        with open(path) as f:
            schema = json.load(f)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        return validator


if not compas.IPY:

    @pytest.mark.parametrize("point", [[0, 0, 0], [0.0, 0, 0], [0.0, 0.0, 0.0]])
    def test_schema_point_valid(point_validator, point):
        point_validator.validate(point)

    @pytest.mark.parametrize("point", [[0, 0], [0, 0, 0, 0], [0, 0, "0"]])
    def test_schema_point_invalid(point_validator, point):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            point_validator.validate(point)

    @pytest.mark.parametrize("vector", [[0, 0, 0], [0.0, 0, 0], [0.0, 0.0, 0.0]])
    def test_schema_vector_valid(vector_validator, vector):
        vector_validator.validate(vector)

    @pytest.mark.parametrize("vector", [[0, 0], [0, 0, 0, 0], [0, 0, "0"]])
    def test_schema_vector_invalid(vector_validator, vector):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            vector_validator.validate(vector)

    @pytest.mark.parametrize(
        "line",
        [
            {"start": [0, 0, 0], "end": [0, 0, 0]},
            {"start": [0, 0, 0], "end": [0, 0, 0], "extra": 0},
        ],
    )
    def test_schema_line_valid(line_validator, line):
        line_validator.validate(line)

    @pytest.mark.parametrize("line", [[[0, 0, 0], [0, 0, 0]], {"START": [0, 0, 0], "END": [0, 0, 0]}])
    def test_schema_line_invalid(line_validator, line):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            line_validator.validate(line)

    @pytest.mark.parametrize("plane", [{"point": [0, 0, 0], "normal": [0, 0, 1]}])
    def test_schema_plane_valid(plane_validator, plane):
        plane_validator.validate(plane)

    @pytest.mark.parametrize("plane", [[[0, 0, 0], [0, 0, 1]], {"POINT": [0, 0, 0], "NORMAL": [0, 0, 1]}])
    def test_schema_plane_invalid(plane_validator, plane):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            plane_validator.validate(plane)

    @pytest.mark.parametrize("circle", [{"plane": {"point": [0, 0, 0], "normal": [0, 0, 1]}, "radius": 1.0}])
    def test_schema_circle_valid(circle_validator, circle):
        circle_validator.validate(circle)

    @pytest.mark.parametrize(
        "circle",
        [
            {"plane": {"point": [0, 0, 0], "normal": [0, 0, 1]}, "radius": 0.0},
            {"plane": [[0, 0, 0], [0, 0, 1]], "radius": 1.0},
            {"PLANE": {"point": [0, 0, 0], "normal": [0, 0, 1]}, "RADIUS": 1.0},
        ],
    )
    def test_schema_circle_invalid(circle_validator, circle):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            circle_validator.validate(circle)

    @pytest.mark.parametrize(
        "ellipse",
        [
            {
                "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                "major": 1.0,
                "minor": 0.5,
            }
        ],
    )
    def test_schema_ellipse_valid(ellipse_validator, ellipse):
        ellipse_validator.validate(ellipse)

    @pytest.mark.parametrize(
        "ellipse",
        [
            {
                "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                "major": 1.0,
                "minor": 0.0,
            },
            {
                "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                "major": 0.0,
                "minor": 0.5,
            },
            {
                "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                "major": 0.0,
                "minor": 0.0,
            },
            {"plane": [[0, 0, 0], [0, 0, 1]], "major": 1.0, "minor": 0.5},
            {
                "PLANE": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                "MAJOR": 1.0,
                "MINOR": 0.5,
            },
        ],
    )
    def test_schema_ellipse_invalid(ellipse_validator, ellipse):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            ellipse_validator.validate(ellipse)

    @pytest.mark.parametrize(
        "frame",
        [
            {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
            {"point": [0, 0, 0], "yaxis": [0, 1, 0], "xaxis": [1, 0, 0]},
            {
                "point": [0, 0, 0],
                "xaxis": [1, 0, 0],
                "yaxis": [0, 1, 0],
                "zaxis": [0, 0, 1],
            },
            {
                "point": [0, 0, 0],
                "xaxis": [1, 0, 0],
                "zaxis": [0, 0, 1],
                "yaxis": [0, 1, 0],
            },
        ],
    )
    def test_schema_frame_valid(frame_validator, frame):
        frame_validator.validate(frame)

    @pytest.mark.parametrize(
        "frame",
        [
            {"point": [0, 0, 0], "yaxis": [0, 1, 0], "zaxis": [0, 0, 1]},
            {"point": [0, 0, 0], "xaxis": [1, 0, 0], "zaxis": [0, 0, 1]},
        ],
    )
    def test_schema_frame_invalid(frame_validator, frame):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            frame_validator.validate(frame)

    @pytest.mark.parametrize(
        "quaternion",
        [
            {"x": 0, "y": 0, "z": 0, "w": 0},
            {"w": 0, "x": 0, "y": 0, "z": 0},
            {"x": 0, "z": 0, "y": 0, "w": 0},
        ],
    )
    def test_schema_quaternion_valid(quaternion_validator, quaternion):
        quaternion_validator.validate(quaternion)

    @pytest.mark.parametrize(
        "quaternion",
        [
            {"x": 0, "y": 0, "z": 0},
            {"x": 0, "y": 0, "w": 0},
            {"y": 0, "z": 0, "w": 0},
            {"X": 0, "Y": 0, "Z": 0, "W": 0},
        ],
    )
    def test_schema_quaternion_invalid(quaternion_validator, quaternion):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            quaternion_validator.validate(quaternion)

    @pytest.mark.parametrize(
        "polygon",
        [
            {"points": [[0, 0, 0], [1, 0, 0]]},
            {"points": [[0, 0, 0], [1, 0, 0], [1, 1, 0]]},
        ],
    )
    def test_schema_polygon_valid(polygon_validator, polygon):
        polygon_validator.validate(polygon)

    @pytest.mark.parametrize(
        "polygon",
        [
            {"points": [[0, 0, 0]]},
            {"points": [0, 0, 0]},
            {"POINTS": [[0, 0, 0], [1, 0, 0]]},
        ],
    )
    def test_schema_polygon_invalid(polygon_validator, polygon):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            polygon_validator.validate(polygon)

    @pytest.mark.parametrize(
        "polyline",
        [
            {"points": [[0, 0, 0], [1, 0, 0]]},
            {"points": [[0, 0, 0], [1, 0, 0], [1, 1, 0]]},
        ],
    )
    def test_schema_polyline_valid(polyline_validator, polyline):
        polyline_validator.validate(polyline)

    @pytest.mark.parametrize(
        "polyline",
        [
            {"points": [[0, 0, 0]]},
            {"points": [0, 0, 0]},
            {"POINTS": [[0, 0, 0], [1, 0, 0]]},
        ],
    )
    def test_schema_polyline_invalid(polyline_validator, polyline):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            polyline_validator.validate(polyline)

    @pytest.mark.parametrize(
        "box",
        [
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "xsize": 1,
                "ysize": 1,
                "zsize": 1,
            }
        ],
    )
    def test_schema_box_valid(box_validator, box):
        box_validator.validate(box)

    @pytest.mark.parametrize(
        "box",
        [
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "xsize": 0,
                "ysize": 1,
                "zsize": 1,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "xsize": 1,
                "ysize": 1,
                "zsize": 0,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "xsize": 1,
                "ysize": 0,
                "zsize": 1,
            },
            {
                "FRAME": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "XSIZE": 1,
                "YSIZE": 1,
                "ZSIZE": 1,
            },
        ],
    )
    def test_schema_box_invalid(box_validator, box):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            box_validator.validate(box)

    @pytest.mark.parametrize("capsule", [{"line": {"start": [0, 0, 0], "end": [1, 0, 0]}, "radius": 1.0}])
    def test_schema_capsule_valid(capsule_validator, capsule):
        capsule_validator.validate(capsule)

    @pytest.mark.parametrize(
        "capsule",
        [
            {"start": [0, 0, 0], "end": [1, 0, 0], "radius": 1.0},
            {"line": [[0, 0, 0], [1, 0, 0]], "radius": 1.0},
            {"line": {"start": [0, 0, 0], "end": [1, 0, 0]}, "radius": 0.0},
            {"LINE": {"start": [0, 0, 0], "end": [1, 0, 0]}, "RADIUS": 1.0},
        ],
    )
    def test_schema_capsule_invalid(capsule_validator, capsule):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            capsule_validator.validate(capsule)

    @pytest.mark.parametrize(
        "cone",
        [
            {
                "circle": {
                    "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                    "radius": 1.0,
                },
                "height": 1.0,
            }
        ],
    )
    def test_schema_cone_valid(cone_validator, cone):
        cone_validator.validate(cone)

    @pytest.mark.parametrize(
        "cone",
        [
            {
                "circle": {
                    "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                    "radius": 1.0,
                },
                "height": 0.0,
            },
            {
                "circle": {
                    "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                    "radius": 0.0,
                },
                "height": 1.0,
            },
            {
                "circle": {
                    "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                    "radius": 0.0,
                },
                "height": 0.0,
            },
            {
                "CIRCLE": {
                    "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                    "radius": 0.0,
                },
                "HEIGHT": 0.0,
            },
        ],
    )
    def test_schema_cone_invalid(cone_validator, cone):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            cone_validator.validate(cone)

    @pytest.mark.parametrize(
        "cylinder",
        [
            {
                "circle": {
                    "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                    "radius": 1.0,
                },
                "height": 1.0,
            }
        ],
    )
    def test_schema_cylinder_valid(cylinder_validator, cylinder):
        cylinder_validator.validate(cylinder)

    @pytest.mark.parametrize(
        "cylinder",
        [
            {
                "circle": {
                    "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                    "radius": 1.0,
                },
                "height": 0.0,
            },
            {
                "circle": {
                    "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                    "radius": 0.0,
                },
                "height": 1.0,
            },
            {
                "circle": {
                    "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                    "radius": 0.0,
                },
                "height": 0.0,
            },
            {
                "CIRCLE": {
                    "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                    "radius": 0.0,
                },
                "HEIGHT": 0.0,
            },
        ],
    )
    def test_schema_cylinder_invalid(cylinder_validator, cylinder):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            cylinder_validator.validate(cylinder)

    @pytest.mark.parametrize(
        "polyhedron",
        [
            {
                "vertices": [[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 0, 1]],
                "faces": [[0, 1, 3], [1, 2, 3], [2, 0, 3], [0, 2, 1]],
            },
        ],
    )
    def test_schema_polyhedron_valid(polyhedron_validator, polyhedron):
        polyhedron_validator.validate(polyhedron)

    @pytest.mark.parametrize(
        "polyhedron",
        [
            {
                "vertices": [[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 0, 1]],
                "faces": [[0, 1, 3], [1, 2, 3], [2, 0, 3]],
            },
            {
                "vertices": [[0, 0, 0], [1, 0, 0], [1, 1, 0]],
                "faces": [[0, 1, 3], [1, 2, 3], [2, 0, 3], [0, 2, 1]],
            },
            {"vertices": [[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 0, 1]], "faces": []},
            {"vertices": [], "faces": [[0, 1, 3], [1, 2, 3], [2, 0, 3], [0, 2, 1]]},
            {"vertices": [], "faces": []},
        ],
    )
    def test_schema_polyhedron_invalid(polyhedron_validator, polyhedron):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            polyhedron_validator.validate(polyhedron)

    @pytest.mark.parametrize("sphere", [{"point": [0, 0, 0], "radius": 1.0}])
    def test_schema_sphere_valid(sphere_validator, sphere):
        sphere_validator.validate(sphere)

    @pytest.mark.parametrize(
        "sphere",
        [
            {"point": [0, 0], "radius": 1},
            {"point": [0, 0, 0, 0], "radius": 1},
            {"point": [0, 0, 0], "radius": 0},
            {"POINT": [0, 0, 0], "RADIUS": 1},
        ],
    )
    def test_schema_sphere_invalid(sphere_validator, sphere):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            sphere_validator.validate(sphere)

    @pytest.mark.parametrize(
        "torus",
        [
            {
                "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                "radius_axis": 1.0,
                "radius_pipe": 1.0,
            }
        ],
    )
    def test_schema_torus_valid(torus_validator, torus):
        torus_validator.validate(torus)

    @pytest.mark.parametrize(
        "torus",
        [
            {
                "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                "radius_axis": 1.0,
                "radius_pipe": 0.0,
            },
            {
                "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                "radius_axis": 0.0,
                "radius_pipe": 1.0,
            },
            {
                "plane": {"point": [0, 0, 0], "normal": [0, 0, 1]},
                "radius_axis": 0.0,
                "radius_pipe": 0.0,
            },
        ],
    )
    def test_schema_torus_invalid(torus_validator, torus):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            torus_validator.validate(torus)

    @pytest.mark.parametrize(
        "pointcloud",
        [
            {"points": [[0, 0, 0]]},
            {"points": [[0, 0, 0], [0, 0, 1]]},
            {"points": [[0, 0, 0], [0, 0, 0]]},
        ],
    )
    def test_schema_pointcloud_valid(pointcloud_validator, pointcloud):
        pointcloud_validator.validate(pointcloud)

    @pytest.mark.parametrize(
        "pointcloud",
        [
            {"points": []},
            {"points": [0, 0, 0]},
            {"points": [["0", 0, 0]]},
            {"POINTS": []},
        ],
    )
    def test_schema_pointcloud_invalid(pointcloud_validator, pointcloud):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            pointcloud_validator.validate(pointcloud)

    @pytest.mark.parametrize(
        "graph",
        [
            {
                "attributes": {},
                "dna": {},
                "dea": {},
                "node": {},
                "edge": {},
                "adjacency": {},
                "max_node": -1,
            },
            {
                "attributes": {},
                "dna": {},
                "dea": {},
                "node": {},
                "edge": {},
                "adjacency": {},
                "max_node": 0,
            },
            {
                "attributes": {},
                "dna": {},
                "dea": {},
                "node": {},
                "edge": {},
                "adjacency": {},
                "max_node": 1000,
            },
        ],
    )
    def test_schema_graph_valid(graph_validator, graph):
        graph_validator.validate(graph)

    @pytest.mark.parametrize(
        "graph",
        [
            {
                "attributes": {},
                "dna": {},
                "dea": {},
                "node": {},
                "edge": {},
                "adjacency": {},
                "max_node": -2,
            },
            {
                "dna": {},
                "dea": {},
                "node": {},
                "edge": {},
                "adjacency": {},
                "max_node": -1,
            },
            {
                "attributes": {},
                "dea": {},
                "node": {},
                "edge": {},
                "adjacency": {},
                "max_node": -1,
            },
            {
                "attributes": {},
                "dna": {},
                "node": {},
                "edge": {},
                "adjacency": {},
                "max_node": -1,
            },
            {
                "attributes": {},
                "dna": {},
                "dea": {},
                "edge": {},
                "adjacency": {},
                "max_node": -1,
            },
            {
                "attributes": {},
                "dna": {},
                "dea": {},
                "node": {},
                "adjacency": {},
                "max_node": -1,
            },
            {
                "attributes": {},
                "dna": {},
                "dea": {},
                "node": {},
                "edge": {},
                "max_node": -1,
            },
            {
                "attributes": {},
                "dna": {},
                "dea": {},
                "node": {},
                "edge": {},
                "adjacency": {},
            },
        ],
    )
    def test_schema_graph_invalid(graph_validator, graph):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            graph_validator.validate(graph)

    @pytest.mark.parametrize(
        "halfedge",
        [
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -1,
            },
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": 0,
            },
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": 0,
                "max_face": -1,
            },
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": 1000,
            },
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": 1000,
                "max_face": -1,
            },
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {"0": {}, "1": {}, "2": {}},
                "face": {"0": [0, 1, 2]},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -1,
            },
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {"0": {}, "1": {}, "2": {}},
                "face": {"0": [0, 1, 2]},
                "facedata": {"0": {}},
                "edgedata": {"0-1": {}},
                "max_vertex": -1,
                "max_face": -1,
            },
        ],
    )
    def test_schema_halfedge_valid(halfedge_validator, halfedge):
        halfedge_validator.validate(halfedge)

    @pytest.mark.parametrize(
        "halfedge",
        [
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -2,
            },
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -2,
                "max_face": -1,
            },
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {"0": {}, "1": {}, "2": {}},
                "face": {"0": [0, 1]},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -1,
            },
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {"0": {}, "1": {}, "2": {}},
                "face": {"0": [0, 1, 2]},
                "facedata": {"0": {}},
                "edgedata": {"0": {}},
                "max_vertex": -1,
                "max_face": -1,
            },
        ],
    )
    def test_schema_halfedge_invalid(halfedge_validator, halfedge):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            halfedge_validator.validate(halfedge)

    @pytest.mark.parametrize(
        "halfedge",
        [
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {0: {}, "1": {}, "2": {}},
                "face": {"0": [0, 1, 2]},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -1,
            },
            {
                "attributes": {},
                "dva": {},
                "dea": {},
                "dfa": {},
                "vertex": {"0": {}, "1": {}, "2": {}},
                "face": {0: [0, 1, 2]},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -1,
            },
        ],
    )
    def test_schema_halfedge_failing(halfedge_validator, halfedge):
        with pytest.raises(TypeError):
            halfedge_validator.validate(halfedge)
