from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities import color_to_colordict

__all__ = ['VertexArtist']


class VertexArtist(object):

    def clear_vertices(self, keys=None):
        """Clear all vertices previously drawn by the ``VertexArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of vertices that should be cleared.
            Default is to clear all vertices.

        """
        data = self.objects['vertices']
        if not keys:
            data.clear()
        else:
            for key in keys:
                if key in data:
                    del data[key]

    def clear_vertexlabels(self, keys=None):
        """Clear all vertex labels previously drawn by the ``VertexArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of vertex labels that should be cleared.
            Default is to clear all vertex labels.

        """
        pass

    def draw_vertices(self, keys=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        keys : list
            A list of vertex keys identifying which vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : str, tuple, dict
            The color specififcation for the vertices.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all vertices, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default vertex
            color (``self.datastructure.attributes['color.vertex']``).
            The default is ``None``, in which case all vertices are assigned the
            default vertex color.

        """
        data = self.objects['vertices']
        keys = keys or list(self.datastructure.vertices())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.datastructure.attributes.get('color.vertex'),
                                       colorformat='rgb',
                                       normalize=False)
        for key in keys:
            data[key] = {
                'pos'   : self.datastructure.vertex_coordinates(key),
                'name'  : self.datastructure.vertex_name(key),
                'color' : colordict[key],
            }

        return data

    def draw_vertexlabels(self, text=None, color=None):
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict
            A dictionary of vertex labels as key-text pairs.
            The default value is ``None``, in which case every vertex will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            If a dictionary of specififcations is provided, the keys of the
            should refer to vertex keys and the values should be color
            specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned
            the default vertex color (``self.datastructure.attributes['color.vertex']``).

        """
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
