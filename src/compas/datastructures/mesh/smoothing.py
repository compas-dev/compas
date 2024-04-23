from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import centroid_points
from compas.geometry import centroid_polygon


def mesh_smooth_centroid(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving every free vertex to the centroid of its neighbors.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh object.
    fixed : list[int], optional
        The fixed vertices of the mesh.
    kmax : int, optional
        The maximum number of iterations.
    damping : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list[Any], optional
        A list of arguments to be passed to the callback.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    """
    if callback:
        if not callable(callback):
            raise Exception("Callback is not callable.")

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        vertex_xyz = {vertex: mesh.vertex_coordinates(vertex) for vertex in mesh.vertices()}

        for vertex, attr in mesh.vertices(True):
            if vertex in fixed:
                continue

            x, y, z = vertex_xyz[vertex]

            cx, cy, cz = centroid_points([vertex_xyz[nbr] for nbr in mesh.vertex_neighbors(vertex)])

            attr["x"] += damping * (cx - x)
            attr["y"] += damping * (cy - y)
            attr["z"] += damping * (cz - z)

        if callback:
            callback(k, callback_args)


def mesh_smooth_centerofmass(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving every free vertex to the center of mass of the polygon formed by the neighboring vertices.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh object.
    fixed : list[int], optional
        The fixed vertices of the mesh.
    kmax : int, optional
        The maximum number of iterations.
    damping : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list[Any], optional
        A list of arguments to be passed to the callback.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    """
    if callback:
        if not callable(callback):
            raise Exception("Callback is not callable.")

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        vertex_xyz = {vertex: mesh.vertex_coordinates(vertex) for vertex in mesh.vertices()}

        for vertex, attr in mesh.vertices(True):
            if vertex in fixed:
                continue

            x, y, z = vertex_xyz[vertex]

            cx, cy, cz = centroid_polygon([vertex_xyz[nbr] for nbr in mesh.vertex_neighbors(vertex, ordered=True)])

            attr["x"] += damping * (cx - x)
            attr["y"] += damping * (cy - y)
            attr["z"] += damping * (cz - z)

        if callback:
            callback(k, callback_args)


def mesh_smooth_area(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving each vertex to the barycenter of the centroids of the surrounding faces, weighted by area.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh object.
    fixed : list[int], optional
        The fixed vertices of the mesh.
    kmax : int, optional
        The maximum number of iterations.
    damping : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list[Any], optional
        A list of arguments to be passed to the callback.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    """
    if callback:
        if not callable(callback):
            raise Exception("Callback is not callable.")

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        vertex_xyz = {vertex: mesh.vertex_coordinates(vertex)[:] for vertex in mesh.vertices()}
        face_centroid = {face: mesh.face_centroid(face) for face in mesh.faces()}
        face_area = {face: mesh.face_area(face) for face in mesh.faces()}

        for vertex, attr in mesh.vertices(True):
            if vertex in fixed:
                continue

            x, y, z = vertex_xyz[vertex]

            A = 0
            ax, ay, az = 0, 0, 0

            for face in mesh.vertex_faces(vertex, ordered=True):
                if face is None:
                    continue

                a = face_area[face]
                c = face_centroid[face]
                ax += a * c[0]
                ay += a * c[1]
                az += a * c[2]
                A += a

            if A:
                ax = ax / A
                ay = ay / A
                az = az / A

            attr["x"] += damping * (ax - x)
            attr["y"] += damping * (ay - y)
            attr["z"] += damping * (az - z)

        if callback:
            callback(k, callback_args)
