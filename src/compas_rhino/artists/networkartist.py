from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial
import compas_rhino

from compas.geometry import centroid_points
from compas.utilities import color_to_colordict

from ._artist import RhinoArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


class NetworkArtist(RhinoArtist):
    """Artist for drawing network data structures.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A COMPAS network.
    layer : str, optional
        The parent layer of the network.
    """

    def __init__(self, network, layer=None):
        super(NetworkArtist, self).__init__(network)
        self.layer = layer

    def clear_by_name(self):
        """Clear all objects in the "namespace" of the associated network."""
        guids = compas_rhino.get_objects(name="{}.*".format(self.network.name))
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self, nodes=None, edges=None, nodecolor=None, edgecolor=None):
        """Draw the network using the chosen visualisation settings.

        Parameters
        ----------
        nodes : list, optional
            A list of nodes to draw.
            Default is ``None``, in which case all nodes are drawn.
        edges : list, optional
            A list of edges to draw.
            The default is ``None``, in which case all edges are drawn.
        nodecolor : tuple or dict of tuple, optional
            The color specififcation for the nodes.
            The default color is the value of ``~NetworkArtist.default_nodecolor``.
        edgecolor : tuple or dict of tuple, optional
            The color specififcation for the edges.
            The default color is the value of ``~NetworkArtist.default_edgecolor``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        guids = self.draw_nodes()
        guids += self.draw_edges()
        return guids

    def draw_nodes(self, nodes=None, color=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list, optional
            A list of nodes to draw.
            Default is ``None``, in which case all nodes are drawn.
        color : tuple or dict of tuple, optional
            The color specififcation for the nodes.
            The default color is the value of ``~NetworkArtist.default_nodecolor``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        self.node_color = color
        node_xyz = self.node_xyz
        nodes = nodes or list(self.network.nodes())
        points = []
        for node in nodes:
            points.append({
                'pos': node_xyz[node],
                'name': "{}.node.{}".format(self.network.name, node),
                'color': self.node_color.get(node, self.default_nodecolor)
            })
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list, optional
            A list of edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : tuple or dict of tuple, optional
            The color specififcation for the edges.
            The default color is the value of ``~NetworkArtist.default_edgecolor``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        self.edge_color = color
        node_xyz = self.node_xyz
        edges = edges or list(self.network.edges())
        lines = []
        for edge in edges:
            lines.append({
                'start': node_xyz[edge[0]],
                'end': node_xyz[edge[1]],
                'color': self.edge_color.get(edge, self.default_edgecolor),
                'name': "{}.edge.{}-{}".format(self.network.name, *edge)
            })
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_nodelabels(self, text=None, color=None):
        """Draw labels for a selection nodes.

        Parameters
        ----------
        text : dict, optional
            A dictionary of node labels as node-text pairs.
            The default value is ``None``, in which case every node will be labelled with its key.
        color : 3-tuple or dict of 3-tuple, optional
            The color sepcification of the labels.
            The default color is the same as the default color of the nodes.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if not text or text == 'key':
            node_text = {node: str(node) for node in self.network.nodes()}
        elif text == 'index':
            node_text = {node: str(index) for index, node in enumerate(self.network.nodes())}
        elif isinstance(text, dict):
            node_text = text
        else:
            raise NotImplementedError
        node_xyz = self.node_xyz
        node_color = colordict(color, node_text.keys(), default=self.color_nodes)
        labels = []
        for node in node_text:
            labels.append({
                'pos': node_xyz[node],
                'name': "{}.nodelabel.{}".format(self.network.name, node),
                'color': node_color[node],
                'text': node_text[node]})
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict, optional
            A dictionary of edgelabels as edge-text pairs.
            The default value is ``None``, in which case every edge will be labelled with its key.
        color : 3-tuple or dict of 3-tuple, optional
            The color sepcification of the labels.
            The default color is the same as the default color of the edges.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if text is None:
            edge_text = {edge: "{}-{}".format(*edge) for edge in self.network.edges()}
        elif isinstance(text, dict):
            edge_text = text
        else:
            raise NotImplementedError
        node_xyz = self.node_xyz
        edge_color = colordict(color, edge_text.keys(), default=self.color_edges)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([node_xyz[edge[0]], node_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.network.name, *edge),
                'color': edge_color[edge],
                'text': edge_text[edge]})
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
