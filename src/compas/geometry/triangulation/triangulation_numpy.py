from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

try:
    from numpy import asarray
    from scipy.spatial import Voronoi
    from scipy.spatial import Delaunay

except ImportError:
    compas.raise_if_not_ironpython()


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

    Example
    -------
    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.geometry import pointcloud_xy
        from compas.geometry import delaunay_from_points_numpy
        from compas.plotters import MeshPlotter

        points = pointcloud_xy(20, (0, 50))
        faces = delaunay_from_points_numpy(points)

        delaunay = Mesh.from_vertices_and_faces(points, faces)

        plotter = MeshPlotter(delaunay)
        plotter.draw_vertices(radius=0.1)
        plotter.draw_faces()
        plotter.show()

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
    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.geometry import closest_point_on_line_xy
        from compas.geometry import voronoi_from_points_numpy

        mesh = Mesh()

        mesh.add_vertex(x=0, y=0)
        mesh.add_vertex(x=1.5, y=0)
        mesh.add_vertex(x=1, y=1)
        mesh.add_vertex(x=0, y=2)

        mesh.add_face([0, 1, 2, 3])

        sites = mesh.get_vertices_attributes('xy')
        voronoi = voronoi_from_points_numpy(sites)

        points = []
        for xy in voronoi.vertices:
            points.append({
                'pos'       : xy,
                'radius'    : 0.02,
                'facecolor' : '#ff0000',
                'edgecolor' : '#ffffff',
            })

        lines = []
        arrows = []
        for (a, b), (c, d) in zip(voronoi.ridge_vertices, voronoi.ridge_points):
            if a > -1 and b > -1:
                lines.append({
                    'start' : voronoi.vertices[a],
                    'end'   : voronoi.vertices[b],
                    'width' : 1.0,
                    'color' : '#ff0000',
                })
            elif a == -1:
                sp = voronoi.vertices[b]
                ep = closest_point_on_line_xy(sp, (voronoi.points[c], voronoi.points[d]))
                arrows.append({
                    'start' : sp,
                    'end'   : ep,
                    'width' : 1.0,
                    'color' : '#00ff00',
                    'arrow' : 'end'
                })
            else:
                sp = voronoi.vertices[a]
                ep = closest_point_on_line_xy(sp, (voronoi.points[c], voronoi.points[d]))
                arrows.append({
                    'start' : sp,
                    'end'   : ep,
                    'width' : 1.0,
                    'color' : '#00ff00',
                    'arrow' : 'end'
                })


        plotter = MeshPlotter(mesh)
        plotter.draw_points(points)
        plotter.draw_lines(lines)
        plotter.draw_arrows(arrows)
        plotter.draw_vertices(radius=0.02)
        plotter.draw_faces()
        plotter.show()

    """
    points = asarray(points)
    voronoi = Voronoi(points)
    return voronoi


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures import Mesh
    from compas.geometry import pointcloud_xy
    from compas.geometry import delaunay_from_points_numpy
    from compas.plotters import MeshPlotter

    points = pointcloud_xy(20, (0, 50))
    faces = delaunay_from_points_numpy(points)

    delaunay = Mesh.from_vertices_and_faces(points, faces)

    plotter = MeshPlotter(delaunay, figsize=(12, 8))

    plotter.draw_vertices(radius=0.1)
    plotter.draw_faces()

    plotter.show()
