# from __future__ import annotations
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import bpy
from functools import partial

import compas_blender
from compas_blender.artists._artist import BaseArtist
from compas.datastructures import Network
from compas.geometry import centroid_points
from compas.utilities import color_to_colordict
from .artist import BlenderArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=True)
Color = Union[Tuple[int, int, int], Tuple[float, float, float]]


class NetworkArtist(BlenderArtist):
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

    def __init__(self, network: Network):
        super().__init__()
        self._nodecollection = None
        self._edgecollection = None
        self._nodelabelcollection = None
        self._edgelabelcollection = None
        self._object_node = {}
        self._object_edge = {}
        self._object_nodelabel = {}
        self._object_edgelabel = {}
        self.color_nodes = (1.0, 1.0, 1.0)
        self.color_edges = (0.0, 0.0, 0.0)
        self.show_nodes = True,
        self.show_edges = True,
        self.show_nodelabels = False,
        self.show_edgelabels = False
        self.network = network

    @property
    def nodecollection(self) -> bpy.types.Collection:
        path = f"{self.network.name}::Nodes"
        if not self._nodecollection:
            self._nodecollection = compas_blender.create_collections_from_path(path)[1]
        return self._nodecollection

    @property
    def edgecollection(self) -> bpy.types.Collection:
        path = f"{self.network.name}::Edges"
        if not self._edgecollection:
            self._edgecollection = compas_blender.create_collections_from_path(path)[1]
        return self._edgecollection

    @property
    def nodelabelcollection(self) -> bpy.types.Collection:
        path = f"{self.network.name}::VertexLabels"
        if not self._nodelabelcollection:
            self._nodelabelcollection = compas_blender.create_collections_from_path(path)[1]
        return self._nodelabelcollection

    @property
    def edgelabelcollection(self) -> bpy.types.Collection:
        path = f"{self.network.name}::EdgeLabels"
        if not self._edgelabelcollection:
            self._edgelabelcollection = compas_blender.create_collections_from_path(path)[1]
        return self._edgelabelcollection

    @property
    def object_node(self) -> Dict[bpy.types.Object, int]:
        if not self._object_node:
            self._object_node = {}
        return self._object_node

    @object_node.setter
    def object_node(self, values):
        self._object_node = dict(values)

    @property
    def object_edge(self) -> Dict[bpy.types.Object, Tuple[int, int]]:
        if not self._object_edge:
            self._object_edge = {}
        return self._object_edge

    @object_edge.setter
    def object_edge(self, values):
        self._object_edge = dict(values)

    @property
    def object_nodelabel(self) -> Dict[bpy.types.Object, int]:
        """Map between Blender object objects and node label identifiers."""
        return self._object_nodelabel

    @object_nodelabel.setter
    def object_nodelabel(self, values):
        self._object_nodelabel = dict(values)

    @property
    def object_edgelabel(self) -> Dict[bpy.types.Object, Tuple[int, int]]:
        """Map between Blender object objects and  edge label identifiers."""
        return self._object_edgelabel

    @object_edgelabel.setter
    def object_edgelabel(self, values):
        self._object_edgelabel = dict(values)

    def clear(self) -> None:
        objects = list(self.object_node)
        objects += list(self.object_edge)
        objects += list(self.object_nodelabel)
        objects += list(self.object_edgelabel)
        compas_blender.delete_objects(objects, purge_data=True)
        self._object_node = {}
        self._object_edge = {}
        self._object_nodelabel = {}
        self._object_edgelabel = {}

    def draw(self) -> None:
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

    def draw_nodes(self,
                   nodes: Optional[List[int]] = None,
                   color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> List[bpy.types.Object]:
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list of int, optional
            A list of node identifiers.
            Default is ``None``, in which case all nodes are drawn.
        color : rgb-tuple or dict of rgb-tuples
            The color specification for the nodes.

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

    def draw_edges(self,
                   edges: Optional[Tuple[int, int]] = None,
                   color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> List[bpy.types.Object]:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : rgb-tuple or dict of rgb-tuples
            The color specification for the edges.

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

    def draw_nodelabels(self,
                        text: Optional[Dict[int, str]] = None,
                        color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None
                        ) -> List[bpy.types.Object]:
        """Draw labels for a selection nodes.

        Parameters
        ----------
        text : dict, optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is ``None``, in which case every vertex will be labeled with its key.
        color : rgb-tuple or dict of rgb-tuple
            The color specification of the labels.
            The default color is the same as the default vertex color.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        if not text or text == 'key':
            node_text = {vertex: str(vertex) for vertex in self.network.nodes()}
        elif text == 'index':
            node_text = {vertex: str(index) for index, vertex in enumerate(self.network.nodes())}
        elif isinstance(text, dict):
            node_text = text
        else:
            raise NotImplementedError
        node_color = colordict(color, node_text, default=self.color_nodes)
        labels = []
        for node in node_text:
            labels.append({
                'pos': self.network.node_coordinates(node),
                'name': "{}.nodelabel.{}".format(self.network.name, node),
                'text': node_text[node],
                'color': node_color[node]})
        objects = compas_blender.draw_texts(labels, collection=self.nodelabelcollection)
        self.object_nodelabel = zip(objects, node_text)
        return objects

    def draw_edgelabels(self,
                        text: Optional[Dict[Tuple[int, int], str]] = None,
                        color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None
                        ) -> List[bpy.types.Object]:
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict, optional
            A dictionary of edge labels as edge-text pairs.
            The default value is ``None``, in which case every edge will be labeled with its key.
        color : rgb-tuple or dict of rgb-tuple
            The color specification of the labels.
            The default color is the same as the default color for edges.

        Returns
        -------
        list of :class:`bpy.types.Object`
        """
        if text is None:
            edge_text = {(u, v): "{}-{}".format(u, v) for u, v in self.network.edges()}
        elif isinstance(text, dict):
            edge_text = text
        else:
            raise NotImplementedError
        edge_color = colordict(color, edge_text, default=self.color_edges)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points(
                    [self.network.node_coordinates(edge[0]), self.network.node_coordinates(edge[1])]
                ),
                'name': "{}.edgelabel.{}-{}".format(self.network.name, *edge),
                'text': edge_text[edge]})
        objects = compas_blender.draw_texts(labels, collection=self.edgelabelcollection, color=edge_color)
        self.object_edgelabel = zip(objects, edge_text)
        return objects
