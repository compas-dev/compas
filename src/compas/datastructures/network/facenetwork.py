from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ast import literal_eval

import compas

from compas.files import OBJ

from compas.utilities import pairwise
from compas.utilities import window

from compas.geometry import normalize_vector
from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import subtract_vectors
from compas.geometry import normal_polygon
from compas.geometry import area_polygon

from compas.datastructures.network import Network

from compas.datastructures._mixins import FaceAttributesManagement
from compas.datastructures._mixins import FaceHelpers
from compas.datastructures._mixins import FaceMappings


__all__ = ['FaceNetwork']


class FaceNetwork(FaceHelpers,
                  FaceAttributesManagement,
                  FaceMappings,
                  Network):
    """Definition of a face network.

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import FaceNetwork
        from compas.topology import network_find_faces
        from compas.plotters import FaceNetworkPlotter

        network = FaceNetwork.from_obj(compas.get('lines.obj'))

        network_find_faces(network, breakpoints=network.leaves())

        plotter = FaceNetworkPlotter(network)

        plotter.draw_vertices(
            facecolor={key: '#ff0000' for key in network.leaves()},
            radius=0.2,
            text={key: key for key in network.vertices()}
        )

        plotter.draw_faces(facecolor='#eeeeee', edgecolor='#eeeeee')
        plotter.draw_edges()

        plotter.show()

    """

    def __init__(self):
        super(FaceNetwork, self).__init__()
        self._max_int_fkey = -1
        self.face = {}
        self.facedata = {}
        self.default_face_attributes = {}

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    @property
    def data(self):
        """Return a data dict of this data structure for serialisation.
        """
        data = {'attributes'  : self.attributes,
                'dva'         : self.default_vertex_attributes,
                'dea'         : self.default_edge_attributes,
                'dfa'         : self.default_face_attributes,
                'vertex'      : {},
                'edge'        : {},
                'halfedge'    : {},
                'face'        : {},
                'facedata'    : {},
                'max_int_key' : self._max_int_key,
                'max_int_fkey': self._max_int_fkey, }

        for key in self.vertex:
            rkey = repr(key)
            data['vertex'][rkey] = self.vertex[key]

        for u in self.edge:
            ru = repr(u)
            data['edge'][ru] = {}

            for v in self.edge[u]:
                rv = repr(v)
                data['edge'][ru][rv] = self.edge[u][v]

        for u in self.halfedge:
            ru = repr(u)
            data['halfedge'][ru] = {}

            for v in self.halfedge[u]:
                rv = repr(v)
                data['halfedge'][ru][rv] = repr(self.halfedge[u][v])

        for fkey in self.face:
            rfkey = repr(fkey)
            data['face'][rfkey] = [repr(key) for key in self.face[fkey]]

        for fkey in self.facedata:
            rfkey = repr(fkey)
            data['facedata'][rfkey] = self.facedata[fkey]

        return data

    @data.setter
    def data(self, data):
        attributes   = data.get('attributes') or {}
        dva          = data.get('dva') or {}
        dfa          = data.get('dfa') or {}
        dea          = data.get('dea') or {}
        vertex       = data.get('vertex') or {}
        halfedge     = data.get('halfedge') or {}
        face         = data.get('face') or {}
        facedata     = data.get('facedata') or {}
        edge         = data.get('edge') or {}
        max_int_key  = data.get('max_int_key', -1)
        max_int_fkey = data.get('max_int_fkey', -1)

        self.attributes.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_face_attributes.update(dfa)
        self.default_edge_attributes.update(dea)

        # add the vertices

        self.vertex = {literal_eval(key): attr for key, attr in iter(vertex.items())}

        # add the edges

        self.edge = {}

        for u, nbrs in iter(edge.items()):
            nbrs = nbrs or {}

            u = literal_eval(u)

            self.edge[u] = {}

            for v, attr in iter(nbrs.items()):
                attr = attr or {}

                v = literal_eval(v)

                self.edge[u][v] = attr

        # add the halfedges

        self.halfedge = {}

        for u, nbrs in iter(halfedge.items()):
            nbrs = nbrs or {}

            u = literal_eval(u)

            self.halfedge[u] = {}

            for v, fkey in iter(nbrs.items()):
                v = literal_eval(v)
                fkey = literal_eval(fkey)

                self.halfedge[u][v] = fkey

        # add the faces

        self.face = {}
        self.facedata = {}

        for fkey, vertices in iter(face.items()):
            attr = facedata.get(fkey) or {}
            fkey = literal_eval(fkey)
            vertices = [literal_eval(key) for key in vertices]

            self.face[fkey] = vertices
            self.facedata[fkey] = attr

        # set the counts

        self._max_int_key = max_int_key
        self._max_int_fkey = max_int_fkey

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath, **kwargs):
        """Initialise a network from the data described in an obj file.

        Parameters:
            filepath (str): The path to the obj file.
            kwargs (dict) : Remaining named parameters. Default is an empty :obj:`dict`.

        Returns:
            Network: A ``Network`` of class ``cls``.

        >>> network = Network.from_obj('path/to/file.obj')

        """
        network = cls()
        network.attributes.update(kwargs)
        obj = OBJ(filepath)
        vertices = obj.parser.vertices
        edges    = obj.parser.lines
        faces = obj.parser.faces
        for i, (x, y, z) in enumerate(vertices):
            network.add_vertex(i, x=x, y=y, z=z)
        for u, v in edges:
            network.add_edge(u, v)
        for face in faces:
            network.add_face(face)
        return network

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces):
        """Construct a mesh object from a list of vertices and faces.

        Parameters
        ----------
        vertices : list
            A list of vertices, represented by their XYZ coordinates.
        faces : list
            A list of faces.
            Each face is a list of indices referencing the list of vertex coordinates.

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        >>> import compas
        >>> from compas.datastructures import Mesh
        >>> vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]]
        >>> faces = [[0, 1, 2]]
        >>> mesh = Mesh.from_vertices_and_faces(vertices, faces)

        """
        network = cls()
        for x, y, z in iter(vertices):
            network.add_vertex(x=x, y=y, z=z)
        for face in iter(faces):
            keys = []
            for u, v in pairwise(face + face[0:1]):
                if not network.has_edge(u, v, directed=False):
                    u, v = network.add_edge(u, v)
                keys.append(u)
            network.add_face(keys)
        return network

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_obj(self, filepath):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def _get_face_key(self, fkey):
        if fkey is None:
            fkey = self._max_int_fkey = self._max_int_fkey + 1
        else:
            try:
                i = int(fkey)
            except (ValueError, TypeError):
                pass
            else:
                if i > self._max_int_fkey:
                    self._max_int_fkey = i
        return fkey

    def clear_facedict(self):
        del self.face
        del self.facedata
        self.face = {}
        self.facedata = {}
        self._max_int_fkey = -1

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face and specify its attributes (optional).

        Notes:
            * All faces are closed. The closing link is implied and, therefore,
              the last vertex in the list should be different from the first.
            * Building a face_adjacency list is slow, if we can't rely on the fact
              that all faces have the same cycle directions. Therefore, it is
              worth considering to ensure unified cycle directions upon addition
              of a new face.
            * A check could be added that no face is added that would leave edges
              without halfedges.
            * Adding a face does not change the layout of edges.

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

        fkey = self._get_face_key(fkey)

        self.face[fkey] = keys
        self.facedata[fkey] = attr

        halfedges = keys + keys[0:1]

        for u, v in pairwise(halfedges):
            if self.has_edge(u, v, directed=False):
                self.halfedge[u][v] = fkey
                if u not in self.halfedge[v]:
                    self.halfedge[v][u] = None

        return fkey

    def delete_face(self, fkey):
        """Delete a face from the mesh object.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Examples
        --------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.plotters import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            mesh.delete_face(12)

            plotter = MeshPlotter(mesh)
            plotter.draw_vertices()
            plotter.draw_faces()
            plotter.show()

        """
        for u, v in self.face_halfedges(fkey):
            self.halfedge[u][v] = None
            if self.halfedge[v][u] is None:
                del self.halfedge[u][v]
                del self.halfedge[v][u]
        del self.face[fkey]

    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------

    def number_of_faces(self):
        return len(list(self.faces()))

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    def faces(self, data=False):
        """Return an iterator for the faces and their attributes (optional)."""
        for fkey in self.face:
            if data:
                yield fkey, self.facedata.setdefault(fkey, self.default_face_attributes.copy())
            else:
                yield fkey

    def halfedges(self):
        edges = set()
        for fkey in self.faces():
            for u, v in self.face_halfedges(fkey):
                if (u, v) in edges or (v, u) in edges:
                    continue
                edges.add((u, v))
        return list(edges)

    def wireframe(self):
        return self.halfedges()

    # --------------------------------------------------------------------------
    # additional accessors
    # --------------------------------------------------------------------------

    def indexed_face_vertices(self):
        k_i = self.key_index()
        return [[k_i[key] for key in self.face_vertices(fkey)] for fkey in self.faces()]

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    def vertex_neighbors(self, key, ordered=False):
        """Return the neighbors of a vertex."""

        temp = list(self.halfedge[key])

        # temp = [nbr for nbr in self.halfedge[key] if self.has_edge(key, nbr, directed=False)]

        if not ordered:
            return temp

        if len(temp) == 1:
            return temp

        start = temp[0]
        for nbr in temp:
            if self.halfedge[key][nbr] is None:
                start = nbr
                break

        fkey = self.halfedge[start][key]
        nbrs = [start]
        count = 10000

        while count:
            count -= 1
            nbr = self.face_vertex_descendant(fkey, key)
            fkey = self.halfedge[nbr][key]

            if nbr == start:
                break

            nbrs.append(nbr)

            if fkey is None:
                break

        return nbrs

    def vertex_faces(self, key, ordered=False, include_None=False):
        """Return the faces connected to a vertex."""
        if not ordered:
            faces = list(self.halfedge[key].values())

        else:
            nbrs = self.vertex_neighbors(key, ordered=True)

            # if len(nbrs) == 1:
            #     nbr = nbrs[0]
            #     faces = [self.halfedge[key][nbr], self.halfedge[nbr][key]]

            # else:
            faces = [self.halfedge[key][n] for n in nbrs]

        if include_None:
            return faces

        return [fkey for fkey in faces if fkey is not None]

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    def edge_faces(self, u, v):
        return [self.halfedge[u][v], self.halfedge[v][u]]

    def is_edge_naked(self, u, v):
        return self.halfedge[u][v] is None or self.halfedge[v][u] is None

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    def face_vertices(self, fkey, ordered=True):
        """Return the vertices of the face."""
        return list(self.face[fkey])

    def face_halfedges(self, fkey):
        """Return the halfedges of a face."""
        vertices = self.face_vertices(fkey)
        return pairwise(vertices + vertices[0:1])

    def face_edges(self, fkey):
        """Return the edges corresponding to the halfedges of a face."""
        edges = []
        for u, v in self.face_halfedges(fkey):
            if v in self.edge[u]:
                edges.append((u, v))
            else:
                edges.append((v, u))
        return edges

    def face_corners(self, fkey):
        vertices = self.face_vertices(fkey)
        return window(vertices + vertices[0:2], 3)

    def face_neighbors(self, fkey):
        """Return the neighbors of a face across its edges."""
        nbrs = []
        for u, v in self.face_halfedges(fkey):
            nbr = self.halfedge[v][u]
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def face_vertex_neighbors(self, fkey):
        """Return the neighbors of a face across its corners."""
        nbrs = []
        for u, v in self.face_halfedges(fkey):
            nbr = self.halfedge[v][u]
            if nbr is not None:
                w = self.face_vertex_descendant(fkey, u)
                nbrs.append(self.halfedge[w][u])
        return nbrs

    def face_neighborhood(self, fkey):
        """Return the neighbors of a face across both edges and corners."""
        nbrs = []
        for u, v in self.face_halfedges(fkey):
            nbr = self.halfedge[v][u]
            if nbr is not None:
                nbrs.append(nbr)
                w = self.face_vertex_descendant(fkey, u)
                nbrs.append(self.halfedge[w][u])
        return nbrs

    def face_vertex_ancestor(self, fkey, key):
        """Return the vertex before the specified vertex in a specific face."""
        i = self.face[fkey].index(key)
        return self.face[fkey][i - 1]

    def face_vertex_descendant(self, fkey, key):
        """Return the vertex after the specified vertex in a specific face."""
        if self.face[fkey][-1] == key:
            return self.face[fkey][0]
        i = self.face[fkey].index(key)
        return self.face[fkey][i + 1]

    def face_adjacency(self):
        # this function does not actually use any of the topological information
        # provided by the halfedges
        # it is used for unifying face cycles
        # so the premise is that halfedge data is not valid/reliable
        from scipy.spatial import cKDTree

        fkey_index = {fkey: index for index, fkey in self.faces_enum()}
        index_fkey = dict(self.faces_enum())
        points = [self.face_centroid(fkey) for fkey in self.faces()]

        tree = cKDTree(points)

        _, closest = tree.query(points, k=10, n_jobs=-1)

        adjacency = {}
        for fkey in self.face:
            nbrs  = []
            index = fkey_index[fkey]
            nnbrs = closest[index]
            found = set()
            for u, v in iter(self.face[fkey].items()):
                for index in nnbrs:
                    nbr = index_fkey[index]
                    if nbr == fkey:
                        continue
                    if nbr in found:
                        continue
                    if v in self.face[nbr] and u == self.face[nbr][v]:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break
                    if u in self.face[nbr] and v == self.face[nbr][u]:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break
            adjacency[fkey] = nbrs
        return adjacency

    # def face_tree(self, root, algo=network_bfs):
    #     return algo(self.face_adjacency(), root)

    def face_adjacency_edge(self, f1, f2):
        for u, v in self.face_halfedges(f1):
            if self.halfedge[v][u] == f2:
                if v in self.edge[u]:
                    return u, v
                return v, u

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_area(self, key):
        """Return the tributary area of a vertex."""
        area = 0

        p0 = self.vertex_coordinates(key)

        for nbr in self.halfedge[key]:
            p1 = self.vertex_coordinates(nbr)
            v1 = subtract_vectors(p1, p0)

            fkey = self.halfedge[key][nbr]
            if fkey is not None:
                p2 = self.face_centroid(fkey)
                v2 = subtract_vectors(p2, p0)
                area += length_vector(cross_vectors(v1, v2))

            fkey = self.halfedge[nbr][key]
            if fkey is not None:
                p3 = self.face_centroid(fkey)
                v3 = subtract_vectors(p3, p0)
                area += length_vector(cross_vectors(v1, v3))

        return 0.25 * area

    # centroid_points is in fact an averaging of vectors
    # name it as such
    def vertex_normal(self, key):
        """Return the normal vector at the vertex as the weighted average of the
        normals of the neighboring faces."""
        vectors = [self.face_normal(fkey) for fkey in self.vertex_faces(key) if fkey is not None]
        return normalize_vector(centroid_points(vectors))

    # --------------------------------------------------------------------------
    # face geometry
    # --------------------------------------------------------------------------

    def face_coordinates(self, fkey, axes='xyz'):
        """Return the coordinates of the vertices of a face."""
        return [self.vertex_coordinates(key, axes=axes) for key in self.face_vertices(fkey)]

    def face_normal(self, fkey, normalized=True):
        """Return the normal of a face."""
        return normal_polygon(self.face_coordinates(fkey), normalized=normalized)

    def face_centroid(self, fkey):
        """Return the location of the centroid of a face."""
        return centroid_points(self.face_coordinates(fkey))

    def face_center(self, fkey):
        """Return the location of the center of mass of a face."""
        return center_of_mass_polygon(self.face_coordinates(fkey))

    def face_area(self, fkey):
        """Return the area of a face."""
        return area_polygon(self.face_coordinates(fkey))

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
        boundary = []
        for fkey in self.faces():
            vertices = self.face_vertices(fkey)
            for u, v in pairwise(vertices + vertices[0:1]):
                if not self.has_edge(u, v, directed=False):
                    boundary.append(fkey)
                    break
        return boundary

    def edges_on_boundary(self):
        edges = []
        for fkey in self.faces_on_boundary():
            vertices = self.face_vertices(fkey)
            for u, v in pairwise(vertices + vertices[0:1]):
                if self.has_edge(u, v):
                    edges.append((u, v))
                elif self.has_edge(v, u):
                    edges.append((v, u))
        return edges


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.datastructures import FaceNetwork
    from compas.topology import network_find_faces
    from compas.plotters import FaceNetworkPlotter

    network = FaceNetwork.from_obj(compas.get('lines.obj'))

    network_find_faces(network, breakpoints=network.leaves())

    plotter = FaceNetworkPlotter(network, figsize=(10, 7))

    plotter.defaults['vertex.fontsize'] = 8.0

    plotter.draw_vertices(
        facecolor={key: '#ff0000' for key in network.leaves()},
        radius=0.2,
        text={key: key for key in network.vertices()}
    )

    plotter.draw_faces(text={key: str(key) for key in network.faces()}, facecolor='#eeeeee', edgecolor='#eeeeee')
    plotter.draw_edges(color={uv: '#ff0000' for uv in network.edges_on_boundary()})

    plotter.show()
