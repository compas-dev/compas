from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import area_polygon


__all__ = [
    'smooth_centroid',
    'smooth_centerofmass',
    'smooth_area',
]


def smooth_centroid(vertices,
                    adjacency,
                    fixed=None,
                    kmax=1,
                    damping=0.5,
                    callback=None,
                    callback_args=None):
    """Smooth a connected set of vertices
    by moving each vertex to the centroid of its neighbors.

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

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.geometry import smooth_centroid
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        vertices   = mesh.get_vertices_attributes('xyz')
        neighbors = [mesh.vertex_neighbors(key) for key in mesh.vertices()]
        fixed      = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u, 'xy'),
                'end'  : mesh.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0,
            })

        smooth_centroid(vertices, neighbors, fixed=fixed, kmax=100)

        for key, attr in mesh.vertices(True):
            attr['x'] = vertices[key][0]
            attr['y'] = vertices[key][1]
            attr['z'] = vertices[key][2]

        plotter = MeshPlotter(mesh)

        plotter.draw_lines(lines)
        plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed}, radius=0.05)
        plotter.draw_edges()

        plotter.show()

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


def smooth_centerofmass(vertices,
                        adjacency,
                        fixed=None,
                        kmax=1,
                        damping=0.5,
                        callback=None,
                        callback_args=None):
    """Smooth a connected set of vertices by moving each vertex to
    the center of mass of the polygon formed by the neighboring vertices.

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

    Notes
    -----
    When using this algorithm in combination with one of the datastructures (as in the example below),
    note that the neighbors of each vertex have to be listed in order, i.e. they have to form a polygon
    without self-intersections.

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.geometry import smooth_centerofmass
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        vertices  = mesh.get_vertices_attributes('xyz')
        adjacency = [mesh.vertex_neighbors(key, ordered=True) for key in mesh.vertices()]
        fixed     = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u, 'xy'),
                'end'  : mesh.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0,
            })

        smooth_centerofmass(vertices, adjacency, fixed=fixed, kmax=100)

        for key, attr in mesh.vertices(True):
            attr['x'] = vertices[key][0]
            attr['y'] = vertices[key][1]
            attr['z'] = vertices[key][2]

        plotter = MeshPlotter(mesh)

        plotter.draw_lines(lines)
        plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
        plotter.draw_edges()

        plotter.show()

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

            com = centroid_polygon([xyz_0[nbr] for nbr in adjacency[index]])

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

    Examples
    --------
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
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Mesh
    from compas.geometry import smooth_centerofmass
    from compas.plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    # key_index = mesh.key_index()
    # vertices  = mesh.get_vertices_attributes('xyz')
    # faces     = [mesh.face_vertices(key) for key in mesh.faces()]
    # neighbors = [[key_index[nbr] for nbr in mesh.vertex_neighbors(key)] for key in mesh.vertices()]
    # fixed     = [key_index[key] for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

    vertices  = mesh.get_vertices_attributes('xyz')
    faces     = [mesh.face_vertices(fkey) for fkey in mesh.faces()]
    adjacency = [mesh.vertex_neighbors(key, ordered=True) for key in mesh.vertices()]
    fixed     = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end'  : mesh.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 1.0,
        })

    smooth_centerofmass(vertices, adjacency, fixed=fixed, kmax=100)

    for key, attr in mesh.vertices(True):
        attr['x'] = vertices[key][0]
        attr['y'] = vertices[key][1]
        attr['z'] = vertices[key][2]

    plotter = MeshPlotter(mesh)

    plotter.draw_lines(lines)
    plotter.draw_vertices(text={key: mesh.vertex_degree(key) for key in mesh.vertices()}, facecolor={key: '#ff0000' for key in fixed})
    plotter.draw_edges()
    plotter.draw_faces(text={key: "{:.1f}".format(mesh.face_area(key)) for key in mesh.faces()})

    plotter.show()
