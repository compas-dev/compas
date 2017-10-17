from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

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


class NetworkModifier(object):

    def __init__(self, network, artist=None):
        self.network = network
        self.artist = artist

    def move(self):
        pass

    def move_vertex(self, key, constraint=None, allow_off=None):
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs  = [self.network.vertex_coordinates(nbr) for nbr in self.network.vertex_neighbours(key)]
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
            self.network.vertex[key]['x'] = pos[0]
            self.network.vertex[key]['y'] = pos[1]
            self.network.vertex[key]['z'] = pos[2]

        if self.artist:
            self.artist.draw_vertices()
            self.artist.draw_edges()


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
    modifier = NetworkModifier(network)

    artist.draw_vertices()
    artist.draw_edges()

    # 'update_view' would make more sense
    artist.redraw()

    modifier.move_vertex(0)

    # would be better if the following could be replaced by a call to 'redraw'

    # should this then be 'clear_view'?
    artist.clear()

    artist.draw_vertices()
    artist.draw_edges()
