from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

import compas
import compas_rhino

try:
    import Rhino
    from Rhino.Geometry import Point3d

except ImportError:
    compas.raise_if_ironpython()

try:
    from compas_rhino.etoforms import PropertyListForm

except:
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
    'VertexModifier',

    'mesh_update_vertex_attributes',
    'mesh_move_vertex',
    'mesh_move_vertices',

    'network_move_vertex',
    'network_update_vertex_attributes'
    ]


def rhino_update_named_values(names, values, message='', title='Update named values'):
    try:
        dialog = PropertyListForm(names, values)
    except:
        values = ShowPropertyListBox(message, title, names, values)
    else:
        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            values = dialog.values
        else:
            values = None
    return values


class VertexModifier(object):

    @staticmethod
    def move_vertex(self, key, constraint=None, allow_off=None):
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs  = [self.vertex_coordinates(nbr) for nbr in self.vertex_neighbors(key)]
        nbrs  = [Point3d(*xyz) for xyz in nbrs]

        def OnDynamicDraw(sender, e):
            for ep in nbrs:
                sp = e.CurrentPoint
                e.Display.DrawDottedLine(sp, ep, color)

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Point to move to?')
        gp.DynamicDraw += OnDynamicDraw

        if constraint:
            gp.Constrain(constraint, allow_off)
        # else:
        #     gp.Constrain(constraint)

        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        pos = list(gp.Point())
        self.vertex[key]['x'] = pos[0]
        self.vertex[key]['y'] = pos[1]
        self.vertex[key]['z'] = pos[2]

        return True

    @staticmethod
    def move_vertices(self, keys):
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for key in keys:
            a = self.vertex_coordinates(key)
            nbrs = self.vertex_neighbors(key)
            for nbr in nbrs:
                b = self.vertex_coordinates(nbr)
                line = [Point3d(* a), Point3d(* b)]
                if nbr in keys:
                    lines.append(line)
                else:
                    connectors.append(line)

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt('Point to move from?')
        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        def OnDynamicDraw(sender, e):
            end = e.CurrentPoint
            vector = end - start
            for a, b in lines:
                a = a + vector
                b = b + vector
                e.Display.DrawDottedLine(a, b, color)
            for a, b in connectors:
                a = a + vector
                e.Display.DrawDottedLine(a, b, color)

        gp.SetCommandPrompt('Point to move to?')
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)

        gp.DynamicDraw += OnDynamicDraw

        gp.Get()

        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()

        vector = list(end - start)

        for key in keys:
            self.vertex[key]['x'] += vector[0]
            self.vertex[key]['y'] += vector[1]
            self.vertex[key]['z'] += vector[2]

        return True

    @staticmethod
    def update_vertex_attributes(self, keys, names=None):
        """Update the attributes of selected vertices of a given datastructure.

        Parameters
        ----------
        self : compas.datastructures.Datastructure
            The data structure.
        keys : list
            The keys of the vertices of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is to update all available attributes.

        Returns
        -------
        bool
            True if the attributes were successfully updated.
            False otherwise.

        """
        if not names:
            names = self.default_vertex_attributes.keys()
        names = sorted(names)
        values = [self.vertex[keys[0]][name] for name in names]
        if len(keys) > 1:
            for i, name in enumerate(names):
                for key in keys[1:]:
                    if values[i] != self.vertex[key][name]:
                        values[i] = '-'
                        break
        values = map(str, values)
        values = rhino_update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                if value != '-':
                    for key in keys:
                        try:
                            self.vertex[key][name] = ast.literal_eval(value)
                        except (ValueError, TypeError):
                            self.vertex[key][name] = value
            return True
        return False


def mesh_update_vertex_attributes(mesh, keys, names=None):
    """Update the attributes of the vertices of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    keys : tuple, list
        The keys of the vertices to update.
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
    * :func:`mesh_update_edge_attributes`
    * :func:`mesh_update_face_attributes`

    """
    return VertexModifier.update_vertex_attributes(mesh, keys, names=names)


def mesh_move_vertex(mesh, key, constraint=None, allow_off=False):
    """Move on vertex of the mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    key : str
        The vertex to move.
    constraint : Rhino.Geometry (None)
        A Rhino geometry object to constrain the movement to.
        By default the movement is unconstrained.
    allow_off : bool (False)
        Allow the vertex to move off the constraint.

    """
    return VertexModifier.move_vertex(mesh, key, constraint=constraint, allow_off=allow_off)


def mesh_move_vertices(mesh, keys):
    """Move on vertices of the mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    keys : list
        The vertices to move.
    constraint : Rhino.Geometry (None)
        A Rhino geometry object to constrain the movement to.
        By default the movement is unconstrained.
    allow_off : bool (False)
        Allow the vertex to move off the constraint.

    """
    return VertexModifier.move_vertices(mesh, keys)


def network_move_vertex(network, key, constraint=None, allow_off=False):
    """Move on vertex of the network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    key : str
        The vertex to move.
    constraint : Rhino.Geometry (None)
        A Rhino geometry object to constrain the movement to.
        By default the movement is unconstrained.
    allow_off : bool (False)
        Allow the vertex to move off the constraint.

    """
    return VertexModifier.move_vertex(network, key, constraint=constraint, allow_off=allow_off)


def network_update_vertex_attributes(network, keys, names=None):
    """Update the attributes of the vertices of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    keys : tuple, list
        The keys of the vertices to update.
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
    * :func:`network_update_edge_attributes`

    """
    return VertexModifier.update_vertex_attributes(network, keys, names=names)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network
    from compas_rhino.artists.networkartist import NetworkArtist
    from compas_rhino.modifiers.vertexmodifier import VertexModifier

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    artist = NetworkArtist(network)

    artist.clear()
    artist.draw_vertices()
    artist.draw_edges()
    artist.redraw()

    if VertexModifier.move_vertex(network, 0):
        artist.clear()
        artist.draw_vertices()
        artist.draw_edges()
        artist.redraw()
