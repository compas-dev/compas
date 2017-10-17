from compas.datastructures.mesh import Mesh

from compas_blender.geometry import BlenderMesh


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'mesh_from_bmesh'
]


def mesh_from_bmesh(bmesh):
    """ Create a Mesh datastructure from a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        obj: Mesh object.
    """
    blendermesh = BlenderMesh(bmesh)
    vertices = blendermesh.get_vertex_coordinates()
    faces = blendermesh.get_face_vertex_indices()
    mesh = Mesh.from_vertices_and_faces(vertices=vertices, faces=faces)
    # mesh.add_edges_from_faces()
    return mesh
