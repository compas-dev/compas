"""Conversions between glTF documents and COMPAS scenes."""

import warnings
from contextlib import contextmanager
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Sequence
from typing import cast

from compas.datastructures import Mesh
from compas.files.gltf.constants import MODE_LINE_LOOP
from compas.files.gltf.constants import MODE_LINE_STRIP
from compas.files.gltf.constants import MODE_LINES
from compas.files.gltf.constants import MODE_POINTS
from compas.files.gltf.constants import MODE_TRIANGLE_FAN
from compas.files.gltf.constants import MODE_TRIANGLE_STRIP
from compas.files.gltf.constants import MODE_TRIANGLES
from compas.files.gltf.data_classes import PrimitiveData
from compas.files.gltf.gltf_mesh import GLTFMesh
from compas.files.gltf.gltf_types import GLTFConversionWarning
from compas.geometry import Geometry
from compas.geometry import Line
from compas.geometry import Pointcloud
from compas.geometry import Polyline
from compas.geometry import Transformation
from compas.scene import GeometryObject
from compas.scene import Group
from compas.scene import MeshObject
from compas.scene import Scene
from compas.scene.context import ITEM_SCENEOBJECT
from compas.scene.context import register

if TYPE_CHECKING:
    from compas.datastructures import TreeNode  # noqa: F401
    from compas.files.gltf.gltf_document import GLTFDocument
    from compas.files.gltf.gltf_node import GLTFNode
    from compas.scene import SceneObject  # noqa: F401


@contextmanager
def _base_scene_context():
    """Provide base scene objects without triggering visualization plugin discovery."""
    original = {context: registry.copy() for context, registry in ITEM_SCENEOBJECT.items()}
    register(Geometry, GeometryObject, context=None)
    register(Mesh, MeshObject, context=None)
    try:
        yield
    finally:
        ITEM_SCENEOBJECT.clear()
        for context, registry in original.items():
            ITEM_SCENEOBJECT[context].update(registry)


def _indexed_positions(
    positions: Sequence[Sequence[float]],
    indices: Optional[Sequence[int]],
) -> list[Sequence[float]]:
    indices = indices if indices is not None else range(len(positions))
    return [positions[index] for index in indices]


def gltf_points_to_pointcloud(
    positions: Sequence[Sequence[float]],
    indices: Optional[Sequence[int]] = None,
    name: Optional[str] = None,
) -> Pointcloud:
    """Convert a glTF points primitive to a COMPAS point cloud.

    Returns
    -------
    Pointcloud
        Converted point cloud.

    """
    return Pointcloud(_indexed_positions(positions, indices), name=name)


def gltf_lines_to_lines(
    positions: Sequence[Sequence[float]],
    indices: Optional[Sequence[int]] = None,
    name: Optional[str] = None,
) -> list[Line]:
    """Convert a glTF lines primitive to COMPAS lines.

    Returns
    -------
    list[Line]
        Converted independent lines.

    """
    indices = list(indices) if indices is not None else list(range(len(positions)))
    return [Line(positions[indices[index]], positions[indices[index + 1]], name=name) for index in range(0, len(indices) - 1, 2)]


def gltf_line_strip_to_polyline(
    positions: Sequence[Sequence[float]],
    indices: Optional[Sequence[int]] = None,
    name: Optional[str] = None,
) -> Polyline:
    """Convert a glTF line strip primitive to a COMPAS polyline.

    Returns
    -------
    Polyline
        Converted open polyline.

    """
    return Polyline(_indexed_positions(positions, indices), name=name)


def gltf_line_loop_to_polyline(
    positions: Sequence[Sequence[float]],
    indices: Optional[Sequence[int]] = None,
    name: Optional[str] = None,
) -> Polyline:
    """Convert a glTF line loop primitive to a closed COMPAS polyline.

    Returns
    -------
    Polyline
        Converted closed polyline.

    """
    points = _indexed_positions(positions, indices)
    if points:
        points.append(points[0])
    return Polyline(points, name=name)


def gltf_triangles_to_mesh(
    positions: Sequence[Sequence[float]],
    indices: Optional[Sequence[int]] = None,
    name: Optional[str] = None,
) -> Mesh:
    """Convert a glTF triangles primitive to a COMPAS mesh.

    Returns
    -------
    Mesh
        Converted mesh.

    """
    indices = list(indices) if indices is not None else list(range(len(positions)))
    faces = [list(indices[index : index + 3]) for index in range(0, len(indices) - 2, 3)]
    return _named_mesh(positions, faces, name)


def gltf_triangle_strip_to_mesh(
    positions: Sequence[Sequence[float]],
    indices: Optional[Sequence[int]] = None,
    name: Optional[str] = None,
) -> Mesh:
    """Convert a glTF triangle strip primitive to a COMPAS mesh.

    Returns
    -------
    Mesh
        Converted mesh with explicit triangle faces.

    """
    indices = list(indices) if indices is not None else list(range(len(positions)))
    faces = []
    for index in range(len(indices) - 2):
        a, b, c = indices[index : index + 3]
        faces.append([a, b, c] if index % 2 == 0 else [b, a, c])
    return _named_mesh(positions, faces, name)


def gltf_triangle_fan_to_mesh(
    positions: Sequence[Sequence[float]],
    indices: Optional[Sequence[int]] = None,
    name: Optional[str] = None,
) -> Mesh:
    """Convert a glTF triangle fan primitive to a COMPAS mesh.

    Returns
    -------
    Mesh
        Converted mesh with explicit triangle faces.

    """
    indices = list(indices) if indices is not None else list(range(len(positions)))
    faces = [[indices[0], indices[index], indices[index + 1]] for index in range(1, len(indices) - 1)]
    return _named_mesh(positions, faces, name)


def _named_mesh(
    positions: Sequence[Sequence[float]],
    faces: Sequence[Sequence[int]],
    name: Optional[str],
) -> Mesh:
    mesh = Mesh.from_vertices_and_faces(positions, faces)
    if name is not None:
        mesh.name = name
    return mesh


def gltf_primitive_to_compas(
    primitive: PrimitiveData,
    positions: Optional[Sequence[Sequence[float]]] = None,
    name: Optional[str] = None,
) -> list[Any]:
    """Convert a glTF primitive to the closest COMPAS geometry objects.

    The optional positions override is used for node-specific morph targets.

    Returns
    -------
    list[Mesh | Pointcloud | Polyline | Line]
        Converted geometry. Independent glTF lines produce multiple objects.

    """
    mode = MODE_TRIANGLES if primitive.mode is None else primitive.mode
    positions = positions if positions is not None else primitive.attributes["POSITION"]
    indices = primitive.indices

    if mode == MODE_POINTS:
        return [gltf_points_to_pointcloud(positions, indices, name)]
    if mode == MODE_LINES:
        return gltf_lines_to_lines(positions, indices, name)
    if mode == MODE_LINE_STRIP:
        return [gltf_line_strip_to_polyline(positions, indices, name)]
    if mode == MODE_LINE_LOOP:
        return [gltf_line_loop_to_polyline(positions, indices, name)]
    if mode == MODE_TRIANGLES:
        return [gltf_triangles_to_mesh(positions, indices, name)]
    if mode == MODE_TRIANGLE_STRIP:
        return [gltf_triangle_strip_to_mesh(positions, indices, name)]
    if mode == MODE_TRIANGLE_FAN:
        return [gltf_triangle_fan_to_mesh(positions, indices, name)]
    raise ValueError("Unsupported glTF primitive mode: {}.".format(mode))


def gltf_to_scene(
    document: "GLTFDocument",
    scene_key: Optional[int] = None,
    scene_type: type[Scene] = Scene,
) -> Scene:
    """Convert a glTF scene to a COMPAS scene.

    Parameters
    ----------
    document
        Source glTF document.
    scene_key
        Scene to convert. By default, use the document's default or first scene.
    scene_type
        COMPAS scene type to construct.

    Returns
    -------
    Scene
        COMPAS scene preserving the glTF node hierarchy and local transformations.

    """
    if not document.scenes:
        return scene_type(name="Scene")
    source_scene = document.scenes[scene_key] if scene_key is not None else document.default_or_first_scene
    scene = scene_type(name=source_scene.name or "Scene")
    objects_by_primitive: dict[tuple[int, tuple[float, ...], int], list[Any]] = {}

    def add_node(node: "GLTFNode", parent: "SceneObject | TreeNode") -> None:
        group = scene.add_group(
            name=node.name or "Node {}".format(node.key),
            parent=parent,
            transformation=Transformation(  # pyright: ignore[reportArgumentType]
                node.get_matrix_from_trs() if node.matrix is None else node.matrix
            ),
        )  # type: ignore[arg-type]
        mesh = node.mesh_data
        if mesh is not None:
            weighted_positions = node.vertices
            assert weighted_positions is not None
            offset = 0
            for primitive_index, primitive in enumerate(mesh.primitive_data_list):
                count = len(primitive.attributes["POSITION"])
                positions = weighted_positions[offset : offset + count]
                primitive_name = node.name or mesh.mesh_name
                weights = tuple(node.weights if node.weights is not None else mesh.weights or [])
                primitive_key = (mesh.key, weights, primitive_index)
                objects = objects_by_primitive.get(primitive_key)
                if objects is None:
                    objects = gltf_primitive_to_compas(primitive, positions, primitive_name)
                    objects_by_primitive[primitive_key] = objects
                for object_index, item in enumerate(objects):
                    item_name = primitive_name
                    if len(mesh.primitive_data_list) > 1:
                        item_name = "{} primitive {}".format(primitive_name or "Mesh", primitive_index)
                    if len(objects) > 1:
                        item_name = "{} line {}".format(item_name or "Lines", object_index)
                    scene.add(item, parent=group, name=item_name)  # type: ignore[arg-type]
                offset += count
        for child_key in node.children:
            add_node(document.nodes[child_key], group)

    with _base_scene_context():
        for root_key in source_scene.children:
            assert scene.root is not None
            add_node(document.nodes[root_key], scene.root)
    return scene


def mesh_to_gltf_primitive(mesh: Mesh) -> PrimitiveData:
    """Convert a COMPAS mesh to a glTF triangles primitive.

    Returns
    -------
    PrimitiveData
        Converted primitive.

    """
    vertices, faces = mesh.to_vertices_and_faces(triangulated=True)
    indices = [index for face in faces for index in face]
    primitive = PrimitiveData({"POSITION": vertices}, indices, mode=MODE_TRIANGLES)
    texture_coordinates = mesh.vertices_attribute("texture_coordinate")
    vertex_normals = mesh.vertices_attribute("vertex_normal")
    vertex_colors = mesh.vertices_attribute("vertex_color")
    if texture_coordinates and texture_coordinates[0] is not None:
        primitive.attributes["TEXCOORD_0"] = texture_coordinates
    if vertex_normals and vertex_normals[0] is not None:
        primitive.attributes["NORMAL"] = vertex_normals
    if vertex_colors and vertex_colors[0] is not None:
        primitive.attributes["COLOR_0"] = vertex_colors
    return primitive


def pointcloud_to_gltf_primitive(pointcloud: Pointcloud) -> PrimitiveData:
    """Convert a COMPAS point cloud to a glTF points primitive.

    Returns
    -------
    PrimitiveData
        Converted primitive.

    """
    positions = [list(point) for point in pointcloud.points]
    return PrimitiveData({"POSITION": positions}, list(range(len(positions))), mode=MODE_POINTS)


def lines_to_gltf_primitive(lines: Sequence[Line]) -> PrimitiveData:
    """Convert COMPAS lines to a glTF independent-lines primitive.

    Returns
    -------
    PrimitiveData
        Converted primitive.

    """
    positions = [list(point) for line in lines for point in (line.start, line.end)]
    return PrimitiveData({"POSITION": positions}, list(range(len(positions))), mode=MODE_LINES)


def line_to_gltf_primitive(line: Line) -> PrimitiveData:
    """Convert a COMPAS line to a glTF independent-lines primitive.

    Returns
    -------
    PrimitiveData
        Converted primitive.

    """
    return lines_to_gltf_primitive([line])


def polyline_to_gltf_primitive(polyline: Polyline) -> PrimitiveData:
    """Convert a COMPAS polyline to a glTF line strip or line loop primitive.

    Returns
    -------
    PrimitiveData
        Converted primitive.

    """
    positions = [list(point) for point in polyline.points]
    closed = len(positions) > 2 and positions[0] == positions[-1]
    if closed:
        positions.pop()
    mode = MODE_LINE_LOOP if closed else MODE_LINE_STRIP
    return PrimitiveData({"POSITION": positions}, list(range(len(positions))), mode=mode)


def compas_to_gltf_primitive(item: Any) -> Optional[PrimitiveData]:
    """Convert supported COMPAS geometry to a glTF primitive.

    Returns
    -------
    PrimitiveData | None
        Converted primitive, or `None` if the item is unsupported.

    """
    if isinstance(item, Mesh):
        return mesh_to_gltf_primitive(item)
    if isinstance(item, Pointcloud):
        return pointcloud_to_gltf_primitive(item)
    if isinstance(item, Line):
        return line_to_gltf_primitive(item)
    if isinstance(item, Polyline):
        return polyline_to_gltf_primitive(item)
    return None


def _geometry_mesh(document: "GLTFDocument", item: Any) -> Optional[GLTFMesh]:
    primitive = compas_to_gltf_primitive(item)
    if primitive is None:
        return None
    return GLTFMesh([primitive], document, mesh_name=item.name)


def scene_to_gltf(scene: Scene) -> "GLTFDocument":
    """Convert a COMPAS scene to a glTF document.

    Unsupported scene items are omitted with a `GLTFConversionWarning`. Their
    scene nodes and descendants are preserved.

    Parameters
    ----------
    scene
        Source COMPAS scene.

    Returns
    -------
    GLTFDocument
        Converted glTF document.

    """
    from compas.files.gltf.gltf_document import GLTFDocument

    document = GLTFDocument()
    target_scene = document.add_scene(name=scene.name)
    document.default_scene_key = target_scene.key
    mesh_by_item_id: dict[int, int] = {}

    def add_object(sceneobject: "SceneObject", parent: "Optional[GLTFNode]" = None) -> None:
        if parent is None:
            node = target_scene.add_child(node_name=sceneobject.name)
        else:
            node = parent.add_child(child_name=sceneobject.name)
        if sceneobject.transformation is not None:
            node.matrix = [list(row) for row in sceneobject.transformation.matrix]

        if not isinstance(sceneobject, Group):
            mesh_key = mesh_by_item_id.get(id(sceneobject.item))
            mesh_data = document.meshes[mesh_key] if mesh_key is not None else _geometry_mesh(document, sceneobject.item)
            if mesh_data is None:
                warnings.warn(
                    "Scene object {!r} contains unsupported item type {} and was omitted from glTF geometry.".format(
                        sceneobject.name, type(sceneobject.item).__name__
                    ),
                    GLTFConversionWarning,
                    stacklevel=2,
                )
            else:
                mesh_by_item_id[id(sceneobject.item)] = mesh_data.key
                node.mesh_key = mesh_data.key
        for child in sceneobject.children:
            add_object(cast("SceneObject", child), node)

    assert scene.root is not None
    for child in scene.root.children:
        add_object(cast("SceneObject", child))
    return document
