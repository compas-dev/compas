__author__     = ['Robin Oval']
__copyright__  = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'oval@arch.ethz.ch'

__all__ = [
    'mesh_disjointed_parts',
    'mesh_explode'
]

def mesh_disjointed_parts(mesh):
    """Get the disjointed parts in a mesh as lists of faces.

    Parameters
    ----------
    mesh : Mesh
        A mesh.

    Returns
    -------
    disjointed_faces : list
        The list of disjointed parts as lists of face keys.

    """

    parts = []
    faces = list(mesh.faces())

    while len(faces) > 0:
        # pop one face to start a part
        part = [faces.pop()]
        next_neighbours = [part[-1]]

        # propagate to neighbours
        while len(next_neighbours) > 0:

            for fkey in mesh.face_neighbors(next_neighbours.pop()):
                
                if fkey not in part:
                    part.append(fkey)
                    faces.remove(fkey)
                    
                    if fkey not in next_neighbours:
                        next_neighbours.append(fkey)
        
        parts.append(part)

    return parts

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

    parts = mesh_disjointed_parts(mesh)

    exploded_meshes = []

    for part in parts:
        
        vertex_keys = list(set([vkey for fkey in part for vkey in mesh.face_vertices(fkey)]))
        vertices = [mesh.vertex_coordinates(vkey) for vkey in vertex_keys]
        
        key_to_index = {vkey: i for i, vkey in enumerate(vertex_keys)}
        faces = [ [key_to_index[vkey] for vkey in mesh.face_vertices(fkey)] for fkey in part]
        
        exploded_meshes.append(cls.from_vertices_and_faces(vertices, faces))

    return exploded_meshes

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
