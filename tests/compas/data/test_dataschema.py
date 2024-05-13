import pytest
import compas

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Frame
from compas.geometry import Quaternion
from compas.geometry import Polygon
from compas.geometry import Polyline
from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Polyhedron
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import Pointcloud

from compas.datastructures import Graph
from compas.datastructures import Mesh

if not compas.IPY:
    import jsonschema.exceptions

    @pytest.mark.parametrize(
        "point",
        [
            [0, 0, 0],
            [0.0, 0, 0],
            [0.0, 0.0, 0.0],
        ],
    )
    def test_schema_point_valid(point):
        Point.validate_data(point)

    @pytest.mark.parametrize(
        "point",
        [
            [0, 0],
            [0, 0, 0, 0],
            [0, 0, "0"],
        ],
    )
    def test_schema_point_invalid(point):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Point.validate_data(point)

    @pytest.mark.parametrize(
        "vector",
        [
            [0, 0, 0],
            [0.0, 0, 0],
            [0.0, 0.0, 0.0],
        ],
    )
    def test_schema_vector_valid(vector):
        Vector.validate_data(vector)

    @pytest.mark.parametrize(
        "vector",
        [
            [0, 0],
            [0, 0, 0, 0],
            [0, 0, "0"],
        ],
    )
    def test_schema_vector_invalid(vector):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Vector.validate_data(vector)

    @pytest.mark.parametrize(
        "line",
        [
            {"start": [0, 0, 0], "end": [0, 0, 0]},
            {"start": [0, 0, 0], "end": [0, 0, 0], "extra": 0},
        ],
    )
    def test_schema_line_valid(line):
        Line.validate_data(line)

    @pytest.mark.parametrize(
        "line",
        [
            [[0, 0, 0], [0, 0, 0]],
            {"START": [0, 0, 0], "END": [0, 0, 0]},
        ],
    )
    def test_schema_line_invalid(line):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Line.validate_data(line)

    @pytest.mark.parametrize(
        "plane",
        [
            {"point": [0, 0, 0], "normal": [0, 0, 1]},
        ],
    )
    def test_schema_plane_valid(plane):
        Plane.validate_data(plane)

    @pytest.mark.parametrize(
        "plane",
        [
            [[0, 0, 0], [0, 0, 1]],
            {"POINT": [0, 0, 0], "NORMAL": [0, 0, 1]},
        ],
    )
    def test_schema_plane_invalid(plane):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Plane.validate_data(plane)

    @pytest.mark.parametrize(
        "circle",
        [
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "radius": 0.0},
        ],
    )
    def test_schema_circle_valid(circle):
        Circle.validate_data(circle)

    @pytest.mark.parametrize(
        "circle",
        [
            {"plane": {"point": [0, 0, 0], "normal": [0, 0, 1]}, "radius": 0.0},
            {"plane": [[0, 0, 0], [0, 0, 1]], "radius": 1.0},
            {"PLANE": {"point": [0, 0, 0], "normal": [0, 0, 1]}, "RADIUS": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0]}, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "yaxis": [0, 1, 0]}, "radius": 1.0},
            {"frame": {"xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "radius": 1.0},
            {"FRAME": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "radius": -1.0},
        ],
    )
    def test_schema_circle_invalid(circle):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Circle.validate_data(circle)

    @pytest.mark.parametrize(
        "ellipse",
        [
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "major": 1.0,
                "minor": 0.5,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "major": 1.0,
                "minor": 0.0,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "major": 0.0,
                "minor": 0.5,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "major": 0.0,
                "minor": 0.0,
            },
        ],
    )
    def test_schema_ellipse_valid(ellipse):
        Ellipse.validate_data(ellipse)

    @pytest.mark.parametrize(
        "ellipse",
        [
            {
                "frame": {"point": [0, 0, 0], "yaxis": [0, 1, 0]},
                "major": 1.0,
                "minor": 1.0,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0]},
                "major": 1.0,
                "minor": 1.0,
            },
            {
                "frame": {"xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "major": 1.0,
                "minor": 1.0,
            },
            {
                "frame": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
                "major": 1.0,
                "minor": 0.5,
            },
            {
                "FRAME": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "MAJOR": 1.0,
                "MINOR": 0.5,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "major": 1.0,
                "minor": -1.0,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "major": -1.0,
                "minor": 1.0,
            },
        ],
    )
    def test_schema_ellipse_invalid(ellipse):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Ellipse.validate_data(ellipse)

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
    def test_schema_frame_valid(frame):
        Frame.validate_data(frame)

    @pytest.mark.parametrize(
        "frame",
        [
            {"point": [0, 0, 0], "yaxis": [0, 1, 0], "zaxis": [0, 0, 1]},
            {"point": [0, 0, 0], "xaxis": [1, 0, 0], "zaxis": [0, 0, 1]},
        ],
    )
    def test_schema_frame_invalid(frame):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Frame.validate_data(frame)

    @pytest.mark.parametrize(
        "quaternion",
        [
            {"x": 0, "y": 0, "z": 0, "w": 0},
            {"w": 0, "x": 0, "y": 0, "z": 0},
            {"x": 0, "z": 0, "y": 0, "w": 0},
        ],
    )
    def test_schema_quaternion_valid(quaternion):
        Quaternion.validate_data(quaternion)

    @pytest.mark.parametrize(
        "quaternion",
        [
            {"x": 0, "y": 0, "z": 0},
            {"x": 0, "y": 0, "w": 0},
            {"y": 0, "z": 0, "w": 0},
            {"X": 0, "Y": 0, "Z": 0, "W": 0},
        ],
    )
    def test_schema_quaternion_invalid(quaternion):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Quaternion.validate_data(quaternion)

    @pytest.mark.parametrize(
        "polygon",
        [
            {"points": [[0, 0, 0], [1, 0, 0]]},
            {"points": [[0, 0, 0], [1, 0, 0], [1, 1, 0]]},
        ],
    )
    def test_schema_polygon_valid(polygon):
        Polygon.validate_data(polygon)

    @pytest.mark.parametrize(
        "polygon",
        [
            {"points": [[0, 0, 0]]},
            {"points": [0, 0, 0]},
            {"POINTS": [[0, 0, 0], [1, 0, 0]]},
        ],
    )
    def test_schema_polygon_invalid(polygon):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Polygon.validate_data(polygon)

    @pytest.mark.parametrize(
        "polyline",
        [
            {"points": [[0, 0, 0], [1, 0, 0]]},
            {"points": [[0, 0, 0], [1, 0, 0], [1, 1, 0]]},
        ],
    )
    def test_schema_polyline_valid(polyline):
        Polyline.validate_data(polyline)

    @pytest.mark.parametrize(
        "polyline",
        [
            {"points": [[0, 0, 0]]},
            {"points": [0, 0, 0]},
            {"POINTS": [[0, 0, 0], [1, 0, 0]]},
        ],
    )
    def test_schema_polyline_invalid(polyline):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Polyline.validate_data(polyline)

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
    def test_schema_box_valid(box):
        Box.validate_data(box)

    @pytest.mark.parametrize(
        "box",
        [
            # {
            #     "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
            #     "xsize": 0,
            #     "ysize": 1,
            #     "zsize": 1,
            # },
            # {
            #     "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
            #     "xsize": 1,
            #     "ysize": 1,
            #     "zsize": 0,
            # },
            # {
            #     "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
            #     "xsize": 1,
            #     "ysize": 0,
            #     "zsize": 1,
            # },
            {
                "FRAME": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "XSIZE": 1,
                "YSIZE": 1,
                "ZSIZE": 1,
            },
        ],
    )
    def test_schema_box_invalid(box):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Box.validate_data(box)

    @pytest.mark.parametrize(
        "capsule",
        [
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 0.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": 0.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 0.0, "radius": 0.0},
        ],
    )
    def test_schema_capsule_valid(capsule):
        Capsule.validate_data(capsule)

    @pytest.mark.parametrize(
        "capsule",
        [
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": -1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": -1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": -1.0, "radius": -1.0},
            {"FRAME": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "HEIGHT": 1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "RADIUS": 1.0},
        ],
    )
    def test_schema_capsule_invalid(capsule):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Capsule.validate_data(capsule)

    @pytest.mark.parametrize(
        "cone",
        [
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 0.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": 0.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 0.0, "radius": 0.0},
        ],
    )
    def test_schema_cone_valid(cone):
        Cone.validate_data(cone)

    @pytest.mark.parametrize(
        "cone",
        [
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": -1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": -1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": -1.0, "radius": -1.0},
            {"FRAME": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "HEIGHT": 1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "RADIUS": 1.0},
        ],
    )
    def test_schema_cone_invalid(cone):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Cone.validate_data(cone)

    @pytest.mark.parametrize(
        "cylinder",
        [
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 0.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": 0.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 0.0, "radius": 0.0},
        ],
    )
    def test_schema_cylinder_valid(cylinder):
        Cylinder.validate_data(cylinder)

    @pytest.mark.parametrize(
        "cylinder",
        [
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": -1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": -1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": -1.0, "radius": -1.0},
            {"FRAME": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "HEIGHT": 1.0, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "height": 1.0, "RADIUS": 1.0},
        ],
    )
    def test_schema_cylinder_invalid(cylinder):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Cylinder.validate_data(cylinder)

    @pytest.mark.parametrize(
        "polyhedron",
        [
            {
                "vertices": [[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 0, 1]],
                "faces": [[0, 1, 3], [1, 2, 3], [2, 0, 3], [0, 2, 1]],
            },
        ],
    )
    def test_schema_polyhedron_valid(polyhedron):
        Polyhedron.validate_data(polyhedron)

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
    def test_schema_polyhedron_invalid(polyhedron):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Polyhedron.validate_data(polyhedron)

    @pytest.mark.parametrize(
        "sphere",
        [
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "radius": 0.0},
        ],
    )
    def test_schema_sphere_valid(sphere):
        Sphere.validate_data(sphere)

    @pytest.mark.parametrize(
        "sphere",
        [
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "radius": -1.0},
            {"FRAME": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "radius": 1.0},
            {"frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]}, "RADIUS": 1.0},
        ],
    )
    def test_schema_sphere_invalid(sphere):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Sphere.validate_data(sphere)

    @pytest.mark.parametrize(
        "torus",
        [
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "radius_axis": 1.0,
                "radius_pipe": 1.0,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "radius_axis": 0.0,
                "radius_pipe": 1.0,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "radius_axis": 1.0,
                "radius_pipe": 0.0,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "radius_axis": 0.0,
                "radius_pipe": 0.0,
            },
        ],
    )
    def test_schema_torus_valid(torus):
        Torus.validate_data(torus)

    @pytest.mark.parametrize(
        "torus",
        [
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "radius_axis": -1.0,
                "radius_pipe": 1.0,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "radius_axis": 1.0,
                "radius_pipe": -1.0,
            },
            {
                "frame": {"point": [0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "radius_axis": 1.0,
                "radius_pipe": 1.0,
            },
            {
                "frame": {"point": [0, 0, 0], "yaxis": [0, 1, 0]},
                "radius_axis": 1.0,
                "radius_pipe": 1.0,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0]},
                "radius_axis": 1.0,
                "radius_pipe": 1.0,
            },
            {
                "FRAME": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "radius_axis": 1.0,
                "radius_pipe": 1.0,
            },
            {
                "frame": {"point": [0, 0, 0], "xaxis": [1, 0, 0], "yaxis": [0, 1, 0]},
                "radius": 1.0,
                "radius_pipe": 1.0,
            },
        ],
    )
    def test_schema_torus_invalid(torus):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Torus.validate_data(torus)

    @pytest.mark.parametrize(
        "pointcloud",
        [
            {"points": [[0, 0, 0]]},
            {"points": [[0, 0, 0], [0, 0, 1]]},
            {"points": [[0, 0, 0], [0, 0, 0]]},
        ],
    )
    def test_schema_pointcloud_valid(pointcloud):
        Pointcloud.validate_data(pointcloud)

    @pytest.mark.parametrize(
        "pointcloud",
        [
            {"points": []},
            {"points": [0, 0, 0]},
            {"points": [["0", 0, 0]]},
            {"POINTS": []},
        ],
    )
    def test_schema_pointcloud_invalid(pointcloud):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Pointcloud.validate_data(pointcloud)

    @pytest.mark.parametrize(
        "graph",
        [
            {
                "attributes": {},
                "default_node_attributes": {},
                "default_edge_attributes": {},
                "node": {},
                "edge": {},
                "max_node": -1,
            },
            {
                "attributes": {},
                "default_node_attributes": {},
                "default_edge_attributes": {},
                "node": {},
                "edge": {},
                "max_node": 0,
            },
            {
                "attributes": {},
                "default_node_attributes": {},
                "default_edge_attributes": {},
                "node": {},
                "edge": {},
                "max_node": 1000,
            },
        ],
    )
    def test_schema_graph_valid(graph):
        Graph.validate_data(graph)

    @pytest.mark.parametrize(
        "graph",
        [
            {
                "default_node_attributes": {},
                "default_edge_attributes": {},
                "node": {},
                "edge": {},
                "max_node": -2,
            },
            {
                "default_edge_attributes": {},
                "node": {},
                "edge": {},
                "max_node": -1,
            },
            {
                "default_node_attributes": {},
                "node": {},
                "edge": {},
                "max_node": -1,
            },
            {
                "default_node_attributes": {},
                "default_edge_attributes": {},
                "edge": {},
                "max_node": -1,
            },
            {
                "default_node_attributes": {},
                "default_edge_attributes": {},
                "node": {},
                "max_node": -1,
            },
            {
                "default_node_attributes": {},
                "default_edge_attributes": {},
                "node": {},
                "edge": {},
            },
        ],
    )
    def test_schema_graph_invalid(graph):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Graph.validate_data(graph)

    @pytest.mark.parametrize(
        "mesh",
        [
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -1,
            },
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": 0,
            },
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": 0,
                "max_face": -1,
            },
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": 1000,
            },
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": 1000,
                "max_face": -1,
            },
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {"0": {}, "1": {}, "2": {}},
                "face": {"0": [0, 1, 2]},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -1,
            },
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {"0": {}, "1": {}, "2": {}},
                "face": {"0": [0, 1, 2]},
                "facedata": {"0": {}},
                "edgedata": {"(0, 1)": {}},
                "max_vertex": -1,
                "max_face": -1,
            },
        ],
    )
    def test_schema_mesh_valid(mesh):
        Mesh.validate_data(mesh)

    @pytest.mark.parametrize(
        "mesh",
        [
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -2,
            },
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {},
                "face": {},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -2,
                "max_face": -1,
            },
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {"0": {}, "1": {}, "2": {}},
                "face": {"0": [0, 1]},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -1,
            },
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {"0": {}, "1": {}, "2": {}},
                "face": {"0": [0, 1, 2]},
                "facedata": {"0": {}},
                "edgedata": {"0": {}},
                "max_vertex": -1,
                "max_face": -1,
            },
        ],
    )
    def test_schema_mesh_invalid(mesh):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            Mesh.validate_data(mesh)

    @pytest.mark.parametrize(
        "mesh",
        [
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {0: {}, "1": {}, "2": {}},
                "face": {"0": [0, 1, 2]},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -1,
            },
            {
                "attributes": {},
                "default_vertex_attributes": {},
                "default_edge_attributes": {},
                "default_face_attributes": {},
                "vertex": {"0": {}, "1": {}, "2": {}},
                "face": {0: [0, 1, 2]},
                "facedata": {},
                "edgedata": {},
                "max_vertex": -1,
                "max_face": -1,
            },
        ],
    )
    def test_schema_mesh_failing(mesh):
        with pytest.raises(TypeError):
            Mesh.validate_data(mesh)
