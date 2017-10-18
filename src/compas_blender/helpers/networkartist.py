from compas.cad import ArtistInterface

from compas.utilities import to_valuedict

from compas_blender.utilities import clear_layer
from compas_blender.utilities import delete_objects
from compas_blender.utilities import xdraw_cubes
from compas_blender.utilities import xdraw_labels
from compas_blender.utilities import xdraw_lines

import time

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['NetworkArtist']


class NetworkArtist(ArtistInterface):
    """"""

    def __init__(self, network, layer=None):
        self.network = network
        self.layer = layer
        self.defaults = {
            'vertex.color': (1, 0, 0),
            'edge.color': (0, 0, 1)}

    def redraw(self, timeout=None):
        """Redraw the Blender view."""
        if timeout:
            time.sleep(timeout)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def clear_layer(self):
        if self.layer:
            clear_layer(layer=self.layer)

    def clear(self):
        self.clear_vertices()
        self.clear_edges()

    def clear_vertices(self, keys=None):
        if not keys:
            keys = list(self.network.vertices())
        objects = []
        for key in keys:
            name = self.network.vertex_name(key)
            object = get_objects(name=name)[0]
            if object:
                objects.append(object)
            name = 'V{0}'.format(key)
            object = get_objects(name=name)[0]
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def clear_edges(self, keys=None):
        if not keys:
            keys = list(self.network.edges())
        objects = []
        for u, v in keys:
            name = self.network.edge_name(u, v)
            object = get_objects(name=name)[0]
            if object:
                objects.append(object)
            name = 'E{0}-{1}'.format(u, v)
            object = get_objects(name=name)[0]
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def draw_vertices(self, radius=0.010, keys=None, color=None):
        keys = keys or list(self.network.vertices())
        colordict = to_valuedict(keys, color, self.defaults['vertex.color'])
        points = []
        for key in keys:
            points.append({
                'pos':    self.network.vertex_coordinates(key),
                'name':   self.network.vertex_name(key),
                'color':  colordict[key],
                'layer':  self.layer,
                'radius': radius
            })
        return xdraw_cubes(points)

    def draw_edges(self, width=0.010, keys=None, color=None):
        keys = keys or list(self.network.edges())
        colordict = to_valuedict(keys, color, self.defaults['edge.color'])
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.network.vertex_coordinates(u),
                'end': self.network.vertex_coordinates(v),
                'color': colordict[(u, v)],
                'name': self.network.edge_name(u, v),
                'width': width,
                'layer': self.layer
            })
        return xdraw_lines(lines)

    def draw_path(self, path):
        raise NotImplementedError

    def draw_vertexlabels(self, text=None, ds=0.0):
        if text is None:
            textdict = {key: 'V{0}'.format(key) for key in self.network.vertices()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        vlabels = []
        for key, text in iter(textdict.items()):
            xyz = self.network.vertex_coordinates(key)
            vlabels.append({
                'pos': [i + ds for i in xyz],
                'name': textdict[key],
                'layer': self.layer
            })
        return xdraw_labels(vlabels)

    def draw_edgelabels(self, text=None, ds=0.0):
        if text is None:
            textdict = {(u, v): 'E{}-{}'.format(u, v) for u, v in self.network.edges()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        elabels = []
        for (u, v), text in iter(textdict.items()):
            xyz = self.network.edge_midpoint(u, v)
            elabels.append({
                'pos': [i + ds for i in xyz],
                'name': textdict[(u, v)],
                'layer': self.layer
            })
        return xdraw_labels(elabels)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas_blender.utilities import get_objects
    from compas_blender.helpers import network_from_bmesh

    bmesh = get_objects(layer=0)[0]
    network = network_from_bmesh(bmesh=bmesh)
    networkartist = NetworkArtist(network=network, layer=1)

    networkartist.draw_vertices(radius=0.010)
    networkartist.draw_vertexlabels()
    networkartist.clear_vertices(keys=[6])

    networkartist.draw_edges(width=0.010)
    networkartist.draw_edgelabels()
    networkartist.clear_edges(keys=[(7, 6)])
