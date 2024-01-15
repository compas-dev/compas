from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import HalfFace
from compas.datastructures import Mesh
from compas.datastructures import Graph
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Vector
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import centroid_polyhedron
from compas.geometry import distance_point_point
from compas.geometry import length_vector
from compas.geometry import normal_polygon
from compas.geometry import normalize_vector
from compas.geometry import volume_polyhedron
from compas.topology import face_adjacency


class CellNetwork(HalfFace):
    """Geometric implementation of a data structure for a collection of mixed topologic entities such as cells, faces, edges and nodes.

    Examples
    --------
    >>> from compas.datastructures import CellNetwork
    >>> cell_network = CellNetwork()
    >>> vertices = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    >>> faces = [[0, 1, 2, 3], [0, 3, 5, 4],[3, 2, 6, 5], [2, 1, 7, 6],[1, 0, 4, 7],[4, 5, 6, 7]]
    >>> cells = [[0, 1, 2, 3, 4, 5]]
    >>> [network.add_vertex(x=x, y=y, z=z) for x, y, z in vertices]
    >>> [cell_network.add_face(fverts) for fverts in faces]
    >>> [cell_network.add_cell(fkeys) for fkeys in cells]
    >>> cell_network

    Parameters
    ----------
    name: str, optional
        The name of the data structure.
    default_vertex_attributes: dict, optional
        Default values for vertex attributes.
    default_edge_attributes: dict, optional
        Default values for edge attributes.
    default_face_attributes: dict, optional
        Default values for face attributes.
    default_cell_attributes: dict, optional
        Default values for cell attributes.
    """

    def __init__(
        self,
        name=None,
        default_vertex_attributes=None,
        default_edge_attributes=None,
        default_face_attributes=None,
        default_cell_attributes=None,
    ):
        _default_vertex_attributes = {"x": 0.0, "y": 0.0, "z": 0.0}
        _default_edge_attributes = default_edge_attributes or {}
        _default_face_attributes = default_face_attributes or {}
        _default_cell_attributes = default_cell_attributes or {}
        if default_vertex_attributes:
            _default_vertex_attributes.update(default_vertex_attributes)
        super(CellNetwork, self).__init__(
            name=name or "CellNetwork",
            default_vertex_attributes=_default_vertex_attributes,
            default_edge_attributes=_default_edge_attributes,
            default_face_attributes=_default_face_attributes,
            default_cell_attributes=_default_cell_attributes,
        )
        self._edge = {}

    def __str__(self):
        tpl = "<CellNetwork with {} vertices, {} faces, {} cells, {} edges>"
        return tpl.format(
            self.number_of_vertices(),
            self.number_of_faces(),
            self.number_of_cells(),
            self.number_of_edges(),
        )

    # --------------------------------------------------------------------------
    # vertex
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex and specify its attributes.

        Parameters
        ----------
        key : hashable, optional
            The identifier of the vertex.
            Defaults to None.
        attr_dict : dict, optional
            A dictionary of vertex attributes.
            Defaults to None.
        **kwattr : dict, optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        hashable
            The identifier of the vertex.
        """
        key = super(CellNetwork, self).add_vertex(key=key, attr_dict=attr_dict, **kwattr)
        if key not in self._edge:
            self._edge[key] = {}
        return key

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, vertex, axes="xyz"):
        """Return the coordinates of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list[float]
            Coordinates of the vertex.
        """
        return [self._vertex[vertex][axis] for axis in axes]

    def vertices_coordinates(self, vertices, axes="xyz"):
        """Return the coordinates of multiple vertices.

        Parameters
        ----------
        vertices : list of int
            The vertex identifiers.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list of list[float]
            Coordinates of the vertices.
        """
        return [self.vertex_coordinates(vertex, axes=axes) for vertex in vertices]

    def vertex_point(self, vertex):
        """Return the point representation of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point.
        """
        return Point(*self.vertex_coordinates(vertex))

    def vertices_points(self, vertices):
        """Returns the point representation of multiple vertices.

        Parameters
        ----------
         vertices : list of int
            The vertex identifiers.

        Returns
        -------
        list of :class:`compas.geometry.Point`
            The points.
        """
        return [self.vertex_point(vertex) for vertex in vertices]

    # --------------------------------------------------------------------------
    # edge
    # --------------------------------------------------------------------------

    def add_edge(self, u, v, attr_dict=None, **kwattr):
        """Add an edge and specify its attributes.

        Parameters
        ----------
        u : hashable
            The identifier of the first node of the edge.
        v : hashable
            The identifier of the second node of the edge.
        attr_dict : dict[str, Any], optional
            A dictionary of edge attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        tuple[hashable, hashable]
            The identifier of the edge.

        Raises
        ------
        ValueError
            If either of the nodes of the edge does not exist.

        """
        if u not in self._vertex:
            raise ValueError("Cannot add edge {}, {} has no vertex {}".format((u, v), self.name, u))
        if v not in self._vertex:
            raise ValueError("Cannot add edge {}, {} has no vertex {}".format((u, v), self.name, u))

        attr = attr_dict or {}
        attr.update(kwattr)

        data = self._edge[u].get(v, {})
        data.update(attr)
        self._edge[u][v] = data
        if v not in self._edge:
            self._edge[v] = {}
        if v not in self._plane[u]:
            self._plane[u][v] = {}
        if u not in self._plane[v]:
            self._plane[v][u] = {}
        return u, v

    def edge_attribute(self, edge, name, value=None):
        """Get or set an attribute of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute, or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.
        """
        u, v = edge
        if u not in self._edge or v not in self._edge[u]:
            raise KeyError(edge)
        attr = self._edge[u][v]
        if value is not None:
            attr[name] = value
            return
        if name in attr:
            return attr[name]
        if name in self.default_edge_attributes:
            return self.default_edge_attributes[name]

    def edges(self, data=False):
        """Iterate over the edges of the cell network.

        Parameters
        ----------
        data : bool, optional
            If True, yield the edge attributes in addition to the edge identifiers.

        Yields
        ------
        tuple[hashable, hashable] | tuple[tuple[hashable, hashable], dict[str, Any]]
            If `data` is False, the next edge identifier (u, v).
            If `data` is True, the next edge identifier and its attributes as a ((u, v), attr) tuple.
        """
        seen = set()
        for u, nbrs in iter(self._edge.items()):
            for v, attr in iter(nbrs.items()):
                if (u, v) in seen or (v, u) in seen:
                    continue
                seen.add((u, v))
                seen.add((v, u))
                if data:
                    yield (u, v), attr
                else:
                    yield u, v

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    def edge_coordinates(self, edge, axes="xyz"):
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.
        axes : str, optional
            The axes along which the coordinates should be included.

        Returns
        -------
        tuple[list[float], list[float]]
            The coordinates of the start point.
            The coordinates of the end point.
        """
        u, v = edge
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    def edge_start(self, edge):
        """Return the start point of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Point`
            The start point.
        """
        return self.vertex_point(edge[0])

    def edge_end(self, edge):
        """Return the end point of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Point`
            The end point.
        """
        return self.vertex_point(edge[1])

    def edge_vector(self, edge):
        """Return the vector of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The vector from start to end.
        """
        a, b = self.edge_coordinates(edge)
        return Vector.from_start_end(a, b)

    def edge_direction(self, edge):
        """Return the direction vector of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The direction vector of the edge.
        """
        return Vector(*normalize_vector(self.edge_vector(edge)))

    def edge_line(self, edge):
        """Return the line representation of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Line`
            The line.
        """
        return Line(*self.edge_coordinates(edge))

    def edge_length(self, edge):
        """Return the length of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        float
            The length of the edge.
        """
        a, b = self.edge_coordinates(edge)
        return distance_point_point(a, b)

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    def edge_faces(self, edge):
        """Return the faces adjacent to an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        list[int]
            The identifiers of the adjacent faces.
        """
        u, v = edge
        faces = set()
        if v in self._plane[u]:
            faces.update(self._plane[u][v].keys())
        if u in self._plane[v]:
            faces.update(self._plane[v][u].keys())
        return sorted(list(faces))

    def edges_no_face(self):
        """Find the edges that are not part of a face.

        Returns
        -------
        list[int]
            The edges without face.

        """
        edges = {edge for edge in self.edges() if not self.edge_faces(edge)}
        return list(edges)

    def non_manifold_edges(self):
        """Returns the edges that belong to more than two faces.

        Returns
        -------
        list[int]
            The edges without face.

        """
        edges = {edge for edge in self.edges() if len(self.edge_faces(edge)) > 2}
        return list(edges)

    # --------------------------------------------------------------------------
    # faces
    # --------------------------------------------------------------------------

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face to the cell network.

        Parameters
        ----------
        vertices : list[int]
            A list of ordered vertex keys representing the face.
            For every vertex that does not yet exist, a new vertex is created.
        fkey : int, optional
            The face identifier.
        attr_dict : dict[str, Any], optional
            dictionary of halfface attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The key of the face.

        See Also
        --------
        :meth:`add_vertex`, :meth:`add_cell`, :meth:`add_edge`

        Notes
        -----
        If no key is provided for the face, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.
        """
        fkey = self.add_halfface(vertices, fkey=fkey, attr_dict=attr_dict, **kwattr)

        for edge in self.face_edges(fkey):
            self.add_edge(*edge)
        return fkey

    def face_attribute(self, face, name, value=None):
        """Get or set an attribute of a face.

        Parameters
        ----------
        face : int
            The face identifier.
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute, or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the face does not exist.

        See Also
        --------
        :meth:`unset_face_attribute`
        :meth:`face_attributes`, :meth:`faces_attribute`, :meth:`faces_attributes`
        :meth:`vertex_attribute`, :meth:`edge_attribute`, :meth:`cell_attribute`

        """
        if face not in self._halfface:
            raise KeyError(face)
        if value is not None:
            if face not in self._face_data:
                self._face_data[face] = {}
            self._face_data[face][name] = value
            return
        if face in self._face_data and name in self._face_data[face]:
            return self._face_data[face][name]
        if name in self.default_face_attributes:
            return self.default_face_attributes[name]

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
        list[int]
            Ordered vertex identifiers.

        """
        return self.halfface_vertices(face)

    def face_coordinates(self, face, axes="xyz"):
        """Compute the coordinates of the vertices of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list[list[float]]
            The coordinates of the vertices of the face.

        See Also
        --------
        :meth:`face_points`, :meth:`face_polygon`, :meth:`face_normal`, :meth:`face_centroid`, :meth:`face_center`
        :meth:`face_area`, :meth:`face_flatness`, :meth:`face_aspect_ratio`

        """
        return [self.vertex_coordinates(vertex, axes=axes) for vertex in self.face_vertices(face)]

    def face_points(self, face):
        """Compute the points of the vertices of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list[:class:`compas.geometry.Point`]
            The points of the vertices of the face.

        See Also
        --------
        :meth:`face_polygon`, :meth:`face_normal`, :meth:`face_centroid`, :meth:`face_center`

        """
        return [self.vertex_point(vertex) for vertex in self.face_vertices(face)]

    def face_polygon(self, face):
        """Compute the polygon of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        :class:`compas.geometry.Polygon`
            The polygon of the face.

        See Also
        --------
        :meth:`face_points`, :meth:`face_normal`, :meth:`face_centroid`, :meth:`face_center`

        """
        return Polygon(self.face_points(face))

    def face_normal(self, face, unitized=True):
        """Compute the oriented normal of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.
        unitized : bool, optional
            If True, unitize the normal vector.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The normal vector.

        See Also
        --------
        :meth:`face_points`, :meth:`face_polygon`, :meth:`face_centroid`, :meth:`face_center`

        """
        return Vector(*normal_polygon(self.face_coordinates(face), unitized=unitized))

    def face_centroid(self, face):
        """Compute the point at the centroid of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        :class:`compas.geometry.Point`
            The coordinates of the centroid.

        See Also
        --------
        :meth:`face_points`, :meth:`face_polygon`, :meth:`face_normal`, :meth:`face_center`

        """
        return Point(*centroid_points(self.face_coordinates(face)))

    def face_center(self, face):
        """Compute the point at the center of mass of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        :class:`compas.geometry.Point`
            The coordinates of the center of mass.

        See Also
        --------
        :meth:`face_points`, :meth:`face_polygon`, :meth:`face_normal`, :meth:`face_centroid`

        """
        return Point(*centroid_polygon(self.face_coordinates(face)))

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

        See Also
        --------
        :meth:`face_flatness`, :meth:`face_aspect_ratio`

        """
        return length_vector(self.face_normal(face, unitized=False))

    halfface_area = face_area
    halfface_centroid = face_centroid
    halfface_center = face_center
    halfface_coordinates = face_coordinates
    halfface_normal = face_normal

    def mesh_from_faces(self, faces, data=False):
        """Construct a mesh from a list of faces.

        Parameters
        ----------
        faces : list
            A list of face identifiers.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh.

        """
        faces_vertices = [self.face_vertices(face) for face in faces]
        mesh = Mesh()
        for fkey, vertices in zip(faces, faces_vertices):
            for v in vertices:
                x, y, z = self.vertex_coordinates(v)
                mesh.add_vertex(key=v, x=x, y=y, z=z)
            if data:
                mesh.add_face(vertices, fkey=fkey, attr_dict=self.face_attributes(fkey))
            else:
                mesh.add_face(vertices, fkey=fkey)
        return mesh

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    def face_edges(self, face):
        return self.halfface_halfedges(face)

    def face_neighbors(self, fkey):
        """Return the neighbors of a face across its edges.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        list[int]
            The identifiers of the neighboring faces.

        """
        nbrs = set()
        for edge in self.face_edges(fkey):
            nbrs.update(self.edge_faces(edge))
        return list(nbrs - {fkey})

    def edge_face_adjacency(self, faces=None):
        """Returns an adjacency where adjacency[edge] = {face1, face2}.

        Parameters
        ----------
        faces : list of int, optional
            The faces for which to compute the adjacency, defaults to all faces in the datastructure

        Returns
        -------
        dict
            A dictionary dict[edge] = face key

        """
        faces = faces or self.faces()
        adjacency = {}
        for face in faces:
            for u, v in self.face_edges(face):
                key = (u, v) if u < v else (v, u)
                if key not in adjacency:
                    adjacency[key] = {face}
                else:
                    adjacency[key].add(face)
        return adjacency

    def face_adjacency(self, faces=None):
        """Construct a face adjacency dictionary from a list of faces.

        Parameters
        ----------
        faces : list
            A list of faces.

        Returns
        -------
        dict
            A face adjacency dictionary.

        """
        faces = faces or self.faces()
        faces_vertices = [self.face_vertices(face) for face in faces]
        vertices = list({v: None for face in faces_vertices for v in face}.keys())  # unique, but keep order
        return face_adjacency(vertices, faces)

    def face_cells(self, fkey):
        """Return the cells connected to a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        list[int]
            The identifiers of the cells connected to the face.

        """
        cells = {cell for cell in [self.halfface_cell(fkey), self.halfface_opposite_cell(fkey)] if cell is not None}
        return list(cells)

    def faces_no_cell(self):
        """Find the faces that are not part of a cell.

        Returns
        -------
        list[int]
            The faces without cell.

        """
        faces = {fkey for fkey in self.faces() if not self.face_cells(fkey)}
        return list(faces)

    def is_halfface_on_boundary(self, halfface):
        """Verify that a face is on the boundary.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.

        """
        u, v = self._halfface[halfface][:2]
        cu = 0 if self._plane[v][u][halfface] is None else 1
        cv = 0 if self._plane[u][v][halfface] is None else 1
        return (cu + cv) == 1  # only one of them

    is_face_on_boundary = is_halfface_on_boundary

    def faces_on_boundaries(self):
        return self.halffaces_on_boundaries()

    def face_cell_adjacency(self, faces=None):
        """Returns an adjacency where adjacency[face] = [cell1, cell2].

        Parameters
        ----------
        faces : list of int, optional
            The faces for which to compute the adjacency, defaults to all faces in the datastructure.

        """
        faces = faces or self.faces()
        adjacency = {}
        for face in faces:
            cells = self.face_cells(face)
            if len(cells):
                adjacency[face] = cells
        return adjacency

    # --------------------------------------------------------------------------
    # cell
    # --------------------------------------------------------------------------

    def add_cell(self, faces, ckey=None, attr_dict=None, **kwattr):
        """Add a cell to the cell network object.

        In order to add a valid cell to the network, the faces must form a closed mesh.
        If the faces do not form a closed mesh, the cell is not added to the network.

        Parameters
        ----------
        faces : list[int]
            The face keys of the cell.
        ckey : int, optional
            The cell identifier.
        attr_dict : dict[str, Any], optional
            A dictionary of cell attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The key of the cell.

        Raises
        ------
        TypeError
            If the provided cell key is of an unhashable type.


        Notes
        -----
        If no key is provided for the cell, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        """

        faces = list(set(faces))

        # 1. Check if the faces form a closed cell
        #    Note: We cannot use mesh.is_closed() here because it only works if the faces are unified
        if any(len(edge_faces) != 2 for _, edge_faces in self.edge_face_adjacency(faces).items()):
            print("Cannot add cell, faces {} do not form a closed cell.".format(faces))
            return

        # 2. Check if the faces can be unified
        mesh = self.mesh_from_faces(faces, data=False)
        try:
            mesh.unify_cycles()
        except AssertionError:
            print("Cannot add cell, faces {} can not be unified.".format(faces))
            return

        # 3. Check if the faces are oriented correctly
        #    If the volume of the polyhedron is negative, we need to flip the faces
        vertices, faces = mesh.to_vertices_and_faces()
        volume = volume_polyhedron((vertices, faces))
        if volume < 0:
            mesh.flip_cycles()

        if ckey is None:
            ckey = self._max_cell = self._max_cell + 1
        ckey = int(ckey)
        if ckey > self._max_cell:
            self._max_cell = ckey
        attr = attr_dict or {}
        attr.update(kwattr)
        self._cell[ckey] = {}
        for name, value in attr.items():
            self.cell_attribute(ckey, name, value)
        for fkey in mesh.faces():
            vertices = mesh.face_vertices(fkey)
            for i in range(-2, len(vertices) - 2):
                u = vertices[i]
                v = vertices[i + 1]
                if u not in self._cell[ckey]:
                    self._cell[ckey][u] = {}
                self._plane[u][v][fkey] = ckey
                self._cell[ckey][u][v] = fkey
        return ckey

    # --------------------------------------------------------------------------
    # cell geometry
    # --------------------------------------------------------------------------

    def cell_points(self, cell):
        """Compute the points of the vertices of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        list[:class:`compas.geometry.Point`]
            The points of the vertices of the cell.

        See Also
        --------
        :meth:`cell_polygon`, :meth:`cell_centroid`, :meth:`cell_center`
        """
        return [self.vertex_point(vertex) for vertex in self.cell_vertices(cell)]

    def cell_centroid(self, cell):
        """Compute the point at the centroid of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        :class:`compas.geometry.Point`
            The coordinates of the centroid.

        See Also
        --------
        :meth:`cell_center`
        """
        vertices = self.cell_vertices(cell)
        return Point(*centroid_points([self.vertex_coordinates(vertex) for vertex in vertices]))

    def cell_center(self, cell):
        """Compute the point at the center of mass of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        :class:`compas.geometry.Point`
            The coordinates of the center of mass.

        See Also
        --------
        :meth:`cell_centroid`
        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return Point(*centroid_polyhedron((vertices, faces)))

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
        :class:`compas.geometry.Vector`
            The components of the normal vector.

        """
        cell_faces = self.cell_faces(cell)
        vectors = [self.face_normal(face) for face in self.vertex_halffaces(vertex) if face in cell_faces]
        return Vector(*normalize_vector(centroid_points(vectors)))

    def cell_polyhedron(self, cell):
        """Construct a polyhedron from the vertices and faces of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        :class:`compas.geometry.Polyhedron`
            The polyhedron.

        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return Polyhedron(vertices, faces)

    def cell_to_vertices_and_faces(self, cell):
        """Return the vertices and faces of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list[list[float]]
            A list of vertices, represented by their XYZ coordinates,
        list[list[int]]
            A list of faces, with each face a list of vertex indices.

        See Also
        --------
        :meth:`cell_to_mesh`

        """
        vertices = self.cell_vertices(cell)
        faces = self.cell_faces(cell)
        vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
        vertices = [self.vertex_coordinates(vertex) for vertex in vertices]
        faces = [[vertex_index[vertex] for vertex in self.halfface_vertices(face)] for face in faces]
        return vertices, faces

    def cell_to_mesh(self, cell):
        """Construct a mesh object from from a cell of a cell network.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        See Also
        --------
        :meth:`cell_to_vertices_and_faces`

        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return Mesh.from_vertices_and_faces(vertices, faces)

    # --------------------------------------------------------------------------
    # cell topology
    # --------------------------------------------------------------------------

    def cells_on_boundaries(self):
        """Find the cells on the boundary.

        Returns
        -------
        list[int]
            The cells of the boundary.

        See Also
        --------
        :meth:`vertices_on_boundaries`, :meth:`faces_on_boundaries`

        """
        cells = set()
        for face in self.faces_on_boundaries():
            cells.update(self.face_cells(face))
        return list(cells)

    # --------------------------------------------------------------------------
    # data
    # --------------------------------------------------------------------------

    @property
    def data(self):
        """Returns a dictionary of structured data representing the cell network data object.

        Note that some of the data stored internally in the data structure object is not included in the dictionary representation of the object.
        This is the case for data that is considered private and/or redundant.
        Specifically, the plane dictionary are not included.
        This is because the information in these dictionaries can be reconstructed from the other data.
        Therefore, to keep the dictionary representation as compact as possible, these dictionaries are not included.

        Returns
        -------
        dict
            The structured data representing the cell network.

        """
        cell = {}
        for c in self._cell:
            faces = set()
            for u in self._cell[c]:
                for v in self._cell[c][u]:
                    faces.add(self._cell[c][u][v])
            cell[c] = sorted(list(faces))

        return {
            "attributes": self.attributes,
            "dva": self.default_vertex_attributes,
            "dea": self.default_edge_attributes,
            "dfa": self.default_face_attributes,
            "dca": self.default_cell_attributes,
            "vertex": self._vertex,
            "cell": cell,
            "face": self._halfface,
            "edge": self._edge,
            "face_data": self._face_data,
            "cell_data": self._cell_data,
            "max_vertex": self._max_vertex,
            "max_face": self._max_face,
            "max_cell": self._max_cell,
        }

    @classmethod
    def from_data(cls, data):
        cell_network = cls()
        cell_network.data = data
        return cell_network

    @data.setter
    def data(self, data):
        self._vertex = {}
        self._halfface = {}
        self._cell = {}
        self._plane = {}
        self._face_data = {}
        self._cell_data = {}
        self._max_vertex = -1
        self._max_face = -1
        self._max_cell = -1
        vertex = data.get("vertex", {})
        cell = data.get("cell", {})
        face = data.get("face", {})
        edge = data.get("edge", {})

        self.attributes.update(data.get("attributes", {}))
        self.default_vertex_attributes.update(data.get("dva") or {})
        self.default_edge_attributes.update(data.get("dea") or {})
        self.default_face_attributes.update(data.get("dfa") or {})
        self.default_cell_attributes.update(data.get("dca") or {})
        for key, attr in iter(vertex.items()):
            self.add_vertex(key=key, attr_dict=attr)
        for u in edge:
            for v, attr in edge[u].items():
                self.add_edge(u, v, attr_dict=attr)
        face_data = data.get("face_data", {})
        for key, vertices in iter(face.items()):
            attr = face_data.get(key) or {}
            self.add_halfface(vertices, fkey=key, attr_dict=attr)
        cell_data = data.get("cell_data", {})
        for ckey, faces in iter(cell.items()):
            attr = cell_data.get(ckey) or {}
            self.add_cell(faces, ckey=ckey, attr_dict=attr)
        self._max_vertex = data.get("max_vertex", self._max_vertex)
        self._max_face = data.get("max_face", self._max_face)
        self._max_cell = data.get("max_cell", self._max_cell)

    # --------------------------------------------------------------------------
    # extraction
    # --------------------------------------------------------------------------

    def to_network(self):
        """Convert the cell network to a graph.

        Returns
        -------
        :class:`compas.datastructures.Graph`
            A graph object.

        """
        graph = Graph()
        for vertex, attr in self.vertices(data=True):
            x, y, z = self.vertex_coordinates(vertex)
            graph.add_node(key=vertex, x=x, y=y, z=z, attr_dict=attr)
        for (u, v), attr in self.edges(data=True):
            graph.add_edge(u, v, attr_dict=attr)
        return graph
