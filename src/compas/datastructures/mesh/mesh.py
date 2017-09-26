from __future__ import print_function

from compas.files.obj import OBJ
from compas.files.ply import PLYreader

from compas.utilities import geometric_key

from compas.utilities.itertools_ import pairwise

from compas.datastructures._graph import Graph


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


# @todo: don't allow the addition of edges
#        for which two opposite halfedges do not already exist


class Mesh(Graph):
    """Class representing a mesh.

    The datastructure of the mesh is implemented as a half-edge.

    Parameters:
        vertices (:obj:`list` of :obj:`dict`) : Optional. A sequence of vertices to add to the mesh.
            Each vertex should be a dictionary of vertex attributes.
        faces (:obj:`list` of :obj:`list`) : Optional. A sequence of faces to add to the mesh.
            Each face should be a list of vertex keys.
        dva (dict) : Optional. A dictionary of default vertex attributes.
        dfa (dict) : Optional. A dictionary of default face attributes.
        dea (dict) : Optional. A dictionary of default edge attributes.
        kwargs (dict) : The remaining named parameters. These are added to the attributes
            dictionary of the instance.

    Attributes:
        vertex (dict) : The vertex dictionary.
            With every key in the dictionary corresponds a dictionary of attributes.
        face (dict) : The face dictionary.
            With every key in the dictionary corresponds a dictionary of half-edges.
        halfedge (dict) : The half-edge dictionary.
            Every key in the dictionary corresponds to a vertex of the mesh.
            With every key corresponds a dictionary of neighbours pointing to face keys.
        edge (dict) : The edge dictionary.
            Every key in the dictionary corresponds to a vertex.
            With every key corresponds a dictionary of neighbours pointing to attribute dictionaries.
        attributes (dict) : General mesh attributes.
        facedata (Mesh, optional) : A ``Mesh`` object for keeping track of face attributes
            by storing them on dual vertices.

    Examples:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.visualization.plotters import MeshPlotter

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            plotter = MeshPlotter(mesh)

            plotter.draw_vertices(radius=0.2)
            plotter.draw_faces()
            plotter.show()


        .. plot::
            :include-source:

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.visualization.plotters import MeshPlotter

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            plotter = MeshPlotter(mesh)

            plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2)
            plotter.draw_faces()
            plotter.show()


        .. plot::
            :include-source:

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.visualization.plotters import MeshPlotter

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            plotter = MeshPlotter(mesh)

            plotter.draw_vertices(radius=0.2)
            plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})
            plotter.show()


        >>> for key in mesh.vertex:
        ...     print(key)
        ...

        >>> for key in mesh.vertices():
        ...     print(key)
        ...

        >>> for key in mesh.vertices_iter():
        ...     print(key)
        ...

        >>> for index, key in mesh.vertices_enum():
        ...     print(index, key)
        ...

        >>> for key, attr in mesh.vertices(True):
        ...     print(key, attr)
        ...

        >>> for key, attr in mesh.vertices_iter(True):
        ...     print(key, attr)
        ...

        >>> for index, key, attr in mesh.vertices_enum(True):
        ...     print(index, key, attr)
        ...

    """

    def __init__(self):
        super(Mesh, self).__init__()
        self.attributes.update({
            'name'         : 'Mesh',
            'color.vertex' : None,
            'color.edge'   : None,
            'color.face'   : None,
        })

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

    def __str__(self):
        """"""
        v = self.number_of_vertices()
        e = self.number_of_edges()
        f = self.number_of_faces()

        if not self.vertex:
            dmin = 0
        else:
            dmin = min(self.vertex_degree(key) for key in self.vertices())

        if not self.vertex:
            dmax = 0
        else:
            dmax = max(self.vertex_degree(key) for key in self.vertices())

        if not self.default_vertex_attributes:
            dva = None
        else:
            dva = '\n'.join(['{0} => {1}'.format(key, value) for key, value in self.default_vertex_attributes.items()])

        if not self.default_edge_attributes:
            dea = None
        else:
            dea = '\n'.join(['{0} => {1}'.format(key, value) for key, value in self.default_edge_attributes.items()])

        if not self.default_face_attributes:
            dfa = None
        else:
            dfa = '\n'.join(['{0} => {1}'.format(key, value) for key, value in self.default_face_attributes.items()])

        return """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
mesh: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- default vertex attributes

{}

- default edge attributes

{}

- default face attributes

{}

- number of vertices: {}
- number of edges: {}
- number of faces: {}

- vertex degree min: {}
- vertex degree max: {}

- face degree min: {}
- face degree max: {}

""".format(self.attributes['name'], dva, dea, dfa, v, e, f, dmin, dmax, None, None)

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath, **kwargs):
        """Initialise a mesh from the data described in an obj file.

        Parameters:
            filepath (str): The path to the obj file.
            kwargs (dict) : Remaining named parameters. Default is an empty :obj:`dict`.

        Returns:
            Mesh: A ``Mesh`` of class ``cls``.

        >>> mesh = Mesh.from_obj('path/to/file.obj')

        """
        mesh = cls()
        mesh.attributes.update(kwargs)
        obj = OBJ(filepath)
        vertices = obj.parser.vertices
        faces = obj.parser.faces
        for x, y, z in vertices:
            mesh.add_vertex(x=x, y=y, z=z)
        for face in faces:
            mesh.add_face(face)
        return mesh

    @classmethod
    def from_ply(cls, filepath, **kwargs):
        reader = PLYreader(filepath)
        reader.read()
        vertices = [(vertex['x'], vertex['y'], vertex['z']) for vertex in reader.vertices]
        faces = [face['vertex_indices'] for face in reader.faces]
        mesh = cls.from_vertices_and_faces(vertices, faces, **kwargs)
        return mesh

    @classmethod
    def from_lines(cls, lines, boundary_face=False, precision='3f'):
        """"""
        from compas.datastructures.network.algorithms.duality import _sort_neighbours
        from compas.datastructures.network.algorithms.duality import _find_first_neighbour
        from compas.datastructures.network.algorithms.duality import _find_edge_face

        mesh = cls()
        edges   = []
        vertex  = {}
        for line in lines:
            sp = line[0]
            ep = line[1]
            a  = geometric_key(sp, precision)
            b  = geometric_key(ep, precision)
            vertex[a] = sp
            vertex[b] = ep
            edges.append((a, b))
        key_index = dict((k, i) for i, k in enumerate(iter(vertex)))
        for key, xyz in iter(vertex.items()):
            i = key_index[key]
            mesh.add_vertex(i, x=xyz[0], y=xyz[1], z=xyz[2])
        edges_uv = []
        for u, v in edges:
            i = key_index[u]
            j = key_index[v]
            edges_uv.append((i, j))
        # the clear commands below are from the network equivalent. Needed?
        # network.clear_facedict()
        # network.clear_halfedgedict()
        mesh.halfedge = dict((key, {}) for key in mesh.vertex)
        for u, v in edges_uv:
            mesh.halfedge[u][v] = None
            mesh.halfedge[v][u] = None
        _sort_neighbours(mesh)

        u = sorted(mesh.vertices(True), key=lambda x: (x[1]['y'], x[1]['x']))[0][0]
        v = _find_first_neighbour(u, mesh)
        key_boundary_face = _find_edge_face(u, v, mesh)
        print(key_boundary_face)
        for u, v in mesh.edges():
            if mesh.halfedge[u][v] is None:
                _find_edge_face(u, v, mesh)
            if mesh.halfedge[v][u] is None:
                _find_edge_face(v, u, mesh)

        if not boundary_face:
            mesh.delete_face(key_boundary_face)
        return mesh

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces, **kwargs):
        """Initialise a mesh from a list of vertices and faces.

        Parameters:
            vertices (list) : A list of vertices, represented by their XYZ coordinates.
            faces (list) : A list of faces. Each face is a list of indices referencing
                the list of vertex coordinates.
            kwargs (dict) : Remaining named parameters. Default is an empty :obj:`dict`.

        Returns:
            Mesh: A ``Mesh`` of class ``cls``.

        >>> vertices = []
        >>> faces = []
        >>> mesh = Mesh.from_vertices_and_faces(vertices, faces)

        """
        mesh = cls()
        mesh.attributes.update(kwargs)
        for x, y, z in iter(vertices):
            mesh.add_vertex(x=x, y=y, z=z)
        for face in iter(faces):
            mesh.add_face(face)
        return mesh

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_obj(self, filepath):
        """Write the mesh to an OBJ file.

        Parameters:
            filepath (str): Full path of the file to write.

        Notes:
            Use the framework ``OBJ`` functionality for this. How to write vertices
            and faces to an ``OBJ`` is not necessarily something a mesh knows how
            to do.
        """
        key_index = self.key_index()
        with open(filepath, 'wb+') as fh:
            for key, attr in self.vertices(True):
                fh.write('v {0[x]:.3f} {0[y]:.3f} {0[z]:.3f}\n'.format(attr))
            for fkey in self.face:
                vertices = self.face_vertices(fkey, ordered=True)
                vertices = [key_index[key] + 1 for key in vertices]
                ixs = ['f']
                for vkey in vertices:
                    ixs.append('{0}'.format(vkey))
                fh.write(' '.join(ixs) + '\n')

    def to_vertices_and_faces(self):
        """Return the vertices and faces of a mesh.

        Returns:
            (list, list): A tuple with a list of vertices, represented by their
                XYZ coordinates, and a list of faces. Each face is a list of
                indices referencing the list of vertex coordinates.
        """
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [self.face_vertices(fkey, ordered=True) for fkey in self.faces()]
        return vertices, faces

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex and specify its attributes (optional).

        Note:
            If no key is provided for the vertex, one is generated
            automatically. An automatically generated key increments the highest
            key in use by 1::

                key = int(sorted(self.vertex.keys())[-1]) + 1

        Parameters:
            key (int): An identifier for the vertex. Defaults to None. The key
                is converted to a string before it is used.
            attr_dict (dict): Vertex attributes, defaults to ``None``.
            **attr: Other named vertex attributes, defaults to an empty :obj:`dict`.

        Returns:
            str: The key of the vertex.

        Examples:
            >>> mesh = Mesh()
            >>> mesh.add_vertex()
            '0'
            >>> mesh.add_vertex(x=0, y=0, z=0)
            '1'
            >>> mesh.add_vertex(key=2)
            '2'
            >>> mesh.add_vertex(key=0, x=1)
            '0'
        """
        attr = self.default_vertex_attributes.copy()
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        attr.update(attr_dict)

        key = self._get_vertexkey(key)

        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
            self.edge[key] = {}

        self.vertex[key].update(attr)

        return key

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face and specify its attributes (optional).

        Note:
            * A dictionary key for the face will be generated automatically, based on
              the keys of its vertices.
            * All faces are closed. The closing link is implied and, therefore,
              the last vertex in the list should be different from the first.
            * Building a face_adjacency list is slow, if we can't rely on the fact
              that all faces have the same cycle directions. Therefore, it is
              worth considering to ensure unified cycle directions upon addition
              of a new face.

        Parameters:
            vertices (list): A list of vertex keys.

        Returns:
            str: The key of the face.
        """
        attr = self.default_face_attributes.copy()
        if attr_dict is None:
            attr_dict = {}
        attr_dict.update(kwattr)
        attr.update(attr_dict)

        if vertices[0] == vertices[-1]:
            del vertices[-1]
        if vertices[-2] == vertices[-1]:
            del vertices[-1]
        if len(vertices) < 3:
            return

        keys = []
        for key in vertices:
            if key not in self.vertex:
                key = self.add_vertex(key)
            keys.append(key)

        fkey = self._get_facekey(fkey)

        self.face[fkey] = keys
        self.facedata[fkey] = attr

        halfedges = keys + keys[0:1]

        for u, v in pairwise(halfedges):
            self.halfedge[u][v] = fkey
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None
            if v not in self.edge[u]:
                if u not in self.edge[v]:
                    self.edge[u][v] = self.default_edge_attributes.copy()

        return fkey

    def add_faces(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    # this should be delete_vertex
    def remove_vertex(self, key):
        nbrs = self.vertex_neighbours(key)
        for nbr in nbrs:
            fkey = self.halfedge[key][nbr]
            if fkey is None:
                continue
            for u, v in self.face_halfedges(fkey):
                self.halfedge[u][v] = None
            del self.face[fkey]
        for nbr in nbrs:
            del self.halfedge[nbr][key]
        for nbr in nbrs:
            for n in self.vertex_neighbours(nbr):
                if self.halfedge[nbr][n] is None and self.halfedge[n][nbr] is None:
                    del self.halfedge[nbr][n]
                    del self.halfedge[n][nbr]
        del self.halfedge[key]
        del self.vertex[key]

    def delete_vertex(self, key):
        raise NotImplementedError

    def insert_vertex(self, fkey, key=None, xyz=None, return_key=False):
        """Insert a vertex in the specified face.

        Parameters:
            fkey (str): The key of the face in which the vertex should be inserted.

        Returns:
            str: The keys of the newly created faces.

        Raises:
            ValueError: If the face does not exist.
        """
        fkeys = []
        if not xyz:
            x, y, z = self.face_center(fkey)
        else:
            x, y, z = xyz
        w = self.add_vertex(key=key, x=x, y=y, z=z)
        for u, v in self.face_halfedges(fkey):
            fkeys.append(self.add_face([u, v, w]))
        del self.face[fkey]
        if return_key:
            return w
        return fkeys

    def delete_face(self, fkey):
        for u, v in self.face_halfedges(fkey):
            self.halfedge[u][v] = None
            if self.halfedge[v][u] is None:
                del self.halfedge[u][v]
                del self.halfedge[v][u]
        del self.face[fkey]

    def cull_unused_vertices(self):
        for u in self.vertices():
            if u not in self.halfedge:
                del self.vertex[u]
            else:
                if not self.halfedge[u]:
                    del self.vertex[u]
                    del self.halfedge[u]

    def cull_unused_edges(self):
        for u, v in self.edges():
            if u not in self.halfedge:
                del self.edge[u][v]
            if v not in self.halfedge[u]:
                del self.edge[u][v]
            if len(self.edge[u]) == 0:
                del self.edge[u]

    # def add_edges_from_faces(self):
    #     for fkey in self.faces():
    #         for u, v in self.face_halfedges(fkey):
    #             if u in self.edge and v in self.edge[u]:
    #                 continue
    #             if v in self.edge and u in self.edge[v]:
    #                 continue
    #             self.add_edge(u, v)

    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------

    def is_valid(self):
        # a mesh is valid if the following conditions are true
        # - halfedges don't point at non-existing faces
        # - all vertices are in the halfedge dict
        # - there are no None-None halfedges
        # - all faces have corresponding halfedge entries
        for key in self.vertices():
            if key not in self.halfedge:
                return False
        for u in self.halfedge:
            if u not in self.vertex:
                return False
            for v in self.halfedge[u]:
                if v not in self.vertex:
                    return False
                if self.halfedge[u][v] is None and self.halfedge[v][u] is None:
                    return False
                fkey = self.halfedge[u][v]
                if fkey:
                    if fkey not in self.face:
                        return False
        for fkey in self.faces():
            for u, v in self.face_halfedges(fkey):
                if u not in self.vertex:
                    return False
                if v not in self.vertex:
                    return False
                if u not in self.halfedge:
                    return False
                if v not in self.halfedge[u]:
                    return False
                if fkey != self.halfedge[u][v]:
                    return False
        return True

    def is_regular(self):
        """Return True if all faces have the same number of edges, and all vertices
        have the same degree (i.e. have the same valence: are incident to the same
        number of edges).

        Note:
            Not sure if the second condition makes sense.
            Example of a regular mesh?
        """
        if not self.vertex or not self.face:
            return False

        vkey = self.get_any_vertex()
        degree = self.vertex_degree(vkey)

        for vkey in self.vertices():
            if self.vertex_degree(vkey) != degree:
                return False

        fkey = self.get_any_face()
        vcount = len(self.face_vertices(fkey))

        for fkey in self.faces():
            vertices = self.face_vertices(fkey)

            if len(vertices) != vcount:
                return False

        return True

    def is_manifold(self):
        """Return True if each edge is incident to only one or two faces, and the
        faces incident to a vertex form a closed or an open fan.

        Note:
            The first condition seems to be fullfilled by construction?!
        """
        if not self.vertex:
            return False

        for key in self.vertices():
            nbrs = self.vertex_neighbours(key, ordered=True)

            if not nbrs:
                return False

            if self.halfedge[nbrs[0]][key] is None:
                for nbr in nbrs[1:-1]:
                    if self.halfedge[key][nbr] is None:
                        return False

                if self.halfedge[key][nbrs[-1]] is not None:
                    return False
            else:
                for nbr in nbrs[1:]:
                    if self.halfedge[key][nbr] is None:
                        return False

        return True

    def is_orientable(self):
        """A manifold mesh is orientable if any two adjacent faces have compatible
        orientation (i.e. if the faces have a unified cycle direction)."""
        raise NotImplementedError

    # as in "does the mesh have a boundary?"
    # and no holes?
    def is_closed(self):
        raise NotImplementedError

    def is_trimesh(self):
        if not self.face:
            return False
        return not any(3 != len(self.face_vertices(fkey)) for fkey in self.faces())

    def is_quadmesh(self):
        if not self.face:
            return False
        return not any(4 != len(self.face_vertices(fkey)) for fkey in self.faces())

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    def edges(self, data=False):
        for u, v in self.halfedges():
            if u in self.edge and v in self.edge[u]:
                if data:
                    yield u, v, self.edge[u][v]
                else:
                    yield u, v
            elif v in self.edge and u in self.edge[v]:
                if data:
                    yield v, u, self.edge[v][u]
                else:
                    yield v, u
            else:
                if u not in self.edge:
                    self.edge[u] = {}
                self.edge[u][v] = {}
                if data:
                    yield u, v, self.edge[u][v]
                else:
                    yield u, v

    # def vertices_iter(self, data=False):
    #     """Get an iterator over the list of vertex keys. If `data` is True, get
    #     an iterator over key, data pairs.

    #     Parameters:
    #         data (bool): Return key, data pairs, defaults to False.

    #     Returns:
    #         iter: An iterator of vertex keys, if data is False.
    #         iter: An iterator of key, data pairs, if data is True.
    #     """
    #     return self.vertices(data=data)

    # def vertices_enum(self, data=False):
    #     """Get an enumeration of the vertex keys.

    #     Parameters:
    #         data (bool) : If ``True``, return the vertex attributes as part of
    #             the enumeration. Default is ``False``.

    #     Returns:
    #         iter : The enumerating iterator of vertex keys.

    #     >>> for index, key in mesh.vertices_enum():
    #     ...     print(index, key)
    #     ...

    #     >>> for index, key, attr in mesh.vertices_enum(data=True):
    #     ...     print(index, key, attr)
    #     ...

    #     """
    #     return enumerate(self.vertices(data=data))

    # def edges_iter(self, data=False):
    #     return self.edges(data=data)

    # def edges_enum(self, data=False):
    #     return enumerate(self.edges(data=data))

    # def faces_iter(self, data=False):
    #     return self.faces(data=data)

    # def faces_enum(self, data=False):
    #     return enumerate(self.faces(data=data))

    # --------------------------------------------------------------------------
    # default attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # vertex attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # edge attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # face attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    # def vertex_cycle(self, key):
    #     nbrs = self.vertex_neighbours(key, ordered=True)
    #     return dict((nbrs[i], nbrs[i + 1]) for i in range(-1, len(nbrs) - 1))

    # def vertex_descendant(self, u, v):
    #     """Return the descendant vertex of halfedge ``uv``.

    #     Parameters:
    #         u (str) : The *from* vertex.
    #         v (str) : The *to* vertex.

    #     Returns:
    #         str : The key of the descendant.
    #         None : If ``uv`` has no descendant.

    #     Raises:
    #         KeyError : If the halfedge is not part of the mesh.
    #         MeshError : If something else went wrong.
    #     """
    #     fkey = self.halfedge[u][v]
    #     if fkey is not None:
    #         # the face is on the inside
    #         return self.face[fkey][v]
    #     # the face is on the outside
    #     for nbr in self.halfedge[v]:
    #         if nbr != u:
    #             if self.halfedge[v][nbr] is None:
    #                 return nbr
    #     # raise a ``MeshError`` here.
    #     return None

    # def vertex_ancestor(self, u, v):
    #     """Return the key of the vertex before u in the face that contains uv."""
    #     fkey = self.halfedge[v][u]
    #     if fkey is not None:
    #         return self.face[fkey][u]
    #     for nbr in self.halfedge[u]:
    #         if nbr != v:
    #             if self.halfedge[u][nbr] is None:
    #                 return nbr
    #     return None

    def is_vertex_on_boundary(self, key):
        for nbr in self.halfedge[key]:
            if self.halfedge[key][nbr] is None:
                return True
        return False

    def is_vertex_extraordinary(self, key, mtype=None):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    # def vertex_normal(self, key):
    #     nx = 0
    #     ny = 0
    #     nz = 0
    #     for nbr in self.halfedge[key]:
    #         fkey = self.halfedge[key][nbr]
    #         if fkey is None:
    #             continue
    #         n   = self.face_normal(fkey, unitized=False)
    #         nx += n[0]
    #         ny += n[1]
    #         nz += n[2]
    #     a = length_vector(n)
    #     return nx / a, ny / a, nz / a

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    # def point_on_edge(self, u, v, t=0.5):
    #     sp = self.vertex_coordinates(u)
    #     ep = self.vertex_coordinates(v)
    #     line = Line(sp, ep)
    #     line.scale(t)
    #     x, y, z = line.end
    #     return x, y, z

    # def edge_vector(self, u, v, unitized=False):
    #     sp  = self.vertex_coordinates(u)
    #     ep  = self.vertex_coordinates(v)
    #     vec = [ep[i] - sp[i] for i in range(3)]
    #     if not unitized:
    #         return vec
    #     vec_len = length_vector(vec)
    #     return [axis / vec_len for axis in vec]

    # --------------------------------------------------------------------------
    # face geometry
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # boundary
    # --------------------------------------------------------------------------

    def vertices_on_boundary(self, ordered=False):
        """Return the vertices on the boundary.

        Warning
        -------
        If the vertices are requested in order, and the mesh has multiple borders,
        currently only the vertices of one of the borders will be returned.

        Parameters
        ----------
        ordered : bool, optional
            If ``True``, Return the vertices in the same order as they are found on the boundary.
            Default is ``False``.

        Returns
        -------
        list
            The vertices of the boundary.

        Examples
        --------
        >>>

        """
        vertices = set()
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, face in iter(nbrs.items()):
                if face is None:
                    vertices.add(key)
                    vertices.add(nbr)

        vertices = list(vertices)

        if not ordered:
            return vertices

        key = vertices[0]
        vertices = []
        start = key

        while 1:
            for nbr, fkey in iter(self.halfedge[key].items()):
                if fkey is None:
                    vertices.append(nbr)
                    key = nbr
                    break

            if key == start:
                break

        return vertices

    def faces_on_boundary(self):
        """Return the faces on the boundary."""
        faces = {}
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, fkey in iter(nbrs.items()):
                if fkey is None:
                    faces[self.halfedge[nbr][key]] = 1
        return faces.keys()

    def edges_on_boundary(self):
        return [(u, v) for u, v in self.edges() if self.is_edge_naked(u, v)]

    # --------------------------------------------------------------------------
    # selections
    # --------------------------------------------------------------------------


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.visualization.plotters.meshplotter import MeshPlotter

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    mesh.update_default_vertex_attributes({'px': 0.0, 'py': 0.0, 'pz': 0.0})
    mesh.update_default_vertex_attributes({'is_fixed': False})

    plotter = MeshPlotter(mesh)

    print(mesh.number_of_vertices())
    print(mesh.number_of_edges())
    print(mesh.number_of_faces())

    plotter.defaults['face.facecolor'] = '#eeeeee'
    plotter.defaults['face.edgewidth'] = 0.0

    plotter.draw_vertices(
        facecolor={key: '#ff0000' for key in mesh.vertices() if mesh.vertex_degree(key) == 2}
    )

    plotter.draw_faces(text={key: key for key in mesh.faces()})
    plotter.draw_edges()

    plotter.show()
