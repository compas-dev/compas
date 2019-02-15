from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas.utilities import color_to_colordict

import compas_ghpython

try:
    import Rhino
except ImportError:
    compas.raise_if_ironpython()


__all__ = ['FaceArtist']


class FaceArtist(object):

    def draw_faces(self, keys=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        fkeys : list
            A list of face keys identifying which faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : str, tuple, dict
            The color specififcation for the faces.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all faces, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.defaults['face.color']``).
            The default is ``None``, in which case all faces are assigned the
            default face color.

        Notes
        -----
        The faces are named using the following template:
        ``"{}.face.{}".format(self.datastructure.name, key)``.

        """
        keys = keys or list(self.datastructure.faces())

        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.defaults.get('color.face'),
                                       colorformat='rgb',
                                       normalize=False)
        faces = []
        for fkey in keys:
            faces.append({
                'points': self.datastructure.face_coordinates(fkey),
                'name'  : self.datastructure.face_name(fkey),
                'color' : colordict[fkey],
                'layer' : self.datastructure.get_face_attribute(fkey, 'layer', None)
            })

        meshes = compas_ghpython.xdraw_faces(faces)
        if not join_faces:
            return meshes
        else:
            joined_mesh = Rhino.Geometry.Mesh()
            [joined_mesh.Append(mesh) for mesh in meshes]
            return joined_mesh

    def draw_facelabels(self, text=None, color=None):
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict
            A dictionary of face labels as key-text pairs.
            The default value is ``None``, in which case every face will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            If a dictionary of specififcations is provided, the keys of the
            should refer to face keys and the values should be color
            specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned
            the default face color (``self.defaults['color.face']``).

        Notes
        -----
        The face labels are named using the following template:
        ``"{}.face.label.{}".format(self.datastructure.name, key)``.
        This name is used afterwards to identify faces and face labels in the Rhino model.

        """
        if text is None:
            textdict = {key: str(key) for key in self.datastructure.faces()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.defaults.get('color.face'),
                                       colorformat='rgb',
                                       normalize=False)

        labels = []
        for key, text in iter(textdict.items()):
            labels.append({
                'pos'   : self.datastructure.face_center(key),
                'name'  : "{}.face.label.{}".format(self.datastructure.name, key),
                'color' : colordict[key],
                'text'  : textdict[key],
                'layer' : self.datastructure.get_face_attribute(key, 'layer', None)
            })
        return compas_ghpython.xdraw_labels(labels)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
