# from __future__ import annotations

from functools import partial

import compas_blender

from compas_blender.artists._artist import BaseArtist
from compas.utilities import color_to_colordict

colordict = partial(color_to_colordict, colorformat='rgb', normalize=True)


__all__ = [
    'NetworkArtist',
]


class NetworkArtist(BaseArtist):
    """Artist for COMPAS network objects.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A COMPAS network.
    settings : dict, optional
        A dict with custom visualisation settings.

    Attributes
    ----------
    network : :class:`compas.datastructures.Network`
        The COMPAS network associated with the artist.
    settings : dict
        Default settings for color, scale, tolerance, ...

    """

    def __init__(self, network):
        super().__init__()
        self._nodecollection = None
        self._edgecollection = None
        self._pathcollection = None
        self._object_node = {}
        self._object_edge = {}
        self._object_path = {}
        self.color_nodes = (1.0, 1.0, 1.0)
        self.color_edges = (0.0, 0.0, 0.0)
        self.show_nodes = True,
        self.show_edges = True,
        self.show_nodelabels = False,
        self.show_edgelabels = False
        self.network = network

    @property
    def nodecollection(self):
        path = f"{self.network.name}::Nodes"
        if not self._nodecollection:
            self._nodecollection = compas_blender.create_collections_from_path(path)[1]
        return self._nodecollection

    @property
    def edgecollection(self):
        path = f"{self.network.name}::Edges"
        if not self._edgecollection:
            self._edgecollection = compas_blender.create_collections_from_path(path)[1]
        return self._edgecollection

    @property
    def pathcollection(self):
        path = f"{self.network.name}::Paths"
        if not self._pathcollection:
            self._pathcollection = compas_blender.create_collections_from_path(path)[1]
        return self._pathcollection

    @property
    def object_node(self):
        if not self._object_node:
            self._object_node = {}
        return self._object_node

    @object_node.setter
    def object_node(self, values):
        self._object_node = dict(values)

    @property
    def object_edge(self):
        if not self._object_edge:
            self._object_edge = {}
        return self._object_edge

    @object_edge.setter
    def object_edge(self, values):
        self._object_edge = dict(values)

    @property
    def object_path(self):
        if not self._object_path:
            self._object_path = {}
        return self._object_path

    @object_path.setter
    def object_path(self, values):
        self._object_path = dict(values)

    def clear(self):
        objects = list(self.object_node)
        objects += list(self.object_edge)
        objects += list(self.object_path)
        compas_blender.delete_objects(objects, purge_data=True)
        self._object_node = {}
        self._object_edge = {}
        self._object_path = {}

    def draw(self):
        """Draw the network.

        Returns
        -------
        list of :class:`bpy.types.Object`
            The created Blender objects.

        """
        self.clear()
        if self.show_nodes:
            self.draw_nodes()
        if self.show_edges:
            self.draw_edges()
        return self.objects

    def draw_nodes(self, nodes=None, color=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list of int, optional
            A list of node identifiers.
            Default is ``None``, in which case all nodes are drawn.
        color : rgb-tuple or dict of rgb-tuples
            The color specififcation for the nodes.

        Returns
        -------
        list of :class:`bpy.types.Object`

        """
        nodes = nodes or list(self.network.nodes())
        node_color = colordict(color, nodes, default=self.color_nodes)
        points = []
        for node in nodes:
            points.append({
                'pos': self.network.node_coordinates(node),
                'name': f"{self.network.name}.node.{node}",
                'color': node_color[node],
                'radius': 0.05})
        objects = compas_blender.draw_points(points, self.nodecollection)
        self.object_node = zip(objects, nodes)
        return objects

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : rgb-tuple or dict of rgb-tuples
            The color specififcation for the edges.

        Returns
        -------
        list of :class:`bpy.types.Object`

        """
        edges = edges or list(self.network.edges())
        edge_color = colordict(color, edges, default=self.color_edges)
        lines = []
        for edge in edges:
            lines.append({
                'start': self.network.node_coordinates(edge[0]),
                'end': self.network.node_coordinates(edge[1]),
                'color': edge_color[edge],
                'name': f"{self.network.name}.edge.{edge[0]}-{edge[1]}",
                'width': 0.02})
        objects = compas_blender.draw_lines(lines, self.edgecollection)
        self.object_edge = zip(objects, edges)
        return objects


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
