import pytest

from compas.datastructures import Mesh
from compas.files import GLTFDocument
from compas.files.gltf.constants import MODE_LINE_LOOP
from compas.files.gltf.constants import MODE_LINE_STRIP
from compas.files.gltf.constants import MODE_POINTS
from compas.files.gltf.constants import MODE_TRIANGLE_FAN
from compas.files.gltf.constants import MODE_TRIANGLE_STRIP
from compas.files.gltf.data_classes import PrimitiveData
from compas.files.gltf.gltf_conversions import GLTFConversionWarning
from compas.files.gltf.gltf_conversions import _base_scene_context
from compas.files.gltf.gltf_conversions import gltf_line_loop_to_polyline
from compas.files.gltf.gltf_conversions import gltf_lines_to_lines
from compas.files.gltf.gltf_conversions import gltf_points_to_pointcloud
from compas.files.gltf.gltf_conversions import gltf_triangle_strip_to_mesh
from compas.files.gltf.gltf_conversions import line_to_gltf_primitive
from compas.files.gltf.gltf_conversions import mesh_to_gltf_primitive
from compas.files.gltf.gltf_conversions import pointcloud_to_gltf_primitive
from compas.files.gltf.gltf_conversions import polyline_to_gltf_primitive
from compas.files.gltf.gltf_mesh import GLTFMesh
from compas.geometry import Pointcloud
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Translation
from compas.geometry import Vector
from compas.scene import Scene


def test_explicit_gltf_to_compas_primitive_conversions():
    positions = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]

    pointcloud = gltf_points_to_pointcloud(positions, [2, 0])
    lines = gltf_lines_to_lines(positions, [0, 1, 2, 3])
    loop = gltf_line_loop_to_polyline(positions)
    strip = gltf_triangle_strip_to_mesh(positions)

    assert [list(point) for point in pointcloud] == [positions[2], positions[0]]
    assert len(lines) == 2
    assert lines[0] == Line(positions[0], positions[1])
    assert loop.is_closed
    assert list(strip.faces()) == [0, 1]
    assert strip.face_vertices(0) == [0, 1, 2]
    assert strip.face_vertices(1) == [2, 1, 3]


def test_explicit_compas_to_gltf_primitive_conversions():
    mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
    pointcloud = Pointcloud([[0, 0, 0], [1, 1, 1]])
    line = Line([0, 0, 0], [1, 0, 0])
    polyline = Polyline([[0, 0, 0], [1, 0, 0], [0, 0, 0]])

    assert mesh_to_gltf_primitive(mesh).mode == 4
    assert len(mesh_to_gltf_primitive(mesh).indices) == 6
    assert pointcloud_to_gltf_primitive(pointcloud).mode == MODE_POINTS
    assert line_to_gltf_primitive(line).mode == 1
    assert polyline_to_gltf_primitive(polyline).mode == MODE_LINE_LOOP


def test_gltf_to_scene_preserves_hierarchy_transform_and_primitive_types():
    document = GLTFDocument()
    source_scene = document.add_scene(name="Model")
    node = source_scene.add_child(node_name="Geometry")
    node.translation = [1.0, 2.0, 3.0]
    node.add_child(child_name="Child")

    primitives = [
        PrimitiveData({"POSITION": [[0, 0, 0], [1, 1, 1]]}, [0, 1], mode=MODE_POINTS),
        PrimitiveData({"POSITION": [[0, 0, 0], [1, 0, 0], [1, 1, 0]]}, [0, 1, 2], mode=MODE_LINE_STRIP),
        PrimitiveData(
            {"POSITION": [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]]},
            [0, 1, 2, 3],
            mode=MODE_TRIANGLE_STRIP,
        ),
    ]
    node.mesh_key = GLTFMesh(primitives, document, mesh_name="Mixed").key

    scene = Scene.from_gltf(document)

    root = scene.find_by_name("Geometry")
    assert root is not None
    assert root.transformation.matrix == Translation.from_vector([1, 2, 3]).matrix
    assert scene.find_by_name("Child").parent is root
    assert any(isinstance(sceneobject.item, Pointcloud) for sceneobject in scene.objects)
    assert any(isinstance(sceneobject.item, Polyline) for sceneobject in scene.objects)
    meshes = [sceneobject.item for sceneobject in scene.objects if isinstance(sceneobject.item, Mesh)]
    assert len(meshes) == 1
    assert meshes[0].number_of_faces() == 2


@pytest.mark.parametrize("mode", [MODE_LINE_LOOP, MODE_TRIANGLE_FAN])
def test_gltf_to_scene_expands_loop_and_fan_modes(mode):
    document = GLTFDocument()
    source_scene = document.add_scene()
    node = source_scene.add_child()
    positions = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    primitive = PrimitiveData({"POSITION": positions}, [0, 1, 2, 3], mode=mode)
    node.mesh_key = GLTFMesh([primitive], document).key

    scene = Scene.from_gltf(document)

    if mode == MODE_LINE_LOOP:
        polyline = next(sceneobject.item for sceneobject in scene.objects if isinstance(sceneobject.item, Polyline))
        assert polyline.is_closed
    else:
        mesh = next(sceneobject.item for sceneobject in scene.objects if isinstance(sceneobject.item, Mesh))
        assert mesh.number_of_faces() == 2


def test_scene_to_gltf_preserves_hierarchy_and_supported_geometry():
    with _base_scene_context():
        scene = Scene(name="Model")
        group = scene.add_group("Group", transformation=Translation.from_vector([1, 2, 3]))
        mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
        scene.add(mesh, parent=group, name="Surface")
        scene.add(Pointcloud([[0, 0, 0], [1, 1, 1]]), parent=group, name="Points")
        scene.add(Polyline([[0, 0, 0], [1, 0, 0], [1, 1, 0]]), parent=group, name="Path")

    document = scene.to_gltf()

    assert document.default_scene_key == 0
    assert document.scenes[0].name == "Model"
    assert len(document.meshes) == 3
    root = document.nodes[document.scenes[0].children[0]]
    assert root.name == "Group"
    assert root.matrix == Translation.from_vector([1, 2, 3]).matrix
    assert [document.nodes[key].name for key in root.children] == ["Surface", "Points", "Path"]
    assert len(document.meshes[document.nodes[root.children[0]].mesh_key].faces) == 2
    assert document.meshes[document.nodes[root.children[1]].mesh_key].primitive_data_list[0].mode == MODE_POINTS
    assert document.meshes[document.nodes[root.children[2]].mesh_key].primitive_data_list[0].mode == MODE_LINE_STRIP


def test_scene_to_gltf_warns_for_unsupported_items_and_preserves_children():
    with _base_scene_context():
        scene = Scene(name="Model")
        unsupported = scene.add(Vector(1, 0, 0), name="Direction")
        scene.add(Pointcloud([[0, 0, 0]]), parent=unsupported, name="Child")

    with pytest.warns(GLTFConversionWarning, match="Vector"):
        document = scene.to_gltf()

    root = document.nodes[document.scenes[0].children[0]]
    assert root.mesh_key is None
    assert len(root.children) == 1
    assert document.nodes[root.children[0]].mesh_key is not None
