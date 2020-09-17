from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import asarray
from scipy.spatial import Voronoi
from scipy.spatial import Delaunay


__all__ = [
    'delaunay_from_points_numpy',
    'voronoi_from_points_numpy',
]


def delaunay_from_points_numpy(points):
    """Computes the delaunay triangulation for a list of points using Numpy.

    Parameters
    ----------
    points : sequence of tuple
        XYZ coordinates of the original points.
    boundary : sequence of tuples
        list of ordered points describing the outer boundary (optional)
    holes : list of sequences of tuples
        list of polygons (ordered points describing internal holes (optional)

    Returns
    -------
    list
        The faces of the triangulation.
        Each face is a triplet of indices referring to the list of point coordinates.

    Examples
    --------
    >>>

    """
    xyz = asarray(points)
    d = Delaunay(xyz[:, 0:2])
    return d.simplices


def voronoi_from_points_numpy(points):
    """Generate a voronoi diagram from a set of points.

    Parameters
    ----------
    points : list of list of float
        XYZ coordinates of the voronoi sites.

    Returns
    -------

    Examples
    --------
    >>>

    """
    points = asarray(points)
    voronoi = Voronoi(points)
    return voronoi


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # from compas.datastructures import Mesh
    # from compas.geometry import pointcloud_xy
    # from compas_plotters import MeshPlotter

    # points = pointcloud_xy(10, (0, 50))
    # faces = delaunay_from_points_numpy(points)

    # delaunay = Mesh.from_vertices_and_faces(points, faces)

    # plotter = MeshPlotter(delaunay, figsize=(8, 5))
    # plotter.draw_vertices(radius=0.1)
    # plotter.draw_faces()
    # plotter.show()

    import doctest
    doctest.testmod(globs=globals())
