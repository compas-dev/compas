from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import geometric_key


__all__ = [
    'mesh_cull_duplicate_vertices'
]


def mesh_cull_duplicate_vertices(mesh, precision=None):
    """Cull all duplicate vertices of a mesh and sanitize affected faces.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    precision (str): Optional.
        A formatting option that specifies the precision of the
        individual numbers in the string (truncation after the decimal point).
        Supported values are any float precision, or decimal integer (``'d'``).
        Default is ``'3f'``.
    """
    key_gkey = {key: geometric_key(mesh.vertex_coordinates(key), precision=precision) for key in mesh.vertices()}
    gkey_key = {gkey: key for key, gkey in iter(key_gkey.items())}

    for key in list(mesh.vertices()):
        test = gkey_key[key_gkey[key]]
        if test != key:
            del mesh.vertex[key]
            del mesh.halfedge[key]
            for u in mesh.halfedge:
                nbrs = list(mesh.halfedge[u].keys())
                for v in nbrs:
                    if v == key:
                        del mesh.halfedge[u][v]

    for fkey in mesh.faces():
        seen = set()
        face = []
        for key in [gkey_key[key_gkey[key]] for key in mesh.face_vertices(fkey)]:
            if key not in seen:
                seen.add(key)
                face.append(key)
        mesh.face[fkey] = face
        for u, v in mesh.face_halfedges(fkey):
            mesh.halfedge[u][v] = fkey
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None



# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    vertices = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (10.0, 10.0, 0.0), (0.0, 10.0, 0.0), (5.0, 5.0, 0.0), (5.0, 5.0, 0.0)]
    faces = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 5]]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_edges(width=0.5)

    print("Original mesh:")
    print(mesh)

    _mesh_cull_duplicate_vertices(mesh)

    print("Mesh with duplicate vertices deleted:")
    print(mesh)

    plotter.show()
