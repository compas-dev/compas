from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points
from compas.geometry import centroid_polygon


__all__ = [
    'mesh_smooth_centroid',
    'mesh_smooth_centerofmass',
    'mesh_smooth_area',
]


def mesh_smooth_centroid(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving every free vertex to the centroid of its neighbors.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fixed : list, optional
        The fixed vertices of the mesh.
    kmax : int, optional
        The maximum number of iterations.
    damping : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list, optional
        A list of arguments to be passed to the callback.

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    Examples
    --------
    >>>

    """
    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)


    for k in range(kmax):
        key_xyz = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}

        for key, attr in mesh.vertices(True):
            if key in fixed:
                continue

            x, y, z = key_xyz[key]

            cx, cy, cz = centroid_points([key_xyz[nbr] for nbr in mesh.vertex_neighbors(key)])
            # print(k, key, cx - x, cx - y, cx - z)

            attr['x'] += damping *(cx - x)
            attr['y'] += damping *(cy - y)
            attr['z'] += damping *(cz - z)

        # mesh.plot(show=True)

        if callback:
            callback(k, callback_args)

def mesh_smooth_centerofmass(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving every free vertex to the center of mass of the polygon formed by the neighboring vertices.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fixed : list, optional
        The fixed vertices of the mesh.
    kmax : int, optional
        The maximum number of iterations.
    damping : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list, optional
        A list of arguments to be passed to the callback.

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    Examples
    --------
    >>>

    """
    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        key_xyz = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}

        for key, attr in mesh.vertices(True):
            if key in fixed:
                continue

            x, y, z = key_xyz[key]

            cx, cy, cz = centroid_polygon([key_xyz[nbr] for nbr in mesh.vertex_neighbors(key, ordered=True)])

            attr['x'] += damping * (cx - x)
            attr['y'] += damping * (cy - y)
            attr['z'] += damping * (cz - z)

        if callback:
            callback(k, callback_args)


def mesh_smooth_area(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving each vertex to the barycenter of the centroids of the surrounding faces, weighted by area.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fixed : list, optional
        The fixed vertices of the mesh.
    kmax : int, optional
        The maximum number of iterations.
    damping : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list, optional
        A list of arguments to be passed to the callback.

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    Examples
    --------
    >>>

    """
    lim = 0.25
    def constrain(x1, x0, lim):
        x1 = min(x0 + lim, x1)
        x1 = max(x0 - lim, x1)
        return x1

    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    key_xyz_0 = {key: mesh.vertex_coordinates(key)[:] for key in mesh.vertices()}
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

            x1 = x + damping * (ax - x)
            y1 = y + damping * (ay - y)
            z1 = z + damping * (az - z)

            x0, y0, z0 = key_xyz[key]
            attr['x'] = constrain(x1, x0, lim)
            attr['y'] = constrain(y1, y0, lim)
            attr['z'] = constrain(z1, z0, lim)

        if callback:
            callback(k, callback_args)

def mesh_smooth_area(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving each vertex to the barycenter of the centroids of the surrounding faces, weighted by area.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fixed : list, optional
        The fixed vertices of the mesh.
    kmax : int, optional
        The maximum number of iterations.
    damping : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list, optional
        A list of arguments to be passed to the callback.

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    Examples
    --------
    >>>

    """
    lim = 1e7
    def constrain(x1, x0, lim):
        x1 = min(x0 + lim, x1)
        x1 = max(x0 - lim, x1)
        return x1

    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    key_xyz_0 = {key: mesh.vertex_coordinates(key)[:] for key in mesh.vertices()}
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

            x1 = x + damping * (ax - x)
            y1 = y + damping * (ay - y)
            z1 = z + damping * (az - z)

            x0, y0, z0 = key_xyz[key]
            attr['x'] = constrain(x1, x0, lim)
            attr['y'] = constrain(y1, y0, lim)
            attr['z'] = constrain(z1, z0, lim)

        if callback:
            callback(k, callback_args)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas_plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    fixed = list(mesh.vertices_where({'vertex_degree': 2}))

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end': mesh.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 1.0,
        })

    mesh_smooth_area(mesh, fixed=fixed, kmax=100, damping=0.)

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_lines(lines)
    plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
    plotter.draw_edges()

    plotter.show()

    import doctest
    doctest.testmod(globs=globals())
