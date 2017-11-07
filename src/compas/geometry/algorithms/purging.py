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

    # this doesn't seem to do anything
    # is the same as geo_keys.values()
    keys_remain = [geo_keys[geo_key] for geo_key in geo_keys]
    keys_del = [key for key in mesh.vertices() if key not in keys_remain]

    for key in keys_del:
        del mesh.vertex[key]

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
    pass
