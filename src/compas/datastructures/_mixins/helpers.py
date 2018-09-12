from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from random import sample
from random import choice


__all__ = [
    'VertexHelpers',
    'EdgeHelpers',
    'FaceHelpers',
]


class VertexHelpers(object):

    def get_any_vertex(self):
        """Get the identifier of a random vertex.

        Returns
        -------
        hashable
            The identifier of the vertex.

        """
        return self.get_any_vertices(1)[0]

    def get_any_vertices(self, n, exclude_leaves=False):
        """Get a list of identifiers of a random set of n vertices.

        Parameters
        ----------
        n : int
            The number of random vertices.
        exclude_leaves : bool (False)
            Exclude the leaves (vertices with only one connected edge) from the set.
            Default is to include the leaves.

        Returns
        -------
        list
            The identifiers of the vertices.

        """
        if exclude_leaves:
            vertices = set(self.vertices()) - set(self.leaves())
        else:
            vertices = self.vertices()
        return sample(list(vertices), n)

    def vertex_name(self, key):
        """Get the name of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        str
            The name of the vertex in the following format ``<name>.vertex.<key>``,
            with *name* the name of the datastructure.

        """
        return '{}.vertex.{}'.format(self.name, key)

    def vertex_label_name(self, key):
        """Get the name of a vertex label.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        str
            The name of the label in the following format ``<name>.vertex.label.<key>``,
            with *name* the name of the datastructure.

        """
        return '{0}.vertex.label.{1}'.format(self.name, key)


class EdgeHelpers(object):

    def get_any_edge(self):
        """Get the identifier of a random edge.

        Returns
        -------
        tuple
            The identifier of the edge in the form of a pair of vertex identifiers.

        """
        return choice(list(self.edges()))

    def edge_name(self, u, v):
        """Get the name of an edge.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex.
        v : hashable
            The identifier of the second vertex.

        Returns
        -------
        str
            The name of the edge in the following format ``<name>.edge.<u>-<v>``,
            with *name* the name of the datastructure.

        """
        return '{0}.edge.{1}-{2}'.format(self.name, u, v)

    def edge_label_name(self, u, v):
        """Get the name of an edge label.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex.
        v : hashable
            The identifier of the second vertex.

        Returns
        -------
        str
            The name of the label in the following format ``<name>.edge.label.<u>-<v>``,
            with *name* the name of the datastructure.

        """
        return '{0}.edge.label.{1}-{2}'.format(self.name, u, v)


class FaceHelpers(object):

    def get_any_face(self):
        """Get the identifier of a random face.

        Returns
        -------
        hashable
            The identifier of the face.

        """
        return choice(list(self.faces()))

    def get_any_face_vertex(self, fkey):
        """Get the identifier of a random vertex of a specific face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Returns
        -------
        hashable
            The identifier of the vertex.

        """
        return self.face_vertices(fkey)[0]

    def face_name(self, fkey):
        """Get the name of a face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Returns
        -------
        str
            The name of the face in the following format ``<name>.face.<key>``,
            with *name* the name of the datastructure.

        """
        return '{0}.face.{1}'.format(self.name, fkey)

    def face_label_name(self, fkey):
        """Get the name of a face label.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Returns
        -------
        str
            The name of the label in the following format ``<name>.face.label.<key>``,
            with *name* the name of the datastructure.

        """
        return '{0}.face.label.{1}'.format(self.name, fkey)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
