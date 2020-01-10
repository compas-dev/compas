from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities import pairwise
from compas.datastructures.mesh.core import BaseMesh


__all__ = ['TriMesh']


# inherit
# - data
# - from_data/to_data
# - from_json/to_json
# - from_pickle/to_pickle
# - from_obj
# - from_ply
# - from_stl
# - from_off
# - from_vertices_and_faces
# - from_points
# - copy
# -


class TriMesh(BaseMesh):

    def __init__(self):
        super(TriMesh, self).__init__()
        self._max_vertex_key = -1
        self._max_face_key = -1

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        if key is None:
            key = self._max_vertex_key = self._max_vertex_key + 1
        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
        attr = attr_dict or {}
        attr.update(kwattr)
        self.vertex[key].update(attr)
        return key

    def add_face(self, vertices, attr_dict=None, **kwattr):
        if len(vertices) != 3:
            return
        key = self._max_face_key = self._max_face_key + 1
        attr = attr_dict or {}
        attr.update(kwattr)
        self.face[key] = vertices
        self.facedata[key] = attr
        for u, v in pairwise(vertices + vertices[:1]):
            self.halfedge[u][v] = key
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None
        return key

    def delete_vertex(self, key):
        halfedge = self.halfedge[key]
        nbrs = list(halfedge)
        faces = [halfedge[nbr] for nbr in nbrs if halfedge[nbr] is not None]
        for fkey in faces:
            vertices = self.face[fkey]
            for u, v in pairwise(vertices + vertices[:1]):
                self.halfedge[u][v] = None
            del self.face[fkey]
        for nbr in nbrs:
            del self.halfedge[nbr][key]
        for nbr in nbrs:
            for n in list(self.halfedge[nbr]):
                if self.halfedge[nbr][n] is None and self.halfedge[n][nbr] is None:
                    del self.halfedge[nbr][n]
                    del self.halfedge[n][nbr]
        del self.halfedge[key]
        del self.vertex[key]

    def delete_face(self, fkey):
        pass

    def vertices(self, data=False):
        for key in self.vertex:
            if not data:
                yield key
            else:
                yield key, self.vertex_attributes(key)

    def faces(self, data=False):
        for key in self.face:
            if not data:
                yield key
            else:
                yield key, self.face_attributes(key)

    def edges(self, data=False):
        seen = set()
        for u in self.halfedge:
            for v in self.halfedge[u]:
                key = u, v
                ikey = v, u
                if key in seen or ikey in seen:
                    continue
                seen.add(key)
                seen.add(ikey)
                if not data:
                    yield key
                else:
                    yield key, self.edge_attributes(key)

    def vertex_attribute(self, key, name, value=None):
        if key not in self.vertex:
            return None
        if value is not None:
            self.vertex[key][name] = value
            return
        if name in self.vertex[key]:
            return self.vertex[key][name]
        else:
            if name in self.default_vertex_attributes:
                return self.default_vertex_attributes[name]

    def vertex_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        names : list, optional
            A list of attribute names.
        values : list, optional
            A list of attribute values.

        Returns
        -------
        None
            If the vertex does not exist.
        None
            If the parameter ``values`` is not empty.
        dict
            If the parameter ``names`` is empty,
            the function returns a dictionary of all attribute name-value pairs of the vertex.
        list
            If the parameter ``names`` is not empty,
            the function returns a list of the values corresponding to the provided attribute names.

        Notes
        -----
        This function can be used as a "setter" as wel as a "getter".
        If no value is provided for the parameter ```values``, the function behaves a "getter".

        """
        if key not in self.vertex:
            return None
        if values:
            # use it as a setter
            for name, value in zip(names, values):
                self.vertex[key][name] = value
            return
        # use it as a getter
        if not names:
            attr = {}
            for name in self.default_vertex_attributes:
                attr[name] = self.default_vertex_attributes[name]
            for name in self.vertex[key]:
                attr[name] = self.vertex[key][name]
            return attr
        values = []
        for name in names:
            if name in self.vertex[key]:
                values.append(self.vertex[key][name])
            elif name in self.default_vertex_attributes:
                values.append(self.default_vertex_attributes[name])
            else:
                values.append(None)
        return values

    def vertices_attribute(self, keys, name, value=None):
        if value:
            for key in keys:
                self.vertex_attribute(key, name, value)
            return
        return [self.vertex_attribute(key, name) for key in keys]

    def vertices_attributes(self, keys, names=None, values=None):
        if values:
            for key in keys:
                self.vertex_attributes(key, names, values)
            return
        return [self.vertex_attributes(key, names) for key in keys]

    def edge_attribute(self, key, name, value=None):
        u, v = key
        if u not in self.halfedge or v not in self.halfedge[u]:
            return
        if value is not None:
            if (u, v) not in self.edgedata:
                self.edgedata[u, v] = {}
            if (v, u) not in self.edgedata:
                self.edgedata[v, u] = {}
            self.edgedata[u, v][name] = self.edgedata[v, u][name] = value
            return
        if (u, v) in self.edgedata:
            if name in self.edgedata[u, v]:
                return self.edgedata[u, v][name]
        if name in self.default_edge_attributes:
            return self.default_edge_attributes[name]
        return

    def edge_attributes(self, key, names=None, values=None):
        u, v = key
        if u not in self.halfedge or v not in self.halfedge[u]:
            return
        if values:
            # use it as a setter
            for name, value in zip(names, values):
                self.edge_attribute(key, name, value)
            return
        # use it as a getter
        if not names:
            # get the entire attribute dict
            attr = {}
            for name in self.default_edge_attributes:
                attr[name] = self.default_edge_attributes[name]
            if key in self.edgedata:
                for name in self.edgedata[key]:
                    attr[name] = self.edgedata[key][name]
            return attr
        # get only the values of the named attributes
        values = []
        for name in names:
            if key in self.edgedata:
                if name in self.edgedata[key]:
                    values.append(self.edgedata[key][name])
                elif name in self.default_edge_attributes:
                    values.append(self.default_edge_attributes[name])
                else:
                    values.append(None)
            else:
                if name in self.default_edge_attributes:
                    values.append(self.default_edge_attributes[name])
                else:
                    values.append(None)
        return values


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    import time

    t0 = time.perf_counter()

    trimesh = TriMesh()
    trimesh.default_vertex_attributes.update({'a': 1, 'b': 2})

    a = trimesh.add_vertex(x=0.0, y=0.0, z=0.0)
    b = trimesh.add_vertex(x=1.0, y=0.0, z=0.0)
    c = trimesh.add_vertex(x=1.0, y=1.0, z=0.0)
    d = trimesh.add_vertex(x=0.0, y=1.0, z=0.0)

    trimesh.add_face([a, b, c])
    trimesh.add_face([a, c, d])

    # trimesh.delete_vertex(b)
    # print(trimesh.summary())

    value = trimesh.vertex_attribute(a, 'x')
    # print(value)

    for key, attr in trimesh.vertices(True):
        print(key, attr)

    for key, attr in trimesh.edges(True):
        print(key, attr)

    # t1 = time.perf_counter()
    # print(t1 - t0)
