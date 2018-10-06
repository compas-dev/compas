from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import color_to_colordict

import compas_rhino


__all__ = ['EdgeArtist']


class EdgeArtist(object):

    __module__ = "compas_rhino.artists.mixins"

    def clear_edges(self, keys=None):
        """Clear all edges previously drawn by the ``EdgeArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of edges that should be cleared.
            Default is to clear all edges.

        """
        if not keys:
            name = '{}.edge.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for u, v in keys:
                name = self.datastructure.edge_name(u, v)
                guid = compas_rhino.get_object(name=name)
                guids.append(guid)
        compas_rhino.delete_objects(guids)

    def clear_edgelabels(self, keys=None):
        """Clear all edge labels previously drawn by the ``EdgeArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of edges of which the labels should be cleared.
            Default is to clear all edge labels.

        """
        if not keys:
            name = '{}.edge.label.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = self.datastructure.edge_label_name(key)
                guid = compas_rhino.get_object(name=name)
                guids.append(guid)
        compas_rhino.delete_objects(guids)

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
            color (``self.defaults['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        Notes
        -----
        All edges are named using the following template:
        ``"{}.edge.{}-{}".fromat(self.datastructure.name, u, v)``.
        This name is used afterwards to identify edges in the Rhino model.

        """
        keys = keys or list(self.datastructure.edges())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.defaults.get('color.edge'),
                                       colorformat='rgb',
                                       normalize=False)
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.datastructure.vertex_coordinates(u),
                'end'  : self.datastructure.vertex_coordinates(v),
                'color': colordict[(u, v)],
                'name' : self.datastructure.edge_name(u, v),
                'layer': self.datastructure.get_edge_attribute((u, v), 'layer', None)
            })

        return compas_rhino.xdraw_lines(lines, layer=self.layer, clear=False, redraw=False)

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
            color (``self.defaults['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        Notes
        -----
        All labels are assigned a name using the folling template:
        ``"{}.edge.{}".format(self.datastructure.name, key)``.

        """
        if text is None:
            textdict = {(u, v): "{}-{}".format(u, v) for u, v in self.datastructure.edges()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.defaults.get('color.edge'),
                                       colorformat='rgb',
                                       normalize=False)
        labels = []

        for (u, v), text in iter(textdict.items()):
            labels.append({
                'pos'  : self.datastructure.edge_midpoint(u, v),
                'name' : self.datastructure.edge_label_name(u, v),
                'color': colordict[(u, v)],
                'text' : textdict[(u, v)],
                'layer': self.datastructure.get_edge_attribute((u, v), 'layer', None)
            })

        return compas_rhino.xdraw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
