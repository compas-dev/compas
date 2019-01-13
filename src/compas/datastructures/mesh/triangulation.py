from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'mesh_quads_to_triangles',
]


def mesh_quads_to_triangles(mesh, check_angles=False):
    """"""
    for fkey in list(mesh.faces()):
        vertices = mesh.face_vertices(fkey)
        if len(vertices) == 4:
            a, b, c, d = vertices
            mesh.split_face(fkey, b, d)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
