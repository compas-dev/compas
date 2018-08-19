from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities import color_to_colordict

__all__ = ['EdgeArtist']


class EdgeArtist(object):

    def clear_edges(self, keys=None):
        """Clear all edges previously drawn by the ``EdgeArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of edges that should be cleared.
            Default is to clear all edges.

        """
        data = self.objects['edges']
        if not keys:
            data.clear()
        else:
            for key in keys:
                if key in data:
                    del data[key]

    def clear_edgelabels(self, keys=None):
        """Clear all edge labels previously drawn by the ``EdgeArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of edges of which the labels should be cleared.
            Default is to clear all edge labels.

        """
        pass

    def draw_edges(self, keys=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        keys : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all edges, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.datastructure.attributes['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        """
        data = self.objects['edges']
        keys = keys or list(self.datastructure.edges())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.datastructure.attributes.get('color.edge'),
                                       colorformat='rgb',
                                       normalize=False)
        for key in keys:
            u, v = key
            data[key] = {
                'start': self.datastructure.vertex_coordinates(u),
                'end'  : self.datastructure.vertex_coordinates(v),
                'color': colordict[(u, v)],
                'name' : self.datastructure.edge_name(u, v),
            }

        return data

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict
            A dictionary of edge labels as key-text pairs.
            The default value is ``None``, in which case every edge will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.datastructure.attributes['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        """
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
