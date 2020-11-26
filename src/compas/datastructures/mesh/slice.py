from compas.geometry import intersection_segment_plane
from compas.geometry import length_vector
from compas.geometry import subtract_vectors
from compas.geometry import dot_vectors


__all__ = ['mesh_slice_plane']


def mesh_slice_plane(mesh, plane):
    """Slice a mesh with a plane and construct the resulting submeshes.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The original mesh.
    plane : compas.geometry.Plane
        The cutting plane.

    Returns
    -------
    None or tuple of :class:`compas.datastructures.Mesh`
        If the mesh and plane do not intersect,
        or if the intersection is degenerate (point or line),
        the function returns ``None``.
        Otherwise, the "positive" and "negative" submeshes are returned.

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


class IntersectionMeshPlane(object):

    def __init__(self, mesh, plane):
        self.mesh = mesh
        self.plane = plane
        self._intersections = []
        self.intersect()

    @property
    def meshtype(self):
        return type(self.mesh)

    @property
    def intersections(self):
        return self._intersections

    @property
    def is_none(self):
        return len(self.intersections) == 0

    @property
    def is_point(self):
        return len(self.intersections) == 1

    @property
    def is_line(self):
        return len(self.intersections) == 2

    @property
    def is_polygon(self):
        return len(self.intersections) >= 3

    @property
    def positive(self):
        if self.is_none:
            return
        vertices = []
        for key in self.mesh.vertices():
            if self.is_positive(key):
                vertices.append(key)
        faces = []
        for key in vertices:
            faces += self.mesh.vertex_faces(key)
        faces = list(set(faces))
        vdict = {key: self.mesh.vertex_coordinates(key) for key in vertices + self.intersections}
        fdict = [self.mesh.face_vertices(fkey) for fkey in faces]
        mesh = self.meshtype.from_vertices_and_faces(vdict, fdict)
        mesh.add_face(mesh.vertices_on_boundary(True))
        return mesh

    def is_positive(self, key):
        o = self.plane.point
        n = self.plane.normal
        if key not in self.intersections:
            a = self.mesh.vertex_attributes(key, 'xyz')
            oa = subtract_vectors(a, o)
            similarity = dot_vectors(n, oa)
            if similarity > 0.0:
                return True
        return False

    @property
    def negative(self):
        if self.is_none:
            return
        vertices = []
        for key in self.mesh.vertices():
            if self.is_negative(key):
                vertices.append(key)
        faces = []
        for key in vertices:
            faces += self.mesh.vertex_faces(key)
        faces = list(set(faces))
        vdict = {key: self.mesh.vertex_coordinates(key) for key in vertices + self.intersections}
        fdict = [self.mesh.face_vertices(fkey) for fkey in faces]
        mesh = self.meshtype.from_vertices_and_faces(vdict, fdict)
        mesh.add_face(mesh.vertices_on_boundary(True))
        return mesh

    def is_negative(self, key):
        o = self.plane.point
        n = self.plane.normal
        if key in self.intersections:
            return False
        a = self.mesh.vertex_attributes(key, 'xyz')
        oa = subtract_vectors(a, o)
        similarity = dot_vectors(n, oa)
        return similarity < 0.0

    def intersect(self):
        intersections = []
        for u, v in list(self.mesh.edges()):
            a = self.mesh.vertex_attributes(u, 'xyz')
            b = self.mesh.vertex_attributes(v, 'xyz')
            x = intersection_segment_plane((a, b), self.plane)
            if not x:
                continue
            L_ax = length_vector(subtract_vectors(x, a))
            L_ab = length_vector(subtract_vectors(b, a))
            t = L_ax / L_ab
            key = self.mesh.split_edge(u, v, t=t, allow_boundary=True)
            intersections.append(key)
        self._intersections = intersections

    def split(self):
        for fkey in list(self.mesh.faces()):
            split = [key for key in self.mesh.face_vertices(fkey) if key in self.intersections]
            if len(split) == 2:
                u, v = split
                self.mesh.split_face(fkey, u, v)
        return self.positive, self.negative


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    doctest.testmod(globs=globals())
