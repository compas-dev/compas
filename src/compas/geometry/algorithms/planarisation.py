from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import project_points_plane
from compas.geometry import centroid_points

from compas.geometry import distance_point_point
from compas.geometry import distance_line_line

from compas.geometry.algorithms.bestfit import bestfit_plane

from compas.utilities import window


__all__ = [
    'flatness',
    'planarize_faces',
    'mesh_flatness',
    'mesh_planarize_faces',
]


def flatness(vertices, faces, maxdev=0.02):
    """Compute mesh flatness per face.

    Parameters
    ----------
    vertices : list
        The vertex coordinates.
    faces : list
        The face vertices.
    maxdev : float, optional
        A maximum value for the allowed deviation from flatness.
        Default is ``0.02``.

    Returns
    -------
    dict
        For each face, a deviation from *flatness*.

    Notes
    -----
    The "flatness" of a face is expressed as the ratio of the distance between
    the diagonals to the average edge length. For the fabrication of glass panels,
    for example, ``0.02`` could be a reasonable maximum value.

    Warning
    -------
    This function only works as expected for quadrilateral faces.

    See Also
    --------
    * :func:`compas.geometry.mesh_flatness`

    """
    dev = []
    for face in faces:
        points = [vertices[index] for index in face]
        lengths = [distance_point_point(a, b) for a, b in window(points + points[0:1], 2)]
        l = sum(lengths) / len(lengths)
        d = distance_line_line((points[0], points[2]), (points[1], points[3]))
        dev.append((d / l) / maxdev)
    return dev


def planarize_faces(vertices,
                    faces,
                    fixed=None,
                    kmax=100,
                    callback=None,
                    callback_args=None):
    """Planarise a set of connected faces.

    Planarisation is implemented as a two-step iterative procedure. At every
    iteration, faces are first individually projected to their best-fit plane,
    and then the vertices are projected to the centroid of the disconnected
    corners of the faces.

    Parameters
    ----------
    vertices : list
        The vertex coordinates.
    faces : list
        The vertex indices per face.
    fixed : list, optional [None]
        A list of fixed vertices.
    kmax : int, optional [100]
        The number of iterations.
    callback : callable, optional [None]
        A user-defined callback that is called after every iteration.
    callback_args : list, optional [None]
        A list of arguments to be passed to the callback function.

    See Also
    --------
    * :func:`compas.geometry.mesh_planarize_faces`
    * :func:`compas.geometry.mesh_planarize_faces_shapeop`

    """
    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):

        positions = [[] for _ in range(len(vertices))]

        for face in iter(faces):
            points = [vertices[index] for index in face]
            plane = bestfit_plane(points)
            projections = project_points_plane(points, plane)

            for i, index in enumerate(face):
                positions[index].append(projections[i])

        for index, vertex in enumerate(vertices):
            if index in fixed:
                continue

            x, y, z = centroid_points(positions[index])
            vertex[0] = x
            vertex[1] = y
            vertex[2] = z

        if callback:
            callback(k, callback_args)


# ==============================================================================
# mesh variations
# ==============================================================================


def mesh_flatness(mesh, maxdev=1.0):
    """Compute mesh flatness per face.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    maxdev : float, optional
        A maximum value for the allowed deviation from flatness.
        Default is ``1.0``.

    Returns
    -------
    dict
        For each face, a deviation from *flatness*.

    Notes
    -----
    The "flatness" of a face is expressed as the ratio of the distance between
    the diagonals to the average edge length. For the fabrication of glass panels,
    for example, ``0.02`` could be a reasonable maximum value.

    Warning
    -------
    This function only works as expected for quadrilateral faces.

    See Also
    --------
    * :func:`compas.geometry.flatness`

    """
    dev = []
    for fkey in mesh.faces():
        points = mesh.face_coordinates(fkey)
        lengths = [distance_point_point(a, b) for a, b in window(points + points[0:1], 2)]
        l = sum(lengths) / len(lengths)
        d = distance_line_line((points[0], points[2]), (points[1], points[3]))
        dev.append((d / l) / maxdev)
    return dev


def mesh_planarize_faces(mesh, fixed=None, kmax=100, callback=None, callback_args=None):
    """Planarise a set of connected faces.

    Planarisation is implemented as a two-step iterative procedure. At every
    iteration, faces are first individually projected to their best-fit plane,
    and then the vertices are projected to the centroid of the disconnected
    corners of the faces.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fixed : list, optional [None]
        A list of fixed vertices.
    kmax : int, optional [100]
        The number of iterations.
    d : float, optional [1.0]
        A damping factor.
    callback : callable, optional [None]
        A user-defined callback that is called after every iteration.
    callback_args : list, optional [None]
        A list of arguments to be passed to the callback function.

    Returns
    -------
    None

    See Also
    --------
    * :func:`compas.geometry.planarize_faces`
    * :func:`compas.geometry.mesh_planarize_faces_shapeop`

    """
    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):

        positions = {key: [] for key in mesh.vertices()}

        for fkey in mesh.faces():
            vertices = mesh.face_vertices(fkey)
            points = [mesh.vertex_coordinates(key) for key in vertices]
            plane = bestfit_plane(points)
            projections = project_points_plane(points, plane)

            for index, key in enumerate(vertices):
                positions[key].append(projections[index])

        for key, attr in mesh.vertices(True):
            if key in fixed:
                continue

            x, y, z = centroid_points(positions[key])
            attr['x'] = x
            attr['y'] = y
            attr['z'] = z

        if callback:
            callback(k, callback_args)


def mesh_planarize_faces_numpy(mesh, fixed=None, kmax=100, callback=None, callback_args=None):
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.utilities import i_to_rgb

    mesh = Mesh.from_obj(compas.get('hypar.obj'))

    for key, attr in mesh.vertices(True):
        attr['is_fixed'] = mesh.vertex_degree(key) == 2

    fixed  = [key for key in mesh.vertices_where({'is_fixed': True})]
    radius = {key: (0.05 if key in fixed else 0.01) for key in mesh.vertices()}

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_vertices(radius=radius)
    plotter.draw_faces()
    plotter.draw_edges()

    def callback(k, args):
        print(k)

        if k % 100 == 0:
            dev = mesh_flatness(mesh, maxdev=0.02)

            plotter.update_vertices(radius=radius)
            plotter.update_faces(facecolor={fkey: i_to_rgb(dev[fkey]) for fkey in mesh.faces()})
            plotter.update_edges()
            plotter.update()

    mesh_planarize_faces(mesh, fixed=fixed, kmax=2000, callback=callback)

    plotter.show()
