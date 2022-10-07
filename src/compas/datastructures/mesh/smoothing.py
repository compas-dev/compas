from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points
from compas.geometry import centroid_polygon


__all__ = [
    "mesh_smooth_centroid",
    "mesh_smooth_centerofmass",
    "mesh_smooth_area",
]


def mesh_smooth_centroid(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving every free vertex to the centroid of its neighbors.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
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
        key_xyz = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}

        for key, attr in mesh.vertices(True):
            if key in fixed:
                continue

            x, y, z = key_xyz[key]

            cx, cy, cz = centroid_points([key_xyz[nbr] for nbr in mesh.vertex_neighbors(key)])

            attr["x"] += damping * (cx - x)
            attr["y"] += damping * (cy - y)
            attr["z"] += damping * (cz - z)

        if callback:
            callback(k, callback_args)


def mesh_smooth_centerofmass(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving every free vertex to the center of mass of the polygon formed by the neighboring vertices.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
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
        key_xyz = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}

        for key, attr in mesh.vertices(True):
            if key in fixed:
                continue

            x, y, z = key_xyz[key]

            cx, cy, cz = centroid_polygon([key_xyz[nbr] for nbr in mesh.vertex_neighbors(key, ordered=True)])

            attr["x"] += damping * (cx - x)
            attr["y"] += damping * (cy - y)
            attr["z"] += damping * (cz - z)

        if callback:
            callback(k, callback_args)


def mesh_smooth_area(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving each vertex to the barycenter of the centroids of the surrounding faces, weighted by area.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
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
        key_xyz = {key: mesh.vertex_coordinates(key)[:] for key in mesh.vertices()}
        fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.faces()}
        fkey_area = {fkey: mesh.face_area(fkey) for fkey in mesh.faces()}

        for key, attr in mesh.vertices(True):
            if key in fixed:
                continue

            x, y, z = key_xyz[key]

            A = 0
            ax, ay, az = 0, 0, 0

            for fkey in mesh.vertex_faces(key, ordered=True):
                if fkey is None:
                    continue

                a = fkey_area[fkey]
                c = fkey_centroid[fkey]
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
