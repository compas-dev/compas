from compas.utilities import valuedict

from compas_blender.utilities import delete_objects
from compas_blender.utilities import get_objects
from compas_blender.utilities import xdraw_faces
from compas_blender.utilities import xdraw_labels


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['FaceArtist']


class FaceArtist(object):

    def clear_faces(self, keys=None):
        if not keys:
            keys = list(self.datastructure.faces())
        objects = []
        for key in keys:
            name = self.datastructure.face_name(key)
            object = get_objects(name=name)
            if object:
                objects.append(object)
            name = 'F{0}'.format(key)
            object = get_objects(name=name)
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def clear_facelabels(self, keys=None):
        if not keys:
            keys = list(self.datastructure.faces())
        objects = []
        for key in keys:
            name = 'F{0}'.format(key)
            object = get_objects(name=name)
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def draw_faces(self, fkeys=None, color=None, alpha=0.5):
        fkeys = fkeys or list(self.datastructure.faces())
        colordict = valuedict(fkeys, color, self.defaults['color.face'])
        faces = []
        for fkey in fkeys:
            faces.append({
                'name': self.datastructure.face_name(fkey),
                'points': self.datastructure.face_coordinates(fkey),
                'color': colordict[fkey],
                'layer': self.layer})
        return xdraw_faces(faces, alpha=alpha)

    def draw_facelabels(self, text=None, ds=0.0):
        if text is None:
            keys = self.datastructure.faces()
            textdict = {key: 'F{0}'.format(key) for key in keys}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        labels = []
        for key, text in iter(textdict.items()):
            xyz = self.datastructure.face_center(key)
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
