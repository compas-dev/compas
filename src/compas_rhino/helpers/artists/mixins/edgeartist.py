from compas.utilities import color_to_colordict

import compas_rhino


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['EdgeArtist']


class EdgeArtist(object):

    def clear_edges(self, keys=None):
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
        pass

    def draw_edges(self, keys=None, color=None):
        """Draw a selection of edges of the network.

        Parameters
        ----------
        keys : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all faces, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.defaults['face.color']``).
            The default is ``None``, in which case all faces are assigned the
            default edge color.

        Notes
        -----
        All edges are named using the following template:
        ``"{}.edge.{}-{}".fromat(self.datastructure.name, u, v)``.
        This name is used afterwards to identify edges of the network in the Rhino model.

        Examples
        --------
        >>> artist.draw_edges()
        >>> artist.draw_edges(color='#ff0000')
        >>> artist.draw_edges(color=(255, 0, 0))
        >>> artist.draw_edges(keys=self.datastructure.edges_xxx())
        >>> artist.draw_edges(color={(u, v): '#00ff00' for u, v in self.datastructure.edges_xxx()})

        """
        keys = keys or list(self.datastructure.edges())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.defaults['color.edge'],
                                       colorformat='rgb',
                                       normalize=False)
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.datastructure.vertex_coordinates(u),
                'end'  : self.datastructure.vertex_coordinates(v),
                'color': colordict[(u, v)],
                'name' : self.datastructure.edge_name(u, v)
            })
        return compas_rhino.xdraw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for selected edges of the network.

        Parameters
        ----------
        text : dict
            A dictionary of edge labels as key-text pairs.
            The default value is ``None``, in which case every edge of the network
            will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            If a dictionary of specififcations is provided, the keys of the
            should refer to edge keys in the network and the values should be color
            specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned
            the default edge color (``self.defaults['color.edge']``).

        Notes
        -----
        All labels are assigned a name using the folling template:
        ``"{}.edge.{}".format(self.datastructure.name, key)``.

        Examples
        --------
        >>>

        """
        if text is None:
            textdict = {(u, v): "{}-{}".format(u, v) for u, v in self.datastructure.edges()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.defaults['color.edge'],
                                       colorformat='rgb',
                                       normalize=False)
        labels = []

        for (u, v), text in iter(textdict.items()):
            labels.append({
                'pos'  : self.datastructure.edge_midpoint(u, v),
                'name' : self.datastructure.edge_name(u, v),
                'color': colordict[(u, v)],
                'text' : textdict[(u, v)],
            })

        return compas_rhino.xdraw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
