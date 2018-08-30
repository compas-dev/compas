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


__all__ = ['Modifier']


class Modifier(object):

    @staticmethod
    def move(self):
        color  = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        origin = {key: self.vertex_coordinates(key) for key in self.self.vertices()}
        vertex = {key: self.vertex_coordinates(key) for key in self.self.vertices()}
        edges  = self.edges()
        start  = compas_rhino.pick_point('Point to move from?')

        if not start:
            return False

        def OnDynamicDraw(sender, e):
            current = list(e.CurrentPoint)
            vec = [current[i] - start[i] for i in range(3)]
            for key in vertex:
                vertex[key] = [origin[key][i] + vec[i] for i in range(3)]
            for u, v in iter(edges):
                sp = vertex[u]
                ep = vertex[v]
                sp = Point3d(*sp)
                ep = Point3d(*ep)
                e.Display.DrawDottedLine(sp, ep, color)

        # name = '{0}.*'.format(self.attributes['name'])
        # guids = compas_rhino.get_objects(name=name)
        # compas_rhino.delete_objects(guids, False)

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Point to move to?')
        gp.DynamicDraw += OnDynamicDraw

        gp.Get()

        if gp.CommandResult() == Rhino.Commands.Result.Success:
            end = list(gp.Point())
            vec = [end[i] - start[i] for i in range(3)]
            for key, attr in self.vertices(True):
                attr['x'] += vec[0]
                attr['y'] += vec[1]
                attr['z'] += vec[2]
            return True
        return False

    @staticmethod
    def update_attributes(self):
        names  = sorted(self.attributes.keys())
        values = [str(self.attributes[name]) for name in names]
        values = compas_rhino.update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                try:
                    self.attributes[name] = ast.literal_eval(value)
                except (ValueError, TypeError):
                    self.attributes[name] = value
            return True
        return False


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    # from compas.datastructures import Network
    # from compas_rhino.artists.networkartist import NetworkArtist
    # from compas_rhino.modifiers.networkmodifier import NetworkModifier

    # network = Network.from_obj(compas.get('grid_irregular.obj'))

    # artist = NetworkArtist(network)

    # artist.clear()
    # artist.draw_vertices()
    # artist.draw_edges()
    # artist.redraw()

    # if NetworkModifier.move_vertex(network, 0):
    #     artist.clear()
    #     artist.draw_vertices()
    #     artist.draw_edges()
    #     artist.redraw()
