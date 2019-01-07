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


__all__ = ['FaceModifier']


class FaceModifier(object):

    @staticmethod
    def move_face(self, key, constraint=None, allow_off=None):
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs  = [self.face_coordinates(nbr) for nbr in self.face_neighbors(key)]
        nbrs  = [Point3d(*xyz) for xyz in nbrs]

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
            self.face[key]['x'] = pos[0]
            self.face[key]['y'] = pos[1]
            self.face[key]['z'] = pos[2]
            return True
        return False

    @staticmethod
    def update_face_attributes(self, keys, names=None):
        if not names:
            names = self.default_face_attributes.keys()
        names = sorted(names)

        values = [self.facedata[keys[0]][name] for name in names]

        if len(keys) > 1:
            for i, name in enumerate(names):
                for key in keys[1:]:
                    if values[i] != self.facedata[key][name]:
                        values[i] = '-'
                        break

        values = map(str, values)
        values = compas_rhino.update_named_values(names, values)

        if values:
            for name, value in zip(names, values):
                if value != '-':
                    for key in keys:
                        try:
                            self.facedata[key][name] = ast.literal_eval(value)
                        except (ValueError, TypeError):
                            self.facedata[key][name] = value
            return True

        return False


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network
    from compas_rhino.artists.networkartist import NetworkArtist
    from compas_rhino.modifiers.facemodifier import FaceModifier

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
