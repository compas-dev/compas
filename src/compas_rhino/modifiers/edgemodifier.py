from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

import compas

try:
    import Rhino
except ImportError:
    compas.raise_if_ironpython()

try:
    from compas_rhino.etoforms import PropertyListForm
except ImportError:
    try:
        from Rhino.UI.Dialogs import ShowPropertyListBox
    except ImportError:
        compas.raise_if_ironpython()
else:
    try:
        import clr
        clr.AddReference('Rhino.UI')
        import Rhino.UI
    except ImportError:
        compas.raise_if_ironpython()


__all__ = [
    'EdgeModifier',
    'mesh_update_edge_attributes',
    'network_update_edge_attributes'
]


def rhino_update_named_values(names, values, message='', title='Update named values'):
    try:
        dialog = PropertyListForm(names, values)
    except Exception:
        values = ShowPropertyListBox(message, title, names, values)
    else:
        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            values = dialog.values
        else:
            values = None
    return values


class EdgeModifier(object):

    @staticmethod
    def move_edge(self, key, constraint=None, allow_off=None):
        raise NotImplementedError

    @staticmethod
    def update_edge_attributes(self, keys, names=None):
        if not names:
            names = self.default_edge_attributes.keys()
        names = sorted(names)

        key = keys[0]
        values = self.edge_attributes(key, names)

        if len(keys) > 1:
            for i, name in enumerate(names):
                for key in keys[1:]:
                    if values[i] != self.edge_attribute(key, name):
                        values[i] = '-'
                        break
        values = map(str, values)
        values = rhino_update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                if value != '-':
                    for key in keys:
                        try:
                            value = ast.literal_eval(value)
                        except (SyntaxError, ValueError, TypeError):
                            pass
                        self.edge_attribute(key, name, value)

            return True
        return False


def mesh_update_edge_attributes(mesh, keys, names=None):
    """Update the attributes of the edges of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    keys : tuple, list
        The keys of the edges to update.
    names : tuple, list (None)
        The names of the atrtibutes to update.
        Default is to update all attributes.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    See Also
    --------
    * :func:`mesh_update_attributes`
    * :func:`mesh_update_vertex_attributes`
    * :func:`mesh_update_face_attributes`

    """
    return EdgeModifier.update_edge_attributes(mesh, keys, names=names)


def network_update_edge_attributes(network, keys, names=None):
    """Update the attributes of the edges of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    keys : tuple, list
        The keys of the edges to update.
    names : tuple, list (None)
        The names of the atrtibutes to update.
        Default is to update all attributes.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    See Also
    --------
    * :func:`network_update_attributes`
    * :func:`network_update_vertex_attributes`

    """
    return EdgeModifier.update_edge_attributes(network, keys, names=names)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network
    from compas_rhino.artists.networkartist import NetworkArtist

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    artist = NetworkArtist(network)

    artist.clear()
    artist.draw_vertices()
    artist.draw_edges()
    artist.redraw()

    if EdgeModifier.move_edge(network, 0):
        artist.clear()
        artist.draw_vertices()
        artist.draw_edges()
        artist.redraw()
