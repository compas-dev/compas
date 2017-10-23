from compas.geometry import circle_from_points_xy


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_dual',
    'mesh_voronoi',
]


def mesh_dual(mesh, cls=None):
    """Construct the dual of a mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    cls : Mesh, optional [None]
        The type of the dual mesh.
        Defaults to the type of the provided mesh object.

    Returns
    -------
    Mesh
        The dual mesh object.

    Example
    -------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.datastructures import mesh_dual
        from compas.visualization import MeshPlotter

        mesh = Mesh.from_obj(compas.get_data('faces.obj'))

        dual = mesh_dual(mesh)

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u, 'xy'),
                'end'  : mesh.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0
            })

        plotter = MeshPlotter(dual)

        plotter.draw_xlines(lines)

        plotter.draw_vertices(facecolor='#eeeeee', edgecolor='#000000', radius=0.2, text='key')
        plotter.draw_edges()

        plotter.show()

    """
    if not cls:
        cls = type(mesh)

    fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.faces()}
    outer = mesh.vertices_on_boundary()
    inner = list(set(mesh.vertices()) - set(outer))
    vertices = {}
    faces = {}

    for key in inner:
        fkeys = mesh.vertex_faces(key, ordered=True)
        for fkey in fkeys:
            if fkey not in vertices:
                vertices[fkey] = fkey_centroid[fkey]
        faces[key] = fkeys

    dual = cls()

    for key, (x, y, z) in vertices.items():
        dual.add_vertex(key, x=x, y=y, z=z)
    for fkey, vertices in faces.items():
        dual.add_face(vertices, fkey=fkey)

    return dual


def mesh_voronoi(mesh, cls=None, update_coordinates=True):
    """Construct the Voronoi dual of the triangulation of a set of points.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    cls : Mesh, optional
        The type of the dual mesh.
        Defaults to the type of the provided mesh object.
    update_coordinates : bool, optional
        Update the vertex coordinates of the voronoi.
        Defaults to true.

    Note
    ----
    This function produces a mesh with faces that have the oposite cycle direction
    of the original mesh.

    Example
    -------
    .. plot::
        :include-source:

        from numpy import random
        from numpy import hstack
        from numpy import zeros

        from compas.datastructures import Mesh
        from compas.datastructures import mesh_dual
        from compas.datastructures import mesh_voronoi
        from compas.datastructures import mesh_delaunay_from_points
        from compas.datastructures import trimesh_remesh

        from compas.visualization import MeshPlotter

        points = hstack((10.0 * random.random_sample((10, 2)), zeros((10, 1)))).tolist()
        mesh = Mesh.from_vertices_and_faces(points, mesh_delaunay_from_points(points))

        trimesh_remesh(mesh, 1.0, allow_boundary_split=True)

        points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
        mesh = Mesh.from_vertices_and_faces(points, mesh_delaunay_from_points(points))

        dual = mesh_voronoi(mesh)

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u, 'xy'),
                'end'  : mesh.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 0.5
            })

        plotter = MeshPlotter(dual, figsize=(10, 7))

        plotter.draw_xlines(lines)
        plotter.draw_vertices(facecolor='#eeeeee', edgecolor='#000000', radius=0.05)
        plotter.draw_faces(facecolor='#eeeeee', edgecolor='#eeeeee', text='key')
        plotter.draw_edges(keys=[(u, v) for u, v in dual.edges() if not dual.is_edge_naked(u, v)])

        plotter.show()

    """
    if not cls:
        cls = type(mesh)

    fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.faces()}
    uv_fkey = {}

    outer = mesh.vertices_on_boundary(ordered=True)[::-1]
    inner = list(set(mesh.vertices()) - set(outer))

    f = mesh._get_face_key(None)

    for i in range(-1, len(outer) - 1):
        u = outer[i]
        v = outer[i + 1]
        uv_fkey[(u, v)] = f
        fkey_centroid[f] = mesh.edge_midpoint(u, v)
        f += 1

    vertices = {}
    faces = {}

    for key in inner:
        fkeys = mesh.vertex_faces(key, ordered=True)
        for fkey in fkeys:
            if fkey not in vertices:
                vertices[fkey] = fkey_centroid[fkey]
        faces[key] = fkeys

    for key in outer:
        nbrs = mesh.vertex_neighbours(key, ordered=True)

        if len(nbrs) < 2:
            continue

        # the first boundary edge
        fkey = uv_fkey[(nbrs[0], key)]
        fkeys = [fkey]
        if fkey not in vertices:
            vertices[fkey] = fkey_centroid[fkey]

        # all internal edges
        for nbr in nbrs[0:-1]:
            fkey = mesh.halfedge[nbr][key]
            fkeys.append(fkey)
            if fkey not in vertices:
                vertices[fkey] = fkey_centroid[fkey]

        # the last boundary edge
        fkey = uv_fkey[(key, nbrs[-1])]
        fkeys.append(fkey)
        if fkey not in vertices:
            vertices[fkey] = fkey_centroid[fkey]
        faces[key] = fkeys

    voronoi = cls()

    for key, (x, y, z) in vertices.items():
        voronoi.add_vertex(key, x=x, y=y, z=z)
    for fkey, vertices in faces.items():
        voronoi.add_face(vertices, fkey=fkey)

    if update_coordinates:
        for key in mesh.faces():
            a, b, c = mesh.face_coordinates(key)
            center, radius, normal = circle_from_points_xy(a, b, c)
            voronoi.vertex[key]['x'] = center[0]
            voronoi.vertex[key]['y'] = center[1]
            voronoi.vertex[key]['z'] = center[2]

    return voronoi


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from numpy import random
    from numpy import hstack
    from numpy import zeros

    from compas.datastructures import Mesh
    from compas.datastructures import mesh_dual
    from compas.datastructures import mesh_voronoi
    from compas.datastructures import mesh_delaunay_from_points
    from compas.datastructures import trimesh_remesh
    from compas.visualization import MeshPlotter

    # points = [[2853.0, -29.0, 594.0], [2922.0, -29.0, 594.0], [2922.0, 59.0, 594.0], [2853.0, 59.0, 594.0], [3028.0, -29.0, 594.0], [3097.0, -29.0, 594.0], [3097.0, 59.0, 594.0], [3028.0, 59.0, 594.0]]
    # faces = mesh_delaunay_from_points(points)
    # mesh = Mesh.from_vertices_and_faces(points, faces)

    points = hstack((10.0 * random.random_sample((10, 2)), zeros((10, 1)))).tolist()
    mesh = Mesh.from_vertices_and_faces(points, mesh_delaunay_from_points(points))
    trimesh_remesh(mesh, 1.0, allow_boundary_split=True)
    points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    mesh = Mesh.from_vertices_and_faces(points, mesh_delaunay_from_points(points))

    dual = mesh_voronoi(mesh, update_coordinates=True)

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end'  : mesh.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 0.5
        })

    plotter = MeshPlotter(dual, figsize=(10, 7))

    plotter.draw_xlines(lines)
    plotter.draw_vertices(facecolor='#eeeeee', edgecolor='#000000', radius=0.05)
    plotter.draw_faces(facecolor='#eeeeee', edgecolor='#eeeeee', text='key')
    plotter.draw_edges(keys=[(u, v) for u, v in dual.edges() if not dual.is_edge_naked(u, v)])

    plotter.show()
