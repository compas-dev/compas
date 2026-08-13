from typing import TYPE_CHECKING
from typing import Generic
from typing import Optional
from typing import Type
from typing import TypeVar

from compas.geometry import Plane
from compas.geometry import intersection_segment_plane
from compas.linalg.vectors import dot_vectors
from compas.linalg.vectors import length_vector
from compas.linalg.vectors import subtract_vectors

from .types import Vertex

if TYPE_CHECKING:
    from .mesh import Mesh

MeshType = TypeVar("MeshType", bound="Mesh")


def mesh_slice_plane(mesh: MeshType, plane: Plane) -> Optional[tuple[MeshType, MeshType]]:
    """Slice a mesh with a plane and construct the resulting submeshes.

    Parameters
    ----------
    mesh
        The original mesh.
    plane
        The cutting plane.

    Returns
    -------
    tuple[Mesh, Mesh] | None
        The "positive" and "negative" submeshes.
        If the mesh and plane do not intersect,
        or if the intersection is degenerate (point or line),
        the function returns None.

    Raises
    ------
    RuntimeError
        If an intersected mesh edge cannot be split.

    Notes
    -----
    The current implementation assumes that the input mesh represents a closed
    volume. This condition is not checked.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Box
    >>> from compas.datastructures import Mesh
    >>> plane = Plane((0, 0, 0), (1, 0, 0))
    >>> box = Box.from_width_height_depth(1, 1, 1)
    >>> mesh = Mesh.from_shape(box)
    >>> result = mesh_slice_plane(mesh, plane)
    >>> len(result) == 2
    True

    """
    intersection = IntersectionMeshPlane(mesh, plane)
    if not intersection.is_polygon:
        return None
    return intersection.split()


class IntersectionMeshPlane(Generic[MeshType]):
    def __init__(self, mesh: MeshType, plane: Plane):
        self.mesh = mesh
        self.plane = plane
        self._intersections: list[Vertex] = []
        self.intersect()

    @property
    def meshtype(self) -> Type[MeshType]:
        return type(self.mesh)

    @property
    def intersections(self) -> list[Vertex]:
        return self._intersections

    @property
    def is_none(self) -> bool:
        return len(self.intersections) == 0

    @property
    def is_point(self) -> bool:
        return len(self.intersections) == 1

    @property
    def is_line(self) -> bool:
        return len(self.intersections) == 2

    @property
    def is_polygon(self) -> bool:
        return len(self.intersections) >= 3

    @property
    def is_mesh_closed(self) -> bool:
        return self.mesh.is_closed()

    @property
    def positive(self) -> Optional[MeshType]:
        if self.is_none:
            return
        vertices = []
        for key in self.mesh.vertices():
            if self.is_positive(key):
                vertices.append(key)
        faces = []
        for key in vertices:
            faces.extend(self.mesh.vertex_faces(key))
        faces = set(faces)
        vdict = {key: self.mesh.vertex_coordinates(key) for key in vertices + self.intersections}
        fdict = [self.mesh.face_vertices(fkey) for fkey in faces]
        mesh = self.meshtype.from_vertices_and_faces(vdict, fdict)
        if self.is_mesh_closed:
            mesh.add_face(mesh.vertices_on_boundary())
        return mesh

    def is_positive(self, key: Vertex) -> bool:
        o = self.plane.point
        n = self.plane.normal
        if key not in self.intersections:
            a = self.mesh.vertex_attributes(key, "xyz")
            oa = subtract_vectors(a, o)
            similarity = dot_vectors(n, oa)
            if similarity > 0.0:
                return True
        return False

    @property
    def negative(self) -> Optional[MeshType]:
        if self.is_none:
            return
        vertices = []
        for key in self.mesh.vertices():
            if self.is_negative(key):
                vertices.append(key)
        faces = []
        for key in vertices:
            faces.extend(self.mesh.vertex_faces(key))
        faces = set(faces)
        vdict = {key: self.mesh.vertex_coordinates(key) for key in vertices + self.intersections}
        fdict = [self.mesh.face_vertices(fkey) for fkey in faces]
        mesh = self.meshtype.from_vertices_and_faces(vdict, fdict)
        if self.is_mesh_closed:
            mesh.add_face(mesh.vertices_on_boundary())
        return mesh

    def is_negative(self, key: Vertex) -> bool:
        o = self.plane.point
        n = self.plane.normal
        if key in self.intersections:
            return False
        a = self.mesh.vertex_attributes(key, "xyz")
        oa = subtract_vectors(a, o)
        similarity = dot_vectors(n, oa)
        return similarity < 0.0

    def intersect(self) -> None:
        intersections: list[Vertex] = []
        vertex_intersections: list[Vertex] = []
        for u, v in list(self.mesh.edges()):
            a = self.mesh.vertex_attributes(u, "xyz")
            b = self.mesh.vertex_attributes(v, "xyz")
            x = intersection_segment_plane((a, b), self.plane)
            if not x:
                continue
            if any([i != j for i, j in zip(x, a)]) and any([i != j for i, j in zip(x, b)]):
                L_ax = length_vector(subtract_vectors(x, a))
                L_ab = length_vector(subtract_vectors(b, a))
                t = L_ax / L_ab
                key = self.mesh.split_edge((u, v), t=t, allow_boundary=True)
                if key is None:
                    raise RuntimeError("Splitting an intersected edge failed.")
                intersections.append(key)
            else:
                if u in vertex_intersections:
                    intersections.append(u)
                vertex_intersections.clear()
                vertex_intersections.append(u)
                vertex_intersections.append(v)
        self._intersections = intersections

    def split(self) -> tuple[MeshType, MeshType]:
        for fkey in list(self.mesh.faces()):
            split = [key for key in self.mesh.face_vertices(fkey) if key in self.intersections]
            if len(split) == 2:
                u, v = split
                try:
                    self.mesh.split_face(fkey, u, v)
                except ValueError:
                    continue
        positive = self.positive
        negative = self.negative
        if positive is None or negative is None:
            raise RuntimeError("Splitting the mesh did not produce two submeshes.")
        return positive, negative
