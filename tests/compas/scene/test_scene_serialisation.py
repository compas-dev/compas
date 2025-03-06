import compas

if not compas.IPY:
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
    from compas.geometry import Vector
    from compas.geometry import Plane
    from compas.datastructures import Mesh
    from compas.datastructures import Graph
    from compas.datastructures import VolMesh
    from compas.scene import Group

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

    def test_scene_serialisation(items, mocker):
        if compas.IPY:
            mocker.patch("compas.is_rhino", return_value=False)

        scene1 = Scene()
        for item in items:
            scene1.add(item)

        scene2 = Scene.from_jsonstring(scene1.to_jsonstring())
        assert assert_is_data_equal(scene1, scene2)

    def test_scene_serialisation_empty():
        scene = Scene()
        scene = compas.json_loads(compas.json_dumps(scene))

        assert isinstance(scene, Scene)
