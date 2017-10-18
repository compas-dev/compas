from compas.utilities import color_to_colordict

import compas_rhino


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['FaceArtist']


class FaceArtist(object):

    def clear_faces(self, keys=None):
        if not keys:
            name = '{}.face.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = self.datastructure.face_name(key)
                guid = compas_rhino.get_object(name=name)
                guids.append(guid)
        compas_rhino.delete_objects(guids)

    def draw_faces(self, fkeys=None, color=None):
        """Draw a selection of faces of the mesh.

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
            default vertex color.

        Notes
        -----
        The faces are named using the following template:
        ``"{}.face.{}".format(self.datastructure.attributes['name'], key)``.
        This name is used afterwards to identify faces of the mesh in the Rhino model.

        Examples
        --------
        >>>

        """
        fkeys = fkeys or list(self.datastructure.faces())
        colordict = color_to_colordict(color,
                                       fkeys,
                                       default=self.defaults['color.face'],
                                       colorformat='rgb',
                                       normalize=False)
        faces = []
        for fkey in fkeys:
            faces.append({
                'points': self.datastructure.face_coordinates(fkey),
                'name'  : self.datastructure.face_name(fkey),
                'color' : colordict[fkey],
            })
        return compas_rhino.xdraw_faces(faces, layer=self.layer, clear=False, redraw=False)

    def draw_facelabels(self, text=None, color=None):
        """Draw labels for selected faces of the mesh.

        Parameters
        ----------

        Notes
        -----

        Examples
        --------

        """
        if text is None:
            textdict = {key: str(key) for key in self.datastructure.faces()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.defaults['color.face'],
                                       colorformat='rgb',
                                       normalize=False)

        labels = []
        for key, text in iter(textdict.items()):
            labels.append({
                'pos'  : self.datastructure.face_center(key),
                'name' : self.datastructure.face_name(key),
                'color': colordict[key],
                'text' : textdict[key],
            })
        return compas_rhino.xdraw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
