from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'smooth_centroid',
    'smooth_centerofmass',
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
    verticses : dict
        A dictionary of vertex coordinates.
    adjacency : dict
        Adjacency information for each of the vertices.
    fixed : list, optional [None]
        The fixed vertices of the mesh.
    kmax : int, optional [1]
        The maximum number of iterations.
    d : float, optional [0.5]
        The damping factor.
    callback : callable, optional [None]
        A user-defined callback function to be executed after every iteration.
    callback_args : list, optional [None]
        A list of arguments to be passed to the callback.

    Raises
    ------
    Exception
        If a callback is provided, but it is not callable.

    Note
    ----
    When using this algorithm in combination with one of the datastructures (as in the example below),
    note that the neighbours of each vertex can be listed in random order.

    See Also
    --------
    * :func:`smooth_centerofmass`
    * :func:`smooth_area`
    * :func:`compas.geometry.centroid_points`

    Example
    -------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.geometry import smooth_centroid
        from compas.visualization import MeshPlotter

        mesh = Mesh.from_obj(compas.get_data('faces.obj'))

        vertices  = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
        adjacency = {key: mesh.vertex_neighbours(key) for key in mesh.vertices()}
        fixed     = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u, 'xy'),
                'end'  : mesh.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0,
            })

        vertices = smooth_centroid(vertices, adjacency, fixed=fixed, kmax=100)

        for key, attr in mesh.vertices(True):
            attr['x'] = vertices[key][0]
            attr['y'] = vertices[key][1]
            attr['z'] = vertices[key][2]

        plotter = MeshPlotter(mesh)

        plotter.draw_xlines(lines)
        plotter.draw_vertices()
        plotter.draw_edges()

        plotter.show()

    """
    if callback:
        if not callable(callback):
            raise Exception('Callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):
        vertices_0 = {key: xyz for key, xyz in iter(vertices.items())}

        for key, point in iter(vertices_0.items()):
            if key in fixed:
                continue

            nbrs = adjacency[key]
            centroid = centroid_points([vertices_0[nbr] for nbr in nbrs])

            vertices[key][0] += damping * (centroid[0] - point[0])
            vertices[key][1] += damping * (centroid[1] - point[1])
            vertices[key][2] += damping * (centroid[2] - point[2])

        if callback:
            callback(vertices, k, callback_args)

    return vertices


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
    fixed : list, optional [None]
        The fixed vertices of the mesh.
    kmax : int, optional [1]
        The maximum number of iterations.
    d : float, optional [0.5]
        The damping factor.
    callback : callable, optional [None]
        A user-defined callback function to be executed after every iteration.
    callback_args : list, optional [None]
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

    See Also
    --------
    * :func:`smooth_centroid`
    * :func:`smooth_area`
    * :func:`compas.geometry.center_of_mass_polygon`

    Example
    -------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.geometry import smooth_centerofmass
        from compas.visualization import MeshPlotter

        mesh = Mesh.from_obj(compas.get_data('faces.obj'))

        vertices  = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
        adjacency = {key: mesh.vertex_neighbours(key, ordered=True) for key in mesh.vertices()}
        fixed     = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u, 'xy'),
                'end'  : mesh.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0,
            })

        vertices = smooth_centerofmass(vertices, adjacency, fixed=fixed, kmax=100)

        for key, attr in mesh.vertices(True):
            attr['x'] = vertices[key][0]
            attr['y'] = vertices[key][1]
            attr['z'] = vertices[key][2]

        plotter = MeshPlotter(mesh)

        plotter.draw_xlines(lines)
        plotter.draw_vertices()
        plotter.draw_edges()

        plotter.show()

    """
    fixed = fixed or []
    fixed = set(fixed)

    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    for k in range(kmax):
        vertices_0 = {key: xyz for key, xyz in iter(vertices.items())}

        for key, point in iter(vertices_0.items()):
            if key in fixed:
                continue

            nbrs = adjacency[key]
            com = center_of_mass_polygon([vertices_0[nbr] for nbr in nbrs])

            vertices[key][0] += damping * (com[0] - point[0])
            vertices[key][1] += damping * (com[1] - point[1])
            vertices[key][2] += damping * (com[2] - point[2])

        if callback:
            callback(vertices, k, callback_args)

    return vertices


def smooth_area():
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Mesh
    from compas.geometry import smooth_centroid
    from compas.geometry import smooth_centerofmass
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    vertices = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
    adjacency = {key: mesh.vertex_neighbours(key, ordered=True) for key in mesh.vertices()}
    fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end'  : mesh.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 1.0,
        })

    plotter = MeshPlotter(mesh)

    plotter.draw_xlines(lines)

    plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
    plotter.draw_edges()

    def callback(vertices, k, args):
        for key, attr in mesh.vertices(True):
            attr['x'] = vertices[key][0]
            attr['y'] = vertices[key][1]
            attr['z'] = vertices[key][2]

        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(pause=0.01)

    vertices = smooth_centerofmass(vertices, adjacency, fixed=fixed, kmax=100, callback=callback)

    plotter.show()
