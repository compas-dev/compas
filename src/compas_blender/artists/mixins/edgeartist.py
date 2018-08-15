from compas.utilities import valuedict

from compas_blender.utilities import delete_objects
from compas_blender.utilities import get_objects
from compas_blender.utilities import xdraw_lines
from compas_blender.utilities import xdraw_labels


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['EdgeArtist']


class EdgeArtist(object):

    def clear_edges(self, keys=None):
        if not keys:
            keys = list(self.datastructure.edges())
        objects = []
        for u, v in keys:
            name = self.datastructure.edge_name(u, v)
            object = get_objects(name=name)
            if object:
                objects.append(object)
            name = 'E{0}-{1}'.format(u, v)
            object = get_objects(name=name)
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def clear_edgelabels(self, keys=None):
        if not keys:
            keys = list(self.datastructure.edges())
        objects = []
        for u, v in keys:
            name = 'E{0}-{1}'.format(u, v)
            object = get_objects(name=name)
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def draw_edges(self, width=0.010, keys=None, color=None):
        keys = keys or list(self.datastructure.edges())
        colordict = valuedict(keys, color, self.defaults['color.edge'])
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.datastructure.vertex_coordinates(u),
                'end': self.datastructure.vertex_coordinates(v),
                'color': colordict[(u, v)],
                'name': self.datastructure.edge_name(u, v),
                'width': width,
                'layer': self.layer})
        return xdraw_lines(lines)

    def draw_edgelabels(self, text=None, ds=0.0):
        if text is None:
            edges = self.datastructure.edges()
            textdict = {(u, v): 'E{}-{}'.format(u, v) for u, v in edges}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        labels = []
        for (u, v), text in iter(textdict.items()):
            xyz = self.datastructure.edge_midpoint(u, v)
            labels.append({
                'pos': [i + ds for i in xyz],
                'name': textdict[(u, v)],
                'layer': self.layer})
        return xdraw_labels(labels)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
