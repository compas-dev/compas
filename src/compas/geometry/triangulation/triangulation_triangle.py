from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from triangle import triangulate

except ImportError:
    pass

from compas.utilities import pairwise


__all__ = [
    'delaunay_triangle',
    'constrained_delaunay_triangle',
    'conforming_delaunay_triangle'
]


def delaunay_triangle(points):
    """Construct a Delaunay triangulation of set of vertices.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points to triangulate.

    Returns
    -------
    list
        The faces of the triangulation.

    References
    ----------
    https://www.cs.cmu.edu/~quake/triangle.delaunay.html

    Examples
    --------
    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.geometry import delaunay_triangle
        from compas.plotters import MeshPlotter

        points = [
            [2.994817685045075, 10.855606612493078, 0.0],
            [4.185204599300653, 9.527867361977242, 0.0],
            [4.414125159734419, 10.718254276232818, 0.0],
            [5.925000858597267, 9.344730913630228, 0.0],
            [8.900968144236211, 10.809822500406325, 0.0],
            [9.496161601363999, 8.566401008155429, 0.0],
            [7.710581229980631, 7.9254234389408875, 0.0],
            [7.847933566240888, 6.414547740078039, 0.0],
            [3.9104999267801377, 4.9036720412151915, 0.0],
            [5.2909301507195865, 6.342692886748852, 0.0]
        ]

        faces = delaunay_triangle(points)

        mesh = Mesh.from_vertices_and_faces(points, faces)

        plotter = MeshPlotter(mesh)
        plotter.draw_faces()
        plotter.draw_vertices(text='key')
        plotter.show()

    """
    data = {'vertices': [point[0:2] for point in points]}
    result = triangulate(data)
    faces = result['triangles']
    return faces


def constrained_delaunay_triangle(points, segments):
    """Construct a Delaunay triangulation of set of vertices, constrained to the specified segments.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points to triangulate.
    segments : list
        A list of point index pairs, to indicate which straight line segments
        should be included in the triangulation.

    Returns
    -------
    list
        The faces of the triangulation.

    Notes
    -----
    Concavities will be removed automatically.
    Therefore, the boundary of the triangulation should be included in the specification
    of segments to avoid unexpected results.

    No additional vertices (Steiner points) will be inserted.
    Therefore not all faces of the triangulation will be Delaunay.

    References
    ----------
    https://www.cs.cmu.edu/~quake/triangle.delaunay.html

    Examples
    --------
    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.geometry import constrained_delaunay_triangle
        from compas.plotters import MeshPlotter

        points = [
            [2.994817685045075, 10.855606612493078, 0.0],
            [4.185204599300653, 9.527867361977242, 0.0],
            [4.414125159734419, 10.718254276232818, 0.0],
            [5.925000858597267, 9.344730913630228, 0.0],
            [8.900968144236211, 10.809822500406325, 0.0],
            [9.496161601363999, 8.566401008155429, 0.0],
            [7.710581229980631, 7.9254234389408875, 0.0],
            [7.847933566240888, 6.414547740078039, 0.0],
            [3.9104999267801377, 4.9036720412151915, 0.0],
            [5.2909301507195865, 6.342692886748852, 0.0]
        ]
        segments = list(pairwise(list(range(len(points))) + [0]))

        faces = constrained_delaunay_triangle(points, segments)

        mesh = Mesh.from_vertices_and_faces(points, faces)

        plotter = MeshPlotter(mesh)
        plotter.draw_faces()
        plotter.draw_vertices(text='key')
        plotter.show()

    """
    data = {'vertices': [point[0:2] for point in points], 'segments': segments}
    result = triangulate(data, opts='p')
    faces = result['triangles']
    return faces


def conforming_delaunay_triangle(points, segments):
    """Construct a Delaunay triangulation of set of vertices,
    constrained to the specified segments,
    and with as many Steiner points inserted as necessary to make sure all faces
    of the triangulation are Delaunay.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points to triangulate.
    segments : list
        A list of point index pairs, to indicate which straight line segments
        should be included in the triangulation.

    Returns
    -------
    tuple
        The vertices of the triangulation and the faces of the triangulation.

    Notes
    -----
    Concavities will be removed automatically.
    Therefore, the boundary of the triangulation should be included in the specification
    of segments to avoid unexpected results.

    References
    ----------
    https://www.cs.cmu.edu/~quake/triangle.delaunay.html

    Examples
    --------
    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.geometry import conforming_delaunay_triangle
        from compas.plotters import MeshPlotter

        points = [
            [2.994817685045075, 10.855606612493078, 0.0],
            [4.185204599300653, 9.527867361977242, 0.0],
            [4.414125159734419, 10.718254276232818, 0.0],
            [5.925000858597267, 9.344730913630228, 0.0],
            [8.900968144236211, 10.809822500406325, 0.0],
            [9.496161601363999, 8.566401008155429, 0.0],
            [7.710581229980631, 7.9254234389408875, 0.0],
            [7.847933566240888, 6.414547740078039, 0.0],
            [3.9104999267801377, 4.9036720412151915, 0.0],
            [5.2909301507195865, 6.342692886748852, 0.0]
        ]
        segments = list(pairwise(list(range(len(points))) + [0]))

        vertices, faces = conforming_delaunay_triangle(points, segments)

        mesh = Mesh.from_vertices_and_faces(vertices, faces)

        plotter = MeshPlotter(mesh)
        plotter.draw_faces()
        plotter.draw_vertices(text='key')
        plotter.show()

    """
    data = {'vertices': [point[0:2] for point in points], 'segments': segments}
    result = triangulate(data, opts='pq0D')
    vertices = [[x, y, 0.0] for x, y in result['vertices']]
    faces = result['triangles']
    return vertices, faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.datastructures import Mesh
    from compas.geometry import conforming_delaunay_triangle
    from compas.plotters import MeshPlotter

    points = [
        [2.994817685045075, 10.855606612493078, 0.0],
        [4.185204599300653, 9.527867361977242, 0.0],
        [4.414125159734419, 10.718254276232818, 0.0],
        [5.925000858597267, 9.344730913630228, 0.0],
        [8.900968144236211, 10.809822500406325, 0.0],
        [9.496161601363999, 8.566401008155429, 0.0],
        [7.710581229980631, 7.9254234389408875, 0.0],
        [7.847933566240888, 6.414547740078039, 0.0],
        [3.9104999267801377, 4.9036720412151915, 0.0],
        [5.2909301507195865, 6.342692886748852, 0.0]
    ]
    segments = list(pairwise(list(range(len(points))) + [0]))

    vertices, faces = conforming_delaunay_triangle(points, segments)

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    plotter = MeshPlotter(mesh)
    plotter.draw_faces()
    plotter.draw_vertices(text='key')
    plotter.show()
