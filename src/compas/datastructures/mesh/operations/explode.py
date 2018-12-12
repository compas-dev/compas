from compas.topology import connected_components

__author__     = ['Robin Oval']
__copyright__  = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'oval@arch.ethz.ch'

__all__ = [
    'mesh_explode'
]

def mesh_explode(mesh, cls=None):
    """Explode a mesh into its disjointed parts.

    Parameters
    ----------
    mesh : Mesh
        A mesh.

    Returns
    -------
    exploded_meshes : list
        The list of the meshes from the exploded mesh parts.

    """

    if cls is None:
        cls = type(mesh)

    connected_vertices = connected_components(mesh.adjacency)

    exploded_meshes = []

    for vertex_keys in connected_vertices:
        
        vertices = [mesh.vertex_coordinates(vkey) for vkey in vertex_keys]
        
        key_to_index = {vkey: i for i, vkey in enumerate(vertex_keys)}

        face_keys = list(set([fkey for vkey in vertex_keys for fkey in mesh.vertex_faces(vkey)]))
        faces = [ [key_to_index[vkey] for vkey in mesh.face_vertices(fkey)] for fkey in face_keys]
        
        exploded_meshes.append(cls.from_vertices_and_faces(vertices, faces))

    return exploded_meshes

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
