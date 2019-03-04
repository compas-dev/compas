from numpy import asarray
from numpy import argmax
from numpy import argmin
from numpy import zeros

import matplotlib
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from compas.plotters.core.utilities import assert_axes_dimension


__all__ = [
    'Axes2D', 'Axes3D', 'Bounds', 'Box', 'Cloud2D', 'Cloud3D', 'Hull',
]


class Axes2D(object):
    """Definition of a 2D Axes object.

    Parameters
    ----------
    origin : tuple or list
        X and Y coordinates for the origin.
    vectors : list
        The X and Y axes.

    Attributes
    ----------
    origin : tuple or list
        X and Y coordinates for the origin.
    vectors : list
        The X and Y axes.

    """

    def __init__(self, origin, vectors):
        """Initialises the Axes2D object"""
        self.origin = asarray(origin)
        self.vectors = asarray(vectors)

    def plot(self, axes):
        """Plots the axes object

        Parameters
        ----------
        axes : object
            The matplotlib axes object.

        """
        assert_axes_dimension(axes, 2)
        o = self.origin
        xy = self.vectors
        axes.plot(
            [o[0, 0], o[0, 0] + xy[0, 0]],
            [o[0, 1], o[0, 1] + xy[0, 1]],
            'r-'
        )
        axes.plot(
            [o[0, 0], o[0, 0] + xy[1, 0]],
            [o[0, 1], o[0, 1] + xy[1, 1]],
            'g-'
        )


class Axes3D(object):
    """Definition of a 3D Axes object.

    Parameters
    ----------
    origin : tuple or list
        X, Y and Z coordinates for the origin.
    vectors : list
        The X, Y and Z axes.

    Attributes
    ----------
    origin : tuple or list
        X, Y and Z coordinates for the origin.
    vectors : list
        The X, Y and Z axes.

    """

    def __init__(self, origin, vectors, colors=None):
        """Initialises the Axes3D object"""
        self.origin = asarray(origin)
        self.vectors = asarray(vectors)
        if not colors:
            colors = ('r', 'g', 'b')
        self.colors = colors

    def plot(self, axes):
        """Plots the axes object

        Parameters
        ----------
        axes : object
            The matplotlib axes object.
        """
        assert_axes_dimension(axes, 3)
        o = self.origin
        xyz = self.vectors
        axes.plot(
            [o[0, 0], o[0, 0] + xyz[0, 0]],
            [o[0, 1], o[0, 1] + xyz[0, 1]],
            [o[0, 2], o[0, 2] + xyz[0, 2]],
            '{0}-'.format(self.colors[0]),
            linewidth=3
        )
        axes.plot(
            [o[0, 0], o[0, 0] + xyz[1, 0]],
            [o[0, 1], o[0, 1] + xyz[1, 1]],
            [o[0, 2], o[0, 2] + xyz[1, 2]],
            '{0}-'.format(self.colors[1]),
            linewidth=3
        )
        axes.plot(
            [o[0, 0], o[0, 0] + xyz[2, 0]],
            [o[0, 1], o[0, 1] + xyz[2, 1]],
            [o[0, 2], o[0, 2] + xyz[2, 2]],
            '{0}-'.format(self.colors[2]),
            linewidth=3
        )


class Bounds(object):
    """"""

    def __init__(self, points):
        self.points = asarray(points)

    def plot(self, axes):
        assert_axes_dimension(axes, 3)
        xmin, ymin, zmin = argmin(self.points, axis=0)
        xmax, ymax, zmax = argmax(self.points, axis=0)
        xspan = self.points[xmax, 0] - self.points[xmin, 0]
        yspan = self.points[ymax, 1] - self.points[ymin, 1]
        zspan = self.points[zmax, 2] - self.points[zmin, 2]
        span = max(xspan, yspan, zspan)
        axes.plot([self.points[xmin, 0]], [self.points[ymin, 1]], [self.points[zmin, 2]], 'w')
        axes.plot([self.points[xmin, 0] + span], [self.points[ymin, 1] + span], [self.points[zmin, 2] + span], 'w')


class Box(object):
    """"""

    def __init__(self, corners):
        self.corners = corners
        self.faces = [[0, 1, 2, 3], [4, 7, 6, 5], [1, 5, 6, 2], [0, 4, 5, 1], [0, 3, 7, 4], [2, 6, 7, 3]]

    def plot(self, axes):
        assert_axes_dimension(axes, 3)
        rec = [[self.corners[index] for index in face] for face in self.faces]
        rec_coll = Poly3DCollection(rec)
        rec_coll.set_facecolors([(1.0, 0.0, 0.0) for face in self.faces])
        rec_coll.set_alpha(0.2)
        axes.add_collection3d(rec_coll)


class Cloud2D(object):
    """"""

    def __init__(self, cloud):
        cloud = asarray(cloud)
        cols = min(2, cloud.shape[1])
        self.cloud = zeros((cloud.shape[0], 2))
        self.cloud[:, :cols] = cloud[:, :cols]

    def plot(self, axes):
        x = self.cloud[:, 0]
        y = self.cloud[:, 1]
        axes.plot(x, y, 'o', color=(1.0, 1.0, 1.0))


class Cloud3D(object):
    """"""

    def __init__(self, cloud):
        cloud = asarray(cloud)
        cols = min(3, cloud.shape[1])
        self.cloud = zeros((cloud.shape[0], 3))
        self.cloud[:, :cols] = cloud[:, :cols]

    def plot(self, axes):
        x = self.cloud[:, 0]
        y = self.cloud[:, 1]
        z = self.cloud[:, 2]
        axes.plot(x, y, z, 'o', color=(0.7, 0.7, 0.7))


class Hull(object):
    """"""
    def __init__(self, hull):
        self.vertices = hull.points
        self.faces = hull.simplices

    def plot(self, axes):
        tri = [[self.vertices[index] for index in face] for face in self.faces]
        tri_coll = Poly3DCollection(tri)
        tri_coll.set_facecolors([(0.0, 1.0, 0.0) for face in self.faces])
        axes.add_collection3d(tri_coll)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
