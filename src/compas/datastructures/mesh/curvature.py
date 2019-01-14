from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = ['trimesh_mean_curvature']


def trimesh_mean_curvature(mesh):
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import array

    import compas

    from compas.datastructures import Mesh
    from compas.datastructures import trimesh_cotangent_laplacian_matrix
    from compas.datastructures import mesh_laplacian_matrix
    from compas.datastructures import mesh_quads_to_triangles
    from compas.datastructures import mesh_flip_cycles

    from compas.geometry import add_vectors
    from compas.geometry import subtract_vectors
    from compas.numerical import normrow

    from compas.plotters import MeshPlotter


    # mesh = Mesh.from_polyhedron(8)
    mesh = Mesh.from_obj(compas.get('mesh.obj'))

    mesh_quads_to_triangles(mesh)
    # mesh_flip_cycles(mesh)

    xyz = array(mesh.get_vertices_attributes('xyz'))

    L = mesh_laplacian_matrix(mesh)

    d = L.dot(xyz).tolist()

    # curvature = normrow(d).ravel().tolist()
    # print(curvature)

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    lines = []
    for index, key in enumerate(mesh.vertices()):
        vector = d[index]
        start = xyz[index]
        end = subtract_vectors(start, vector)
        lines.append({
            'start' : end,
            'end'   : start,
            'arrow' : 'end',
            'color' : '#ff0000'
        })

    plotter.draw_vertices(radius=0.02)
    plotter.draw_faces()

    plotter.draw_arrows(lines)

    plotter.show()
