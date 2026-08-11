"""Convenience functions for reading and writing OBJ data."""

from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Iterable
from typing import Optional

import compas
from compas.tolerance import TOL

from .obj_document import OBJDocument
from .obj_document import OBJElementReference
from .obj_document import OBJFace
from .obj_document import OBJObject
from .obj_document import OBJVertexReference
from .obj_parser import OBJParser
from .obj_reader import OBJReader
from .obj_reader import OBJSource
from .obj_writer import OBJTarget
from .obj_writer import OBJWriter

if TYPE_CHECKING:
    from compas.datastructures import Mesh


@dataclass
class OBJData:
    """Geometric projection of an OBJ document.

    The projection preserves every declared vertex and converts element
    references to plain vertex indices.

    """

    vertices: list[list[float]]
    points: list[int]
    lines: list[list[int]]
    polylines: list[list[int]]
    faces: list[list[int]]
    objects: dict[str, tuple[dict[int, list[float]], list[list[int]]]]
    groups: dict[str, list[tuple[str, int]]]


def read_obj(source: OBJSource, encoding: str = "utf-8") -> OBJDocument:
    """Read an OBJ source into an OBJ document.

    Parameters
    ----------
    source
        Path, URL, text stream, or binary stream containing OBJ data.
    encoding
        Encoding used for text streams and source decoding.

    Returns
    -------
    OBJDocument
        Parsed OBJ document.

    """
    data = OBJReader(source, encoding=encoding).read()
    return OBJParser(data, encoding=encoding).parse()


def obj_data(document: OBJDocument) -> OBJData:
    """Project an OBJ document to geometric data.

    Parameters
    ----------
    document
        Parsed OBJ document.
    Returns
    -------
    OBJData
        Geometric data with plain vertex indices.

    """
    index_index = {index: index for index in range(len(document.vertices))}
    return _project_obj_data(document, list(document.vertices), index_index)


def weld_obj_data(document: OBJDocument, precision: Optional[int] = None) -> OBJData:
    """Project an OBJ document to explicitly welded geometric data.

    Parameters
    ----------
    document
        Parsed OBJ document.
    precision
        Precision used to identify coincident vertices.

    Returns
    -------
    OBJData
        Welded geometric data with plain vertex indices.

    """
    index_key = OrderedDict(
        (index, TOL.geometric_key(xyz, precision)) for index, xyz in enumerate(document.vertices)
    )
    vertex = OrderedDict((key, document.vertices[index]) for index, key in index_key.items())
    vertex_index = {key: index for index, key in enumerate(vertex)}
    index_index = {index: vertex_index[key] for index, key in index_key.items()}
    return _project_obj_data(document, list(vertex.values()), index_index)


def read_obj_meshes(
    source: OBJSource,
    weld: bool = False,
    precision: Optional[int] = None,
) -> list["Mesh"]:
    """Read all polygon meshes from an OBJ source.

    Parameters
    ----------
    source
        Path, URL, text stream, or binary stream containing OBJ data.
    weld
        If True, explicitly weld coincident vertices before constructing the meshes.
    precision
        Precision used when welding vertices.

    Returns
    -------
    list[Mesh]
        Meshes corresponding to the named OBJ objects. Files without named
        objects produce one mesh.

    """
    from compas.datastructures import Mesh

    document = read_obj(source)
    data = weld_obj_data(document, precision) if weld else obj_data(document)
    meshes = []
    claimed_faces = set()

    for name, obj in document.objects.items():
        face_indices = [reference.index for reference in obj.elements if reference.kind == "face"]
        if not face_indices:
            continue
        claimed_faces.update(face_indices)
        mesh = _mesh_from_obj_faces(Mesh, data, face_indices)
        mesh.name = name
        meshes.append(mesh)

    remaining = [index for index in range(len(data.faces)) if index not in claimed_faces]
    if remaining:
        meshes.insert(0, _mesh_from_obj_faces(Mesh, data, remaining))

    return meshes


def _mesh_from_obj_faces(mesh_type: Any, data: OBJData, face_indices: Iterable[int]) -> "Mesh":
    vertex_index = {}
    vertices = []
    faces = []
    for face_index in face_indices:
        face = []
        for vertex in data.faces[face_index]:
            if vertex not in vertex_index:
                vertex_index[vertex] = len(vertices)
                vertices.append(data.vertices[vertex])
            face.append(vertex_index[vertex])
        faces.append(face)
    return mesh_type.from_vertices_and_faces(vertices, faces)


def _project_obj_data(
    document: OBJDocument,
    vertices: list[list[float]],
    index_index: dict[int, int],
) -> OBJData:
    points = [index_index[reference.vertex] for point in document.points for reference in point.vertices]
    elements = [[index_index[reference.vertex] for reference in line.vertices] for line in document.lines]
    lines = [line for line in elements if len(line) == 2]
    polylines = [line for line in elements if len(line) > 2]
    faces = [[index_index[reference.vertex] for reference in face.vertices] for face in document.faces]
    groups = {
        name: [(reference.kind[0], reference.index) for reference in group.elements]
        for name, group in document.groups.items()
    }
    objects = {}
    for name, obj in document.objects.items():
        object_faces = [faces[reference.index] for reference in obj.elements if reference.kind == "face"]
        object_vertices = {index: vertices[index] for face in object_faces for index in face}
        objects[name] = object_vertices, object_faces

    return OBJData(vertices, points, lines, polylines, faces, objects, groups)


def write_obj(
    target: OBJTarget,
    data: Any,
    precision: Optional[int] = None,
    unweld: bool = False,
    author: Optional[str] = None,
    email: Optional[str] = None,
    date: Optional[str] = None,
) -> None:
    """Write an OBJ document, mesh, or collection of meshes.

    Parameters
    ----------
    target
        Path or writable text or binary stream.
    data
        OBJ document, mesh, or collection of meshes to write.
    precision
        Number of digits after the decimal point.
    unweld
        If True, write unique vertices for every mesh face.
    author
        Author name to include in the mesh compatibility header.
    email
        Author email to include in the mesh compatibility header.
    date
        Date to include in the mesh compatibility header.

    Returns
    -------
    None

    """
    precision = TOL.precision if precision is None else precision
    if isinstance(data, OBJDocument):
        document = deepcopy(data)
    else:
        meshes = list(data) if isinstance(data, (list, tuple)) else [data]
        document = _document_from_meshes(meshes, unweld=unweld)
        document.comments.extend(
            [
                "OBJ",
                "COMPAS",
                f"version: {compas.__version__}",
                f"precision: {precision}",
                "V F E: {} {} {}".format(
                    sum(mesh.number_of_vertices() for mesh in meshes),
                    sum(mesh.number_of_faces() for mesh in meshes),
                    sum(mesh.number_of_edges() for mesh in meshes),
                ),
            ]
        )
    if author:
        document.comments.append(f"author: {author}")
    if email:
        document.comments.append(f"email: {email}")
    if date:
        document.comments.append(f"date: {date}")
    OBJWriter(target, precision=precision).write(document)


def _document_from_meshes(meshes: Iterable[Any], unweld: bool = False) -> OBJDocument:
    document = OBJDocument()
    for index, mesh in enumerate(meshes):
        name = mesh.name if mesh.name != "Mesh" else f"Mesh {index}"
        obj = document.objects.setdefault(name, OBJObject(name))

        if unweld:
            for face in mesh.faces():
                references = []
                for vertex in mesh.face_vertices(face):
                    document.vertices.append(mesh.vertex_coordinates(vertex))
                    document.vertex_weights.append(1.0)
                    references.append(OBJVertexReference(len(document.vertices) - 1))
                document.faces.append(OBJFace(references))
                reference = OBJElementReference("face", len(document.faces) - 1)
                document.elements.append(reference)
                obj.elements.append(reference)
            continue

        offset = len(document.vertices)
        vertex_index = mesh.vertex_index()
        document.vertices.extend(mesh.vertex_coordinates(vertex) for vertex in mesh.vertices())
        document.vertex_weights.extend([1.0] * mesh.number_of_vertices())
        for face in mesh.faces():
            references = [OBJVertexReference(offset + vertex_index[vertex]) for vertex in mesh.face_vertices(face)]
            document.faces.append(OBJFace(references))
            reference = OBJElementReference("face", len(document.faces) - 1)
            document.elements.append(reference)
            obj.elements.append(reference)
    return document
