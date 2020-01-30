from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists import Artist

from compas.utilities import color_to_colordict


__all__ = ['NetworkArtist']


class NetworkArtist(Artist):
    """A network artist defines functionality for visualising COMPAS networks in Rhino.

    Parameters
    ----------
    network : compas.datastructures.Network
        A COMPAS network.
    layer : str, optional
        The name of the layer that will contain the network.

    Attributes
    ----------
    defaults : dict
        Default settings for color, scale, tolerance, ...

    """

    __module__ = "compas_rhino.artists"

    def __init__(self, network, layer=None):
        super(NetworkArtist, self).__init__(layer=layer)
        self.settings.update({
            'color.vertex': (255, 255, 255),
            'color.edge': (0, 0, 0),
        })

    @property
    def network(self):
        """compas.datastructures.Network: The network that should be painted."""
        return self.network

    @network.setter
    def network(self, network):
        self.network = network

    @classmethod
    def from_data(cls, data):
        module, attr = data['dtype'].split('/')
        Network = getattr(__import__(module, fromlist=[attr]), attr)
        network = Network.from_data(data['value'])
        artist = cls(network)
        return artist

    def to_data(self):
        return self.network.to_data()

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Clear the vertices and edges of the network, without clearing the
        other elements in the layer."""
        self.clear_vertices()
        self.clear_edges()
        self.clear_vertexlabels()
        self.clear_edgelabels()

    def clear_vertices(self, keys=None):
        """Clear all previously drawn vertices.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of vertices that should be cleared.
            Default is to clear all vertices.

        """
        if not keys:
            name = '{}.vertex.*'.format(self.network.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.vertex.{}'.format(self.network.name, key)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_edges(self, keys=None):
        """Clear all previously drawn edges.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of edges that should be cleared.
            Default is to clear all edges.

        """
        if not keys:
            name = '{}.edge.*'.format(self.network.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for u, v in keys:
                name = '{}.edge.{}-{}'.format(self.network.name, u, v)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_vertexlabels(self, keys=None):
        """Clear all previously drawn vertex labels.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of vertex labels that should be cleared.
            Default is to clear all vertex labels.

        """
        if not keys:
            name = '{}.vertex.label.*'.format(self.network.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.vertex.label.{}'.format(self.network.name, key)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_edgelabels(self, keys=None):
        """Clear all previously drawn edge labels.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of edges of which the labels should be cleared.
            Default is to clear all edge labels.

        """
        if not keys:
            name = '{}.edge.label.*'.format(self.network.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for u, v in keys:
                name = '{}.edge.label.{}-{}'.format(self.network.name, u, v)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    # ==========================================================================
    # components
    # ==========================================================================

    def draw(self, settings=None):
        raise NotImplementedError

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
            color (``self.settings['color.vertex']``).
            The default is ``None``, in which case all vertices are assigned the
            default vertex color.

        Notes
        -----
        The vertices are named using the following template:
        ``"{}.vertex.{}".format(self.network.name, key)``.
        This name is used afterwards to identify vertices in the Rhino model.

        """
        keys = keys or list(self.network.vertices())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings.get('color.vertex'),
                                       colorformat='rgb',
                                       normalize=False)
        points = []
        for key in keys:
            points.append({
                'pos': self.network.vertex_coordinates(key),
                'name': "{}.vertex.{}".format(self.network.name, key),
                'color': colordict[key],
                'layer': self.network.get_vertex_attribute(key, 'layer', None)
            })
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

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
            color (``self.settings['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        Notes
        -----
        All edges are named using the following template:
        ``"{}.edge.{}-{}".fromat(self.network.name, u, v)``.
        This name is used afterwards to identify edges in the Rhino model.

        """
        keys = keys or list(self.network.edges())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings.get('color.edge'),
                                       colorformat='rgb',
                                       normalize=False)
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.network.vertex_coordinates(u),
                'end': self.network.vertex_coordinates(v),
                'color': colordict[(u, v)],
                'name': "{}.edge.{}-{}".format(self.network.name, u, v),
                'layer': self.network.get_edge_attribute((u, v), 'layer', None)
            })

        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # ==========================================================================
    # labels
    # ==========================================================================

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
            the default vertex color (``self.settings['color.vertex']``).

        Notes
        -----
        All labels are assigned a name using the folling template:
        ``"{}.vertex.label.{}".format(self.network.name, key)``.

        """
        if text is None:
            textdict = {key: str(key) for key in self.network.vertices()}
        elif isinstance(text, dict):
            textdict = text
        elif text == 'key':
            textdict = {key: str(key) for key in self.network.vertices()}
        elif text == 'index':
            textdict = {key: str(index) for index, key in enumerate(self.network.vertices())}
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings.get('color.vertex'),
                                       colorformat='rgb',
                                       normalize=False)
        labels = []

        for key, text in iter(textdict.items()):
            labels.append({
                'pos': self.network.vertex_coordinates(key),
                'name': "{}.vertex.label.{}".format(self.network.name, key),
                'color': colordict[key],
                'text': textdict[key],
                'layer': self.network.get_vertex_attribute(key, 'layer', None)
            })

        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

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
            color (``self.settings['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        Notes
        -----
        All labels are assigned a name using the folling template:
        ``"{}.edge.{}".format(self.network.name, key)``.

        """
        if text is None:
            textdict = {(u, v): "{}-{}".format(u, v) for u, v in self.network.edges()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings.get('color.edge'),
                                       colorformat='rgb',
                                       normalize=False)
        labels = []

        for (u, v), text in iter(textdict.items()):
            labels.append({
                'pos': self.network.edge_midpoint(u, v),
                'name': "{}.edge.label.{}-{}".format(self.network.name, u, v),
                'color': colordict[(u, v)],
                'text': textdict[(u, v)],
                'layer': self.network.get_edge_attribute((u, v), 'layer', None)
            })

        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    artist = NetworkArtist(network)
    artist.clear()
    artist.draw_vertices()
    artist.draw_edges()
    artist.draw_vertexlabels(text='key')
    artist.draw_edgelabels(text={key: index for index, key in enumerate(network.edges())})
