from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import distance_point_point
from compas.geometry import midpoint_line
from compas.geometry import normalize_vector
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors


__all__ = [
    'VertexGeometry',
    'EdgeGeometry',
    'FaceGeometry',
]


class VertexGeometry(object):
    pass


class EdgeGeometry(object):

    def edge_coordinates(self, u, v, axes='xyz'):
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        u : hashable
            The key of the start vertex.
        v : hashable
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
        u : hashable
            The key of the start vertex.
        v : hashable
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
        u : hashable
            The key of the start vertex.
        v : hashable
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
        u : hashable
            The key of the start vertex.
        v : hashable
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

    def edge_midpoint(self, u, v):
        """Return the location of the midpoint of an edge.

        Parameters
        ----------
        u : hashable
            The key of the start vertex.
        v : hashable
            The key of the end vertex.

        Returns
        -------
        list
            The XYZ coordinates of the midpoint.

        """
        a, b = self.edge_coordinates(u, v)
        return midpoint_line((a, b))

    def edge_direction(self, u, v):
        """Return the direction vector of an edge.

        Parameters
        ----------
        u : hashable
            The key of the start vertex.
        v : hashable
            The key of the end vertex.

        Returns
        -------
        list
            The direction vector of the edge.

        """
        return normalize_vector(self.edge_vector(u, v))


class FaceGeometry(object):
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
