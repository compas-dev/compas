from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

try:
    import rhinoscriptsyntax as rs
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


class NetworkSelector(object):

    def __init__(self, network):
        self.network = network

    def select_vertex(self, message="Select a vertex."):
        guid = rs.GetObject(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
        if guid:
            prefix = self.network.attributes['name']
            name = rs.ObjectName(guid).split('.')
            if 'vertex' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    return ast.literal_eval(key)
        return None

    def select_vertices(self, message="Select vertices."):
        keys = []
        guids = rs.GetObjects(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
        if guids:
            prefix = self.network.attributes['name']
            seen = set()
            for guid in guids:
                name = rs.ObjectName(guid).split('.')
                if 'vertex' in name:
                    if not prefix or prefix in name:
                        key = name[-1]
                        if not seen.add(key):
                            key = ast.literal_eval(key)
                            keys.append(key)
        return keys

    def select_edge(self, message="Select an edge."):
        guid = rs.GetObject(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
        if guid:
            prefix = self.network.attributes['name']
            name = rs.ObjectName(guid).split('.')
            if 'edge' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    u, v = key.split('-')
                    u = ast.literal_eval(u)
                    v = ast.literal_eval(v)
                    return u, v
        return None

    def select_edges(self, message="Select edges."):
        keys = []
        guids = rs.GetObjects(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
        if guids:
            prefix = network.attributes['name']
            seen = set()
            for guid in guids:
                name = rs.ObjectName(guid).split('.')
                if 'edge' in name:
                    if not prefix or prefix in name:
                        key = name[-1]
                        if not seen.add(key):
                            u, v = key.split('-')
                            u = ast.literal_eval(u)
                            v = ast.literal_eval(v)
                            keys.append((u, v))
        return keys


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Network
    from compas_rhino.helpers.artists.networkartist import NetworkArtist
    from compas_rhino.helpers.selectors.networkselector import NetworkSelector
    from compas_rhino.helpers.modifiers.networkmodifier import NetworkModifier

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    artist = NetworkArtist(network)
    selector = NetworkSelector(network)
    modifier = NetworkModifier(network)

    artist.draw_vertices()
    artist.draw_edges()

    # 'update_view' would make more sense
    artist.redraw()

    key = selector.select_vertex()
    modifier.move_vertex(key)

    # would be better if the following could be replaced by a call to 'redraw'

    # should this then be 'clear_view'?
    artist.clear()

    artist.draw_vertices()
    artist.draw_edges()
