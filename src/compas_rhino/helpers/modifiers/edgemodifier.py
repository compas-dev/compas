from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

import compas_rhino

try:
    import Rhino
    from Rhino.Geometry import Point3d

except ImportError:
    import sys
    if 'ironpython' in sys.version.lower():
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'EdgeModifier',
]


class EdgeModifier(object):

    @staticmethod
    def move_edge(self, key, constraint=None, allow_off=None):
        raise NotImplementedError

    @staticmethod
    def update_edge_attributes(self, keys, names=None):
        if not names:
            names = self.default_edge_attributes.keys()

        names = sorted(names)

        u, v = keys[0]
        values = [self.edge[u][v][name] for name in names]

        if len(keys) > 1:
            for i, name in enumerate(names):
                for u, v in keys[1:]:
                    if values[i] != self.edge[u][v][name]:
                        values[i] = '-'
                        break

        values = map(str, values)
        values = compas_rhino.update_named_values(names, values)

        if values:
            for name, value in zip(names, values):
                if value != '-':
                    for u, v in keys:
                        try:
                            self.edge[u][v][name] = ast.literal_eval(value)
                        except (ValueError, TypeError):
                            self.edge[u][v][name] = value
            return True

        return False


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network
    from compas_rhino.helpers.artists.networkartist import NetworkArtist
    from compas_rhino.helpers.modifiers.edgemodifier import EdgeModifier

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
