__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_dual',
]


def mesh_dual(mesh, cls=None):
    """Construct the dual of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        cls (compas.datastructures.mesh.Mesh): Optional. Mesh class of the dual.
            Defaults to the type of the provided mesh object.

    Returns:
        compas.datastructures.Mesh: The dual mesh.

    Example:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.datastructures import mesh_dual
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            dual = mesh_dual(mesh)

            plotter = MeshPlotter(dual)

            lines = []
            for u, v in mesh.edges():
                lines.append({
                    'start': mesh.vertex_coordinates(u, 'xy'),
                    'end'  : mesh.vertex_coordinates(v, 'xy'),
                    'color': '#cccccc',
                    'width': 1.0
                })

            plotter.draw_xlines(lines)

            plotter.draw_vertices(facecolor='#eeeeee', edgecolor='#000000', radius=0.2, text={key: key for key in dual.vertices()})
            plotter.draw_edges(color='#000000', width=2.0)

            plotter.show()

    """
    if not cls:
        cls = type(mesh)

    fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.face}
    inner = list(set(mesh.vertices()) - set(mesh.vertices_on_boundary()))
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


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas
    from compas.datastructures import Mesh
    from compas.datastructures import mesh_dual

    from compas.visualization.plotters.meshplotter import MeshPlotter

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    dual = mesh_dual(mesh)

    lines = []
    for u, v in dual.wireframe():
        lines.append({
            'start': dual.vertex_coordinates(u, 'xy'),
            'end'  : dual.vertex_coordinates(v, 'xy'),
            'color': '#000000',
            'width': 2.0
        })

    points = []
    for key in dual.vertices():
        points.append({
            'pos'      : dual.vertex_coordinates(key, 'xy'),
            'text'     : str(key),
            'textcolor': '#000000',
            'facecolor': '#eeeeee',
            'edgecolor': '#000000',
            'radius'   : 0.2
        })

    plotter = MeshPlotter(mesh)

    plotter.draw_edges(color={(u, v): '#cccccc' for u, v in mesh.edges()})
    plotter.draw_xlines(lines)
    plotter.draw_xpoints(points)

    plotter.show()
