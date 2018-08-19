from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
from compas.utilities import color_to_colordict

__all__ = ['FaceArtist']


class FaceArtist(object):

    def clear_faces(self, keys=None):
        """Clear all faces previously drawn by the ``FaceArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of faces that should be cleared.
            Default is to clear all faces.

        """
        data = self.objects['faces']
        if not keys:
            data.clear()
        else:
            for key in keys:
                if key in data:
                    del data[key]

    def clear_facelabels(self, keys=None):
        """Clear all face labels previously drawn by the ``FaceArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of face labels that should be cleared.
            Default is to clear all face labels.

        """
        pass

    def draw_faces(self, fkeys=None, color=None, join_faces=False):
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

        """
        data = self.objects['faces']
        fkeys = fkeys or list(self.datastructure.faces())
        colordict = color_to_colordict(color,
                                       fkeys,
                                       default=self.datastructure.attributes.get('color.face'),
                                       colorformat='rgb',
                                       normalize=False)

        for fkey in fkeys:
            data[fkey] = {
                'points': self.datastructure.face_coordinates(fkey),
                'name'  : self.datastructure.face_name(fkey),
                'color' : colordict[fkey],
            }

        return data

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
            the default face color (``self.datastructure.attributes['color.face']``).

        """
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
