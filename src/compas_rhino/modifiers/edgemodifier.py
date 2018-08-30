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


__all__ = ['EdgeModifier']


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
        values = self.get_edge_attributes(key, names)

        if len(keys) > 1:
            for i, name in enumerate(names):
                for key in keys[1:]:
                    if values[i] != self.get_edge_attribute(key, name):
                        values[i] = '-'
                        break

        values = map(str, values)
        values = compas_rhino.update_named_values(names, values)

        if values:
            for name, value in zip(names, values):
                if value != '-':
                    for key in keys:
                        try:
                            value = ast.literal_eval(value)
                        except (SyntaxError, ValueError, TypeError):
                            pass
                        self.set_edge_attribute(key, name, value)

            return True
        return False


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network
    from compas_rhino.artists.networkartist import NetworkArtist
    from compas_rhino.modifiers.edgemodifier import EdgeModifier

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
