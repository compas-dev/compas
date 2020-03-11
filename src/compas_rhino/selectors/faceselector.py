from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

import compas

try:
    import rhinoscriptsyntax as rs
except ImportError:
    compas.raise_if_ironpython()


__all__ = [
    'FaceSelector',

    'mesh_select_faces',
    'mesh_select_face',

    'volmesh_select_faces',
    'volmesh_select_face'
    ]


class FaceSelector(object):

    @staticmethod
    def select_face(self, message="Select a face."):
        guid = rs.GetObject(message, preselect=True, filter=rs.filter.mesh | rs.filter.textdot)
        if guid:
            prefix = self.attributes['name']
            name = rs.ObjectName(guid).split('.')
            if 'face' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    key = ast.literal_eval(key)
                    return key
        return None

    @staticmethod
    def select_faces(self, message="Select faces."):
        keys = []
        guids = rs.GetObjects(message, preselect=True, filter=rs.filter.mesh | rs.filter.textdot)
        if guids:
            prefix = self.attributes['name']
            seen = set()
            for guid in guids:
                name = rs.ObjectName(guid).split('.')
                if 'face' in name:
                    if not prefix or prefix in name:
                        key = name[-1]
                        if not seen.add(key):
                            key = ast.literal_eval(key)
                            keys.append(key)
        return keys


def mesh_select_faces(mesh, message='Select mesh faces.'):
    """Select faces of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    message : str ("Select mesh faces.")
        The message to display to the user.

    Returns
    -------
    list
        The keys of the selected faces.

    See Also
    --------
    * :func:`mesh_select_vertices`
    * :func:`mesh_select_edges`

    """
    return FaceSelector.select_faces(mesh)


def mesh_select_face(mesh, message='Select face.'):
    """Select one face of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    message : str ("Select a mesh face.")
        The message to display to the user.

    Returns
    -------
    hashable
        The key of the selected face.

    See Also
    --------
    * :func:`mesh_select_faces`

    """
    return FaceSelector.select_face(mesh)


def volmesh_select_face(volmesh):
    """"""
    return FaceSelector.select_face(volmesh)


def volmesh_select_faces(volmesh):
    """"""
    return FaceSelector.select_faces(volmesh)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
