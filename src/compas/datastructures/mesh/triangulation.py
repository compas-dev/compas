from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.datastructures.mesh.operations import mesh_split_face


__all__ = [
    'mesh_quads_to_triangles',
]


def mesh_quads_to_triangles(mesh, check_angles=False):
    """"""
    for fkey in list(mesh.faces()):
        attr = mesh.facedata[fkey]
        vertices = mesh.face_vertices(fkey)
        if len(vertices) == 4:
            a, b, c, d = vertices
            t1, t2 = mesh_split_face(mesh, fkey, b, d)
            mesh.facedata[t1] = attr.copy()
            mesh.facedata[t2] = attr.copy()
        del mesh.facedata[fkey]

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
