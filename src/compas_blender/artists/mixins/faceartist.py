
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.utilities import set_objects_show_names
from compas_blender.utilities import xdraw_mesh


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'FaceArtist',
]


class FaceArtist(object):

    __module__ = "compas_blender.artists.mixins"

    def clear_faces(self, keys=None):

        pass


    def clear_facelabels(self, keys=None):

        set_objects_show_names(objects=self.face_objects, show=False)


    def draw_faces(self, keys=None, colors=None, join_faces=False):

        self.clear_faces()
        self.clear_facelabels()

        keys = keys or list(self.datastructure.faces())

        if colors is None:
            colors = {key: self.defaults['color.face'] for key in keys}

        objects = [0] * len(keys)

        for c, key in enumerate(keys):

            mesh = xdraw_mesh(
                name='F{0}'.format(key),
                vertices=[self.datastructure.vertex_coordinates(i) for i in self.datastructure.face[key]],
                faces=[list(range(len(self.datastructure.face[key])))],
                color=colors[key],
                layer=self.layer,
            )

            objects[c] = mesh

        self.face_objects = objects


    def draw_facelabels(self, text=None, color=None):

        set_objects_show_names(objects=self.face_objects, show=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
