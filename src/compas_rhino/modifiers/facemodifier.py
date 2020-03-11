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


__all__ = [
    'FaceModifier',
    'mesh_update_face_attributes'
]


class FaceModifier(object):

    @staticmethod
    def move_face(self, key, constraint=None, allow_off=None):
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs = [self.face_coordinates(nbr) for nbr in self.face_neighbors(key)]
        nbrs = [Point3d(*xyz) for xyz in nbrs]

        def OnDynamicDraw(sender, e):
            for ep in nbrs:
                sp = e.CurrentPoint
                e.Display.DrawDottedLine(sp, ep, color)

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Point to move to?')
        gp.DynamicDraw += OnDynamicDraw

        if constraint:
            if allow_off is not None:
                gp.Constrain(constraint, allow_off)
            else:
                gp.Constrain(constraint)

        gp.Get()

        if gp.CommandResult() == Rhino.Commands.Result.Success:
            pos = list(gp.Point())
            self.face_attributes(key, 'xyz', pos)
            return True
        return False

    @staticmethod
    def update_face_attributes(self, keys, names=None):
        if not names:
            names = self.default_face_attributes.keys()
        names = sorted(names)

        values = self.face_attributes(keys[0], names)

        if len(keys) > 1:
            for i, name in enumerate(names):
                for key in keys[1:]:
                    if values[i] != self.face_attribute(key, name):
                        values[i] = '-'
                        break

        values = map(str, values)
        values = compas_rhino.update_named_values(names, values)

        if values:
            for name, value in zip(names, values):
                if value != '-':
                    for key in keys:
                        try:
                            self.face_attribute(key, name, ast.literal_eval(value))
                        except (ValueError, TypeError):
                            self.face_attribute(key, name, value)
            return True

        return False


def mesh_update_face_attributes(mesh, fkeys, names=None):
    """Update the attributes of the faces of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    fkeys : tuple, list
        The keys of the faces to update.
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
    * :func:`mesh_update_edge_attributes`

    """
    return FaceModifier.update_vertex_attributes(mesh, fkeys, names=names)

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

    if FaceModifier.move_face(network, 0):
        artist.clear()
        artist.draw_vertices()
        artist.draw_edges()
        artist.redraw()
