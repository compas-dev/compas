from __future__ import print_function

from compas.utilities import geometric_key


__author__    = ['Matthias Rippmann']
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'rippmann@ethz.ch'


__all__ = [
    'mesh_cull_duplicate_vertices'
]


def mesh_cull_duplicate_vertices(mesh, precision='3f'):
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

    geo_keys = {}
    keys_geo = {}
    keys_pointer = {}
    for key in mesh.vertices():
        geo_key = geometric_key(mesh.vertex_coordinates(key), precision)
        if geo_key in geo_keys:
            keys_pointer[key] = geo_keys[geo_key]
        else:
            geo_keys[geo_key] = key
            keys_geo[key] = geo_key

    keys_remain = geo_keys.values()
    keys_del = [key for key in mesh.vertices() if key not in keys_remain]

    # delete vertices
    for key in keys_del:
        del mesh.vertex[key]

    # sanitize affected faces
    new_faces = {}
    for fkey in mesh.faces():
        face = []
        seen = set()
        for key in mesh.face_vertices(fkey):
            if key in keys_pointer:
                pointer = keys_pointer[key]
                if pointer not in seen:
                    face.append(pointer)
                    seen.add(pointer)
            else:
                face.append(key)
        if seen:
            new_faces[fkey] = face

    for fkey in new_faces:
        del mesh.face[fkey]
        mesh.add_face(new_faces[fkey], fkey)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    

    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter

    vertices = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (10.0, 10.0, 0.0), (0.0, 10.0, 0.0), (5.0, 5.0, 0.0), (5.0, 5.0, 0.0)]
    faces = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 5]]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)


   

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_edges(width=0.5)

    print("Original mesh:")
    print(mesh)
    
    mesh_cull_duplicate_vertices(mesh)

    print("Mesh with duplicate vertices deleted:")
    print(mesh)
    #plotter.update(pause=2.0)
    plotter.show()

