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
    """Geometric implementation of a halfface data structure for volumetric meshes.


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
        * 'max_int_fkey' => int
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
        obj      = OBJ(filepath, precision)
        vertices = obj.parser.vertices
        faces    = obj.parser.faces
        groups   = obj.parser.groups
        cells    = []
        for name in groups:
            group = groups[name]
            cell  = []
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
            List of cells (list of halffaces).

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

            Each cell is a list of halffaces, which are lists of indices referencing the list of vertex coordinates.

        """
        key_index = self.key_index()
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        cells = []
        for ckey in self.cell:
            halffaces = [[key_index[key] for key in self.halfface[fkey]] for fkey in self.halffaces()]
            cells.append(halffaces)
        return vertices, cells

    def cell_to_mesh(self, ckey):
        """Construct a mesh object from from a cell of a volmesh.

        Parameters
        ----------
        hfkey : hashable
            Identifier of the cell.

        Returns
        -------
        Mesh
            A mesh object.

        """
        vertices, halffaces = self.cell_to_vertices_and_halffaces(ckey)
        return Mesh.from_vertices_and_faces(vertices, halffaces)

    def cell_to_vertices_and_halffaces(self, ckey):
        """Return the vertices and halffaces of a cell.

        Returns
        -------
        tuple
            A 2-tuple containing

            * a list of vertices, represented by their XYZ coordinates, and
            * a list of halffaces.

            Each halfface is a list of indices referencing the list of vertex coordinates.

        """
        vkeys       = self.cell_vertices(ckey)
        hfkeys      = self.cell_halffaces(ckey)
        vkey_vindex = dict((vkey, index) for index, vkey in enumerate(vkeys))
        vertices    = [self.vertex_coordinates(vkey) for vkey in vkeys]
        halffaces   = [[vkey_vindex[vkey] for vkey in self.halfface[fkey]] for fkey in hfkeys]
        return vertices, halffaces

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def key_gkey(self, precision=None):
        """Returns a dictionary that maps vertex dictionary keys to the corresponding
        *geometric key* up to a certain precision.

        Parameters
        ----------
        precision : str (3f)
            The float precision specifier used in string formatting.

        Returns
        -------
        dict
            A dictionary of key-geometric key pairs.

        """
        gkey = geometric_key
        xyz = self.vertex_coordinates
        return {key: gkey(xyz(key), precision) for key in self.vertices()}

    def gkey_key(self, precision=None):
        """Returns a dictionary that maps *geometric keys* of a certain precision
        to the keys of the corresponding vertices.

        Parameters
        ----------
        precision : str (3f)
            The float precision specifier used in string formatting.

        Returns
        -------
        dict
            A dictionary of geometric key-key pairs.

        """
        gkey = geometric_key
        xyz = self.vertex_coordinates
        return {gkey(xyz(key), precision): key for key in self.vertices()}

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

        Parameters
        ----------

        Returns
        -------
        list
            The coordinates of the centroid.

        """
        return centroid_points([self.vertex_coordinates(vkey) for vkey in self.vertex])

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, vkey, axes='xyz'):
        """Return the coordinates of a vertex.

        Parameters
        ----------
        vkey : hashable
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
        return [self.vertex[vkey][axis] for axis in axes]

    def vertex_laplacian(self, key):
        """Compute the vector from a vertex to the centroid of its neighbors.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        list
            The components of the vector.
        """
        c = self.vertex_neighborhood_centroid(key)
        p = self.vertex_coordinates(key)
        return subtract_vectors(c, p)

    def vertex_neighborhood_centroid(self, key):
        """Compute the centroid of the neighbors of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        list
            The coordinates of the centroid.
        """
        return centroid_points([self.vertex_coordinates(nbr) for nbr in self.vertex_neighbors(key)])

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    def edge_coordinates(self, u, v, axes='xyz'):
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.
        axes : str (xyz)
            The axes along which the coordinates should be included.

        Returns
        -------
        tuple
            The coordinates of the start point and the coordinates of the end point.

        """
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    def edge_length(self, u, v):
        """Return the length of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        float
            The length of the edge.

        """
        a, b = self.edge_coordinates(u, v)
        return distance_point_point(a, b)

    def edge_vector(self, u, v):
        """Return the vector of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        list
            The vector from u to v.

        """
        a, b = self.edge_coordinates(u, v)
        ab = subtract_vectors(b, a)
        return ab

    def edge_point(self, u, v, t=0.5):
        """Return the location of a point along an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.
        t : float (0.5)
            The location of the point on the edge.
            If the value of ``t`` is outside the range ``0-1``, the point will
            lie in the direction of the edge, but not on the edge vector.

        Returns
        -------
        list
            The XYZ coordinates of the point.

        """
        a, b = self.edge_coordinates(u, v)
        ab = subtract_vectors(b, a)
        return add_vectors(a, scale_vector(ab, t))

    def edge_direction(self, u, v):
        """Return the direction vector of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        list
            The direction vector of the edge.

        """
        return normalize_vector(self.edge_vector(u, v))

    # --------------------------------------------------------------------------
    # halfface geometry
    # --------------------------------------------------------------------------

    def halfface_coordinates(self, hfkey):
        """Compute the coordinates of the vertices of a halfface.

        Parameters
        ----------
        hfkey : hashable
            The identifier of the halfface.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of ``'x'``, ``'y'``, ``'z'``.
            Default is ``'xyz'``.

        Returns
        -------
        list of list
            The coordinates of the vertices of the halfface.

        """
        return [self.vertex_coordinates(key) for key in self.halfface_vertices(hfkey)]

    def halfface_normal(self, hfkey, unitized=True):
        """Compute the oriented normal of a halfface.

        Parameters
        ----------
        fkey : hashable
            The identifier of the halfface.
        unitized : bool, optional
            Unitize the normal vector.
            Default is ``True``.

        Returns
        -------
        list
            The components of the normal vector.

        """
        return normal_polygon(self.halfface_coordinates(hfkey), unitized=unitized)

    def halfface_centroid(self, hfkey):
        """Compute the location of the centroid of a halfface.

        Parameters
        ----------
        hfkey : hashable
            The identifier of the halfface.

        Returns
        -------
        list
            The coordinates of the centroid.

        """
        return centroid_points(self.halfface_coordinates(hfkey))

    def halfface_center(self, hfkey):
        """Compute the location of the center of mass of a halfface.

        Parameters
        ----------
        hfkey : hashable
            The identifier of the halfface.

        Returns
        -------
        list
            The coordinates of the center of mass.

        """
        return centroid_polygon(self.halfface_coordinates(hfkey))

    def halfface_area(self, hfkey):
        """Compute the oriented area of a halfface.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Returns
        -------
        float
            The non-oriented area of the face.

        """
        return length_vector(self.halfface_normal(hfkey, unitized=False))

    def halfface_flatness(self, hfkey, maxdev=0.02):
        """Compute the flatness of a halfface.

        Parameters
        ----------
        hfkey : int
            The identifier of the halfface.

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
        polygon   = self.halfface_coordinates()
        plane     = bestfit_plane(polygon)
        for pt in polygon:
            pt_proj = project_point_plane(pt, plane)
            dev     = distance_point_point(pt, pt_proj)
            if dev > deviation:
                deviation = dev
        return deviation

    def halfface_aspect_ratio(self, hfkey):
        """Face aspect ratio as the ratio between the lengths of the maximum and minimum face edges.

        Parameters
        ----------
        hfkey : Key
            The halfface key.

        Returns
        -------
        float
            The aspect ratio.

        References
        ----------
        .. [1] Wikipedia. *Types of mesh*.
               Available at: https://en.wikipedia.org/wiki/Types_of_mesh.
        """
        face_edge_lengths = [self.edge_length(u, v) for u, v in self.face_halfedges(hfkey)]
        return max(face_edge_lengths) / min(face_edge_lengths)

    face_area         = halfface_area
    face_centroid     = halfface_centroid
    face_center       = halfface_center
    face_coordinates  = halfface_coordinates
    face_flatness     = halfface_flatness
    face_normal       = halfface_normal
    face_aspect_ratio = halfface_aspect_ratio

    # --------------------------------------------------------------------------
    # cell geometry
    # --------------------------------------------------------------------------

    def cell_centroid(self, ckey):
        """Compute the location of the centroid of a cell.

        Parameters
        ----------
        ckey : hashable
            The identifier of the cell.

        Returns
        -------
        list
            The coordinates of the centroid.

        """
        vkeys = self.cell_vertices(ckey)
        return centroid_points([self.vertex_coordinates(vkey) for vkey in vkeys])

    def cell_center(self, ckey):
        """Compute the location of the center of mass of a cell.

        Parameters
        ----------
        ckey : hashable
            The identifier of the cell.

        Returns
        -------
        list
            The coordinates of the center of mass.

        """
        vertices, halffaces = self.cell_to_vertices_and_halffaces(ckey)
        return centroid_polyhedron((vertices, halffaces))

    def cell_vertex_normal(self, ckey, vkey):
        """Return the normal vector at the vertex of a cell as the weighted average of the
        normals of the neighboring halffaces.

        Parameters
        ----------
        ckey : int
            The identifier of the vertex of the cell.
        vkey : int
            The identifier of the vertex of the cell.

        Returns
        -------
        list
            The components of the normal vector.
        """
        vectors = [self.face_normal(hfkey) for hfkey in self.vertex_halffaces(vkey) if hfkey is not None]
        return normalize_vector(centroid_points(vectors))

    # --------------------------------------------------------------------------
    # geometric operations
    # --------------------------------------------------------------------------

    def scale(self, factor=1.0, origin=(0, 0, 0)):
        """Scale the entire volmesh object.

        Parameters
        ----------
        factor : float
            Scaling factor.

        Returns
        -------
        Volmesh
            The volmesh with updated XYZ coordinates.

        """
        for key in self.vertex:
            x, y, z = subtract_vectors(self.vertex_coordinates(key), origin)
            attr = self.vertex[key]
            attr['x'] = origin[0] + x * factor
            attr['y'] = origin[1] + y * factor
            attr['z'] = origin[2] + z * factor


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
