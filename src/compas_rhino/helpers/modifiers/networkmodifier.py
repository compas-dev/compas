from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

try:
    import Rhino
    from Rhino.Geometry import Point3d
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'NetworkModifier',
]


class NetworkModifier(object):

    @staticmethod
    def move(self):
        color  = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        origin = {key: self.vertex_coordinates(key) for key in self.network.vertices()}
        vertex = {key: self.vertex_coordinates(key) for key in self.network.vertices()}
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
    def move_vertex(self, key, constraint=None, allow_off=None):
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs  = [self.vertex_coordinates(nbr) for nbr in self.vertex_neighbours(key)]
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
            self.vertex[key]['x'] = pos[0]
            self.vertex[key]['y'] = pos[1]
            self.vertex[key]['z'] = pos[2]
            return True
        return False


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network
    from compas_rhino.helpers.artists.networkartist import NetworkArtist
    from compas_rhino.helpers.modifiers.networkmodifier import NetworkModifier

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    artist = NetworkArtist(network)

    artist.clear()
    artist.draw_vertices()
    artist.draw_edges()
    artist.redraw()

    if NetworkModifier.move_vertex(network, 0):
        artist.clear()
        artist.draw_vertices()
        artist.draw_edges()
        artist.redraw()
