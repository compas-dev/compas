from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon
from compas.geometry import area_polygon


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'smooth_centroid',
    'smooth_centerofmass',
    'smooth_area',

    'mesh_smooth_centroid',
    'mesh_smooth_area',

    'network_smooth_centroid',
]


def smooth_centroid(vertices,
                    adjacency,
                    fixed=None,
                    kmax=1,
                    damping=0.5,
                    callback=None,
                    callback_args=None):
    """Smooth a connected set of vertices
    by moving each vertex to the centroid of its neighbours.

    Parameters
    ----------
    vertices : dict
        A dictionary of vertex coordinates.
    adjacency : dict
        Adjacency information for each of the vertices.
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

    Example
    -------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.geometry import smooth_centroid
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        vertices   = mesh.get_vertices_attributes('xyz')
        neighbours = [mesh.vertex_neighbours(key) for key in mesh.vertices()]
        fixed      = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u, 'xy'),
                'end'  : mesh.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0,
            })

        smooth_centroid(vertices, neighbours, fixed=fixed, kmax=100)

        for key, attr in mesh.vertices(True):
            attr['x'] = vertices[key][0]
            attr['y'] = vertices[key][1]
            attr['z'] = vertices[key][2]

        plotter = MeshPlotter(mesh)

        plotter.draw_lines(lines)
        plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed}, radius=0.05)
        plotter.draw_edges()

        plotter.show()

    See Also
    --------
    * :func:`smooth_centerofmass`
    * :func:`smooth_area`
    * :func:`compas.geometry.centroid_points`

    """
    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        xyz_0 = [xyz[:] for xyz in vertices]

        for index, point in enumerate(xyz_0):
            if index in fixed:
                continue

            nbrs = adjacency[index]
            centroid = centroid_points([xyz_0[nbr] for nbr in nbrs])

            vertices[index][0] += damping * (centroid[0] - point[0])
            vertices[index][1] += damping * (centroid[1] - point[1])
            vertices[index][2] += damping * (centroid[2] - point[2])

        if callback:
            callback(k, callback_args)


def smooth_laplacian():
    pass


def smooth_centerofmass(vertices,
                        adjacency,
                        fixed=None,
                        kmax=1,
                        damping=0.5,
                        callback=None,
                        callback_args=None):
    """Smooth a connected set of vertices by moving each vertex to
    the center of mass of the polygon formed by the neighbouring vertices.

    Parameters
    ----------
    verticses : dict
        A dictionary of vertex coordinates.
    adjacency : dict
        Adjacency information for each of the vertices.
    fixed : list, optional
        The fixed vertices of the mesh.
    kmax : int, optional
        The maximum number of iterations.
    d : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list, optional
        A list of arguments to be passed to the callback.

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    Note
    ----
    When using this algorithm in combination with one of the datastructures (as in the example below),
    note that the neighbours of each vertex have to be listed in order, i.e. they have to form a polygon
    without self-intersections.

    Example
    -------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.geometry import smooth_centerofmass
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        vertices   = mesh.get_vertices_attributes('xyz')
        neighbours = [mesh.vertex_neighbours(key) for key in mesh.vertices()]
        fixed      = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u, 'xy'),
                'end'  : mesh.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0,
            })

        smooth_centerofmass(vertices, neighbours, fixed=fixed, kmax=100)

        for key, attr in mesh.vertices(True):
            attr['x'] = vertices[key][0]
            attr['y'] = vertices[key][1]
            attr['z'] = vertices[key][2]

        plotter = MeshPlotter(mesh)

        plotter.draw_lines(lines)
        plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
        plotter.draw_edges()

        plotter.show()

    See Also
    --------
    * :func:`smooth_centroid`
    * :func:`smooth_area`
    * :func:`compas.geometry.center_of_mass_polygon`

    """
    fixed = fixed or []
    fixed = set(fixed)

    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    for k in range(kmax):
        xyz_0 = [xyz[:] for xyz in vertices]

        for index, point in enumerate(xyz_0):
            if index in fixed:
                continue

            nbrs = adjacency[index]
            com = center_of_mass_polygon([xyz_0[nbr] for nbr in nbrs])

            vertices[index][0] += damping * (com[0] - point[0])
            vertices[index][1] += damping * (com[1] - point[1])
            vertices[index][2] += damping * (com[2] - point[2])

        if callback:
            callback(k, callback_args)


def smooth_area(vertices,
                faces,
                adjacency,
                fixed=None,
                kmax=1,
                damping=0.5,
                callback=None,
                callback_args=None):
    """Smooth a set of connected vertices by moving each vertex to the centroid
    of the surrounding faces, weighted by the area of the face.

    Parameters
    ----------
    vertices : dict
        A dictionary of vertex coordinates.
    faces : dict
        A dictionary of faces referencing the vertices dict.
    adjacency : dict
        Adjacency information for each of the vertices.
    fixed : list, optional
        The fixed vertices of the mesh.
    kmax : int, optional
        The maximum number of iterations.
    d : float, optional
        The damping factor.
    callback : callable, optional
        A user-defined callback function to be executed after every iteration.
    callback_args : list, optional
        A list of arguments to be passed to the callback.

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    Example
    -------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.geometry import smooth_area

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        vertices  = mesh.get_vertices_attributes('xyz')
        faces     = [mesh.face_vertices(fkey) for fkey in mesh.faces()]
        adjacency = [mesh.vertex_faces(key, ordered=True) for key in mesh.vertices()]
        fixed     = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u, 'xy'),
                'end'  : mesh.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0,
            })

        smooth_area(vertices, faces, adjacency, fixed=fixed, kmax=100)

        for key, attr in mesh.vertices(True):
            attr['x'] = vertices[key][0]
            attr['y'] = vertices[key][1]
            attr['z'] = vertices[key][2]

        plotter = MeshPlotter(mesh)

        plotter.draw_lines(lines)
        plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
        plotter.draw_edges()

        plotter.show()

    See Also
    --------
    * :func:`smooth_centroid`
    * :func:`smooth_centerofmass`
    * :func:`compas.geometry.centroid_points`
    * :func:`compas.geometry.area_polygon`

    """
    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        xyz_0      = [xyz[:] for xyz in vertices]
        centroid_0 = [centroid_points([vertices[index] for index in corners]) for corners in faces]
        area_0     = [area_polygon([vertices[index] for index in corners]) for corners in faces]

        for index, point in enumerate(xyz_0):
            if index in fixed:
                continue

            A = 0
            x, y, z = 0, 0, 0
            for nbr in adjacency[index]:
                if nbr is not None:
                    a  = area_0[nbr]
                    c  = centroid_0[nbr]
                    x += a * c[0]
                    y += a * c[1]
                    z += a * c[2]
                    A += a
            if A:
                x = x / A
                y = y / A
                z = z / A

            vertices[index][0] += damping * (x - point[0])
            vertices[index][1] += damping * (y - point[1])
            vertices[index][2] += damping * (z - point[2])

        if callback:
            callback(k, callback_args)


# ==============================================================================
# mesh variations
# ==============================================================================


def mesh_smooth_centroid(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving every free vertex to the centroid of its neighbours.

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

    Example
    -------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.geometry import mesh_smooth_centroid

        mesh = Mesh.from_obj(compas.get('faces.obj'))
        fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

        mesh_smooth_centroid(mesh, fixed=fixed)

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
        plotter.draw_faces()
        plotter.draw_edges()

        plotter.show()

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

            point = key_xyz[key]

            centroid = centroid_points([key_xyz[nbr] for nbr in mesh.vertex_neighbours(key)])

            attr['x'] += damping * (centroid[0] - point[0])
            attr['y'] += damping * (centroid[1] - point[1])
            attr['z'] += damping * (centroid[2] - point[2])

        if callback:
            callback(k, callback_args)


def mesh_smooth_area(mesh, fixed=None, kmax=100, damping=0.5, callback=None, callback_args=None):
    """Smooth a mesh by moving each vertex to the barycentre of the centroids of the surrounding faces, weighted by area.

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

    Example
    -------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.geometry import mesh_smooth_area

        mesh = Mesh.from_obj(compas.get('faces.obj'))
        fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

        mesh_smooth_area(mesh, fixed=fixed)

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
        plotter.draw_faces()
        plotter.draw_edges()

        plotter.show()

    """
    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        key_xyz       = {key: mesh.vertex_coordinates(key)[:] for key in mesh.vertices()}
        fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.faces()}
        fkey_area     = {fkey: mesh.face_area(fkey) for fkey in mesh.faces()}

        for key, attr in mesh.vertices(True):
            if key in fixed:
                continue

            point = key_xyz[key]

            A = 0
            x, y, z = 0, 0, 0

            for fkey in mesh.vertex_faces(key, ordered=True):
                if fkey is None:
                    continue

                a  = fkey_area[fkey]
                c  = fkey_centroid[fkey]
                x += a * c[0]
                y += a * c[1]
                z += a * c[2]
                A += a

            if A:
                x = x / A
                y = y / A
                z = z / A

            attr['x'] += damping * (x - point[0])
            attr['y'] += damping * (y - point[1])
            attr['z'] += damping * (z - point[2])

        if callback:
            callback(k, callback_args)


# ==============================================================================
# network variations
# ==============================================================================


def network_smooth_centroid(network, fixed=None, kmax=100, damping=1.0, callback=None, callback_args=None):
    """Smooth a network by moving each vertex to the centroid of its neighbours.

    Parameters
    ----------
    network : Mesh
        A network object.
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

    Example
    -------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Network
        from compas.plotters import NetworkPlotter
        from compas.geometry import network_smooth_centroid

        network = Network.from_obj(compas.get('grid_irregular.obj'))
        fixed = [key for key in network.vertices() if network.vertex_degree(key) == 1]

        network_smooth_centroid(network, fixed=fixed)

        plotter = NetworkPlotter(network)

        plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
        plotter.draw_edges()

        plotter.show()

    """
    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        key_xyz = {key: network.vertex_coordinates(key) for key in network.vertices()}

        for key, attr in network.vertices(True):
            if key in fixed:
                continue

            point = key_xyz[key]

            centroid = centroid_points([key_xyz[nbr] for nbr in network.vertex_neighbours(key)])

            attr['x'] += damping * (centroid[0] - point[0])
            attr['y'] += damping * (centroid[1] - point[1])
            attr['z'] += damping * (centroid[2] - point[2])

        if callback:
            callback(k, callback_args)


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":

    import os
    import sys

    import compas

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    # images = []

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start' : mesh.vertex_coordinates(u, 'xy'),
            'end'   : mesh.vertex_coordinates(v, 'xy'),
            'color' : '#cccccc',
            'width' : 0.5
        })
    plotter.draw_lines(lines)

    plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.update(pause=1.0)

    # filepath = os.path.join(compas.TEMP, 'image_{}.jpg'.format(0))
    # plotter.save(filepath)
    # images.append(filepath)

    def callback(k, args):
        print(k)

        # for key, attr in mesh.vertices(True):
        #     index = key_index[key]
        #     attr['x'] = vertices[index][0]
        #     attr['y'] = vertices[index][1]
        #     attr['z'] = vertices[index][2]

        plotter.update_vertices()
        plotter.update_faces()
        plotter.update_edges()
        plotter.update(pause=0.001)

        # filepath = os.path.join(compas.TEMP, 'image_{}.jpg'.format(k + 1))
        # plotter.save(filepath)
        # images.append(filepath)

    mesh_smooth_area(mesh, kmax=50, fixed=fixed, callback=callback)

    # plotter.saveas_gif(os.path.join(compas.TEMP, 'smoothing.gif'), images)

    # for filepath in images:
    #     os.remove(filepath)

    plotter.show()
