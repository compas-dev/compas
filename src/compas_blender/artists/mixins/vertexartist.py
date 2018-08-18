from compas.utilities import valuedict

from compas_blender.utilities import delete_objects
from compas_blender.utilities import get_objects
from compas_blender.utilities import xdraw_cubes
from compas_blender.utilities import xdraw_labels


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['VertexArtist']


class VertexArtist(object):

    def clear_vertices(self, keys=None):
        if not keys:
            keys = list(self.datastructure.vertices())
        objects = []
        for key in keys:
            name = self.datastructure.vertex_name(key)
            object = get_objects(name=name)
            if object:
                objects.append(object)
            name = 'V{0}'.format(key)
            object = get_objects(name=name)
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def clear_vertexlabels(self, keys=None):
        if not keys:
            keys = list(self.datastructure.vertices())
        objects = []
        for key in keys:
            name = 'V{0}'.format(key)
            object = get_objects(name=name)
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def draw_vertices(self, radius=0.010, keys=None, color=None):
        keys = keys or list(self.datastructure.vertices())
        colordict = valuedict(keys, color, self.defaults['color.vertex'])
        points = []
        for key in keys:
            points.append({
                'pos': self.datastructure.vertex_coordinates(key),
                'name': self.datastructure.vertex_name(key),
                'color': colordict[key],
                'layer': self.layer,
                'radius': radius})
        return xdraw_cubes(points)

    def draw_vertexlabels(self, text=None, ds=0.0):
        if text is None:
            keys = self.datastructure.vertices()
            textdict = {key: 'V{0}'.format(key) for key in keys}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        labels = []
        for key, text in iter(textdict.items()):
            xyz = self.datastructure.vertex_coordinates(key)
            labels.append({
                'pos': [i + ds for i in xyz],
                'name': textdict[key],
                'layer': self.layer})
        return xdraw_labels(labels)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
