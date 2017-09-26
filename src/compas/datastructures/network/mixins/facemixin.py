""""""

from compas.utilities import pairwise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


class FaceMixin(object):
    """"""

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
            if self.has_edge(u, v, directed=False):
                self.halfedge[u][v] = fkey
                if u not in self.halfedge[v]:
                    self.halfedge[v][u] = None

        return fkey


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
