from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import project_points_plane
from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.geometry import distance_line_line
from compas.geometry import bestfit_plane

from compas.utilities import window


__all__ = [
    'mesh_flatness',
    'mesh_planarize_faces',
]


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

    Warnings
    --------
    This function only works as expected for quadrilateral faces.

    """
    dev = []
    for fkey in mesh.faces():
        points = mesh.face_coordinates(fkey)
        if len(points) == 3:
            dev.append(0.0)
        else:
            lengths = [distance_point_point(a, b) for a, b in window(points + points[0:1], 2)]
            length = sum(lengths) / len(lengths)
            d = distance_line_line((points[0], points[2]), (points[1], points[3]))
            dev.append((d / length) / maxdev)
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
