from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures.volmesh.core.halfface import HalfFace
from compas.datastructures import Mesh

from compas.files import OBJ

from compas.geometry import add_vectors
from compas.geometry import bestfit_plane
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import centroid_polyhedron
from compas.geometry import distance_point_point
from compas.geometry import length_vector
from compas.geometry import normal_polygon
from compas.geometry import normalize_vector
from compas.geometry import project_point_plane
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors

from compas.utilities import geometric_key


__all__ = ['BaseVolMesh']


class BaseVolMesh(HalfFace):
    """Geometric implementation of a face data structure for volumetric meshes.

    Attributes
    ----------
    attributes : dict
        A dictionary of general volmesh attributes.

        * ``'name': "VolMesh"``

    default_vertex_attributes : dict
        The names of pre-assigned vertex attributes and their default values.

        * ``'x': 0.0``
        * ``'y': 0.0``
        * ``'z': 0.0``

    default_edge_attributes : dict
        The default data attributes assigned to every new edge.
    default_face_attributes : dict
        The default data attributes assigned to every new face.
    name : str
        The name of the volmesh.
        Shorthand for ``volmesh.attributes['name']``

    data : dict
        The data representing the mesh.
        The dict has the following structure:

        * 'attributes'   => dict
        * 'dva'          => dict
        * 'dea'          => dict
        * 'dfa'          => dict
        * 'dca'          => dict
        * 'vertex'       => dict
        * 'halface'      => dict
        * 'cell'         => dict
        * 'plane'        => dict
        * 'edgedata'     => dict
        * 'facedata'     => dict
        * 'celldata'     => dict
        * 'max_int_key'  => int
        * 'max_int_hfkey' => int
        * 'max_int_ckey' => int

    """

    def __init__(self):
        super(BaseVolMesh, self).__init__()
        self.attributes.update({'name': 'VolMesh'})
        self.default_vertex_attributes.update({'x': 0.0, 'y': 0.0, 'z': 0.0})

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # from/to
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath, precision=None):
        """Construct a volmesh object from the data described in an OBJ file.

        Parameters
        ----------
        filepath : str
            The path to the file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Volesh
            A volmesh object.
        """
        obj = OBJ(filepath, precision)
        vertices = obj.parser.vertices
        faces = obj.parser.faces
        groups = obj.parser.groups
        cells = []
        for name in groups:
            group = groups[name]
            cell = []
            for item in group:
                if item[0] != 'f':
                    continue
                face = faces[item[1]]
                cell.append(face)
            cells.append(cell)
        return cls.from_vertices_and_cells(vertices, cells)

    def to_obj(self, filepath, precision=None, **kwargs):
        """Write the volmesh to an OBJ file.

        Parameters
        ----------
        filepath : str
            Full path of the file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.
        unweld : bool, optional
            If true, all faces have their own unique vertices.
            If false, vertices are shared between faces if this is also the case in the mesh.
            Default is ``False``.

        Warnings
        --------
        This function only writes geometric data about the vertices and
        the faces to the file.
        """
        obj = OBJ(filepath, precision=precision)
        obj.write(self, **kwargs)

    @classmethod
    def from_vertices_and_cells(cls, vertices, cells):
        """Construct a volmesh object from vertices and cells.

        Parameters
        ----------
        vertices : list
            Ordered list of vertices, represented by their XYZ coordinates.
        cells : lists of lists
            List of cells (list of faces).

        Returns
        -------
        Volmesh
            A volmesh object.
        """
        volmesh = cls()
        for x, y, z in vertices:
            volmesh.add_vertex(x=x, y=y, z=z)
        for cell in cells:
            volmesh.add_cell(cell)
        return volmesh

    def to_vertices_and_cells(self):
        """Return the vertices and cells of a volmesh.

        Returns
        -------
        tuple
            A 2-tuple containing

            * a list of vertices, represented by their XYZ coordinates, and
            * a list of cells.

            Each cell is a list of faces, which are lists of indices referencing the list of vertex coordinates.
        """
        vertex_index = self.vertex_index()
        vertices = [self.vertex_coordinates(vertex) for vertex in self.vertices()]
        cells = []
        for cell in self.cell:
            faces = [[vertex_index[vertex] for vertex in self.halfface_vertices(face)] for face in self.cell_faces(cell)]
            cells.append(faces)
        return vertices, cells

    def cell_to_mesh(self, cell):
        """Construct a mesh object from from a cell of a volmesh.

        Parameters
        ----------
        cell : hashable
            Identifier of the cell.

        Returns
        -------
        Mesh
            A mesh object.
        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return Mesh.from_vertices_and_faces(vertices, faces)

    def cell_to_vertices_and_faces(self, cell):
        """Return the vertices and faces of a cell.

        Parameters
        ----------
        cell : hashable
            Identifier of the cell.

        Returns
        -------
        tuple
            A 2-tuple containing

            * a list of vertices, represented by their XYZ coordinates, and
            * a list of faces.

            Each face is a list of indices referencing the list of vertex coordinates.
        """
        vertices = self.cell_vertices(cell)
        faces = self.cell_faces(cell)
        vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))
        vertices = [self.vertex_coordinates(vertex) for vertex in vertices]
        faces = [[vertex_index[vertex] for vertex in self.halfface_vertices(face)] for face in faces]
        return vertices, faces

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def vertex_gkey(self, precision=None):
        """Returns a dictionary that maps vertex dictionary keys to the corresponding
        *geometric key* up to a certain precision.

        Parameters
        ----------
        precision : str (3f)
            The float precision specifier used in string formatting.

        Returns
        -------
        dict
            A dictionary of vertex-geometric key pairs.

        """
        gkey = geometric_key
        xyz = self.vertex_coordinates
        return {vertex: gkey(xyz(vertex), precision) for vertex in self.vertices()}

    def gkey_vertex(self, precision=None):
        """Returns a dictionary that maps *geometric keys* of a certain precision
        to the keys of the corresponding vertices.

        Parameters
        ----------
        precision : str (3f)
            The float precision specifier used in string formatting.

        Returns
        -------
        dict
            A dictionary of geometric key-vertex pairs.

        """
        gkey = geometric_key
        xyz = self.vertex_coordinates
        return {gkey(xyz(vertex), precision): vertex for vertex in self.vertices()}

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # volmesh geometry
    # --------------------------------------------------------------------------

    def centroid(self):
        """Compute the centroid of the volmesh.

        Returns
        -------
        list
            The coordinates of the centroid.

        """
        return centroid_points([self.vertex_coordinates(vertex) for vertex in self.vertices()])

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, vertex, axes='xyz'):
        """Return the coordinates of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of ``'x'``, ``'y'``, ``'z'``.
            Default is ``'xyz'``.

        Returns
        -------
        list
            Coordinates of the vertex.

        """
        return [self._vertex[vertex][axis] for axis in axes]

    def vertex_laplacian(self, vertex):
        """Compute the vector from a vertex to the centroid of its neighbors.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list
            The components of the vector.
        """
        c = self.vertex_neighborhood_centroid(vertex)
        p = self.vertex_coordinates(vertex)
        return subtract_vectors(c, p)

    def vertex_neighborhood_centroid(self, vertex):
        """Compute the centroid of the neighbors of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list
            The coordinates of the centroid.
        """
        return centroid_points([self.vertex_coordinates(nbr) for nbr in self.vertex_neighbors(vertex)])

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    def edge_coordinates(self, edge, axes='xyz'):
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        edge : tuple of int
            The edge identifier.
        axes : str (xyz)
            The axes along which the coordinates should be included.

        Returns
        -------
        tuple
            The coordinates of the start point and the coordinates of the end point.

        """
        u, v = edge
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    def edge_length(self, edge):
        """Return the length of an edge.

        Parameters
        ----------
        edge : tuple of int
            The edge identifier.

        Returns
        -------
        float
            The length of the edge.

        """
        a, b = self.edge_coordinates(edge)
        return distance_point_point(a, b)

    def edge_vector(self, edge):
        """Return the vector of an edge.

        Parameters
        ----------
        edge : tuple of int
            The edge identifier.

        Returns
        -------
        list
            The vector from u to v.

        """
        a, b = self.edge_coordinates(edge)
        ab = subtract_vectors(b, a)
        return ab

    def edge_point(self, edge, t=0.5):
        """Return the location of a point along an edge.

        Parameters
        ----------
        edge : tuple of int
            The edge identifier.
        t : float (0.5)
            The location of the point on the edge.
            If the value of ``t`` is outside the range ``0-1``, the point will
            lie in the direction of the edge, but not on the edge vector.

        Returns
        -------
        list
            The XYZ coordinates of the point.

        """
        a, b = self.edge_coordinates(edge)
        ab = subtract_vectors(b, a)
        return add_vectors(a, scale_vector(ab, t))

    def edge_direction(self, edge):
        """Return the direction vector of an edge.

        Parameters
        ----------
        edge : tuple of int
            The edge identifier.

        Returns
        -------
        list
            The direction vector of the edge.

        """
        return normalize_vector(self.edge_vector(edge))

    # --------------------------------------------------------------------------
    # face geometry
    # --------------------------------------------------------------------------

    def face_vertices(self, face):
        """The vertices of a face.

        Parameters
        ----------
        halfface : int
            The identifier of the face.

        Returns
        -------
        list
            Ordered vertex identifiers.
        """
        return self.halfface_vertices(face)

    def face_coordinates(self, face):
        """Compute the coordinates of the vertices of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of ``'x'``, ``'y'``, ``'z'``.
            Default is ``'xyz'``.

        Returns
        -------
        list of list
            The coordinates of the vertices of the face.

        """
        return [self.vertex_coordinates(vertex) for vertex in self.face_vertices(face)]

    def face_normal(self, face, unitized=True):
        """Compute the oriented normal of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.
        unitized : bool, optional
            Unitize the normal vector.
            Default is ``True``.

        Returns
        -------
        list
            The components of the normal vector.

        """
        return normal_polygon(self.face_coordinates(face), unitized=unitized)

    def face_centroid(self, face):
        """Compute the location of the centroid of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list
            The coordinates of the centroid.

        """
        return centroid_points(self.face_coordinates(face))

    def face_center(self, face):
        """Compute the location of the center of mass of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list
            The coordinates of the center of mass.

        """
        return centroid_polygon(self.face_coordinates(face))

    def face_area(self, face):
        """Compute the oriented area of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        float
            The non-oriented area of the face.

        """
        return length_vector(self.face_normal(face, unitized=False))

    def face_flatness(self, face, maxdev=0.02):
        """Compute the flatness of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        float
            The flatness.

        Note
        ----
        compas.geometry.mesh_flatness function currently only works for quadrilateral faces.
        This function uses the distance between each face vertex and its projected point on the best-fit plane of the face as the flatness metric.

        """
        deviation = 0
        polygon = self.face_coordinates(face)
        plane = bestfit_plane(polygon)
        for pt in polygon:
            pt_proj = project_point_plane(pt, plane)
            dev = distance_point_point(pt, pt_proj)
            if dev > deviation:
                deviation = dev
        return deviation

    def face_aspect_ratio(self, face):
        """Face aspect ratio as the ratio between the lengths of the maximum and minimum face edges.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        float
            The aspect ratio.

        References
        ----------
        .. [1] Wikipedia. *Types of mesh*.
               Available at: https://en.wikipedia.org/wiki/Types_of_mesh.
        """
        face_edge_lengths = [self.edge_length(edge) for edge in self.face_halfedges(face)]
        return max(face_edge_lengths) / min(face_edge_lengths)

    halfface_area = face_area
    halfface_centroid = face_centroid
    halfface_center = face_center
    halfface_coordinates = face_coordinates
    halfface_flatness = face_flatness
    halfface_normal = face_normal
    halfface_aspect_ratio = face_aspect_ratio

    # --------------------------------------------------------------------------
    # cell geometry
    # --------------------------------------------------------------------------

    def cell_centroid(self, cell):
        """Compute the location of the centroid of a cell.

        Parameters
        ----------
        cell : hashable
            The identifier of the cell.

        Returns
        -------
        list
            The coordinates of the centroid.
        """
        vertices = self.cell_vertices(cell)
        return centroid_points([self.vertex_coordinates(vertex) for vertex in vertices])

    def cell_center(self, cell):
        """Compute the location of the center of mass of a cell.

        Parameters
        ----------
        cell : hashable
            The identifier of the cell.

        Returns
        -------
        list
            The coordinates of the center of mass.
        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return centroid_polyhedron((vertices, faces))

    def cell_vertex_normal(self, cell, vertex):
        """Return the normal vector at the vertex of a boundary cell as the weighted average of the
        normals of the neighboring faces.

        Parameters
        ----------
        cell : int
            The identifier of the vertex of the cell.
        vertex : int
            The identifier of the vertex of the cell.

        Returns
        -------
        list
            The components of the normal vector.
        """
        cell_faces = self.cell_faces(cell)
        vectors = [self.face_normal(face) for face in self.vertex_faces(vertex) if face in cell_faces]
        return normalize_vector(centroid_points(vectors))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
