from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import bpy
from functools import partial

import compas_blender
from compas.datastructures import Network
from compas.geometry import centroid_points
from compas.utilities import color_to_colordict
from compas.artists import NetworkArtist
from compas.colors import Color
from .artist import BlenderArtist

colordict = partial(color_to_colordict, colorformat="rgb", normalize=True)


class NetworkArtist(BlenderArtist, NetworkArtist):
    """Artist for drawing network data structures in Blender.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A COMPAS network.
    collection : str | :blender:`bpy.types.Collection`
        The name of the collection the object belongs to.

    Attributes
    ----------
    nodecollection : :blender:`bpy.types.Collection`
        The collection containing the nodes.
    edgecollection : :blender:`bpy.types.Collection`
        The collection containing the edges.
    nodelabelcollection : :blender:`bpy.types.Collection`
        The collection containing the node labels.
    edgelabelcollection : :blender:`bpy.types.Collection`
        The collection containing the edge labels.

    Examples
    --------
    Use the Blender artist explicitly.

    .. code-block:: python

        import compas
        from compas.datastructures import Network
        from compas_blender.artists import NetworkArtist

        network = Network.from_obj(compas.get('lines.obj'))

        artist = NetworkArtist(network)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        import compas
        from compas.datastructures import Network
        from compas.artists import Artist

        network = Network.from_obj(compas.get('lines.obj'))

        artist = Artist(network)
        artist.draw()

    """

    def __init__(
        self,
        network: Network,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        **kwargs: Any,
    ):

        super().__init__(network=network, collection=collection or network.name, **kwargs)

    @property
    def nodecollection(self) -> bpy.types.Collection:
        if not self._nodecollection:
            self._nodecollection = compas_blender.create_collection("Nodes", parent=self.collection)
        return self._nodecollection

    @property
    def edgecollection(self) -> bpy.types.Collection:
        if not self._edgecollection:
            self._edgecollection = compas_blender.create_collection("Edges", parent=self.collection)
        return self._edgecollection

    @property
    def nodelabelcollection(self) -> bpy.types.Collection:
        if not self._nodelabelcollection:
            self._nodelabelcollection = compas_blender.create_collection("NodeLabels", parent=self.collection)
        return self._nodelabelcollection

    @property
    def edgelabelcollection(self) -> bpy.types.Collection:
        if not self._edgelabelcollection:
            self._edgelabelcollection = compas_blender.create_collection("EdgeLabels", parent=self.collection)
        return self._edgelabelcollection

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_nodes(self):
        """Clear all objects contained in the node collection.

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.nodecollection.objects)

    def clear_edges(self):
        """Clear all objects contained in the edge collection.

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.edgecollection.objects)

    def clear_nodelabels(self):
        """Clear all objects contained in the nodelabel collection.

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.nodelabelcollection.objects)

    def clear_edgelabels(self):
        """Clear all objects contained in the edgelabel collection.

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.edgelabelcollection.objects)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(
        self,
        nodes: Optional[List[int]] = None,
        edges: Optional[Tuple[int, int]] = None,
        nodecolor: Optional[Union[str, Color, Dict[int, Color]]] = None,
        edgecolor: Optional[Union[str, Color, Dict[int, Color]]] = None,
    ) -> None:
        """Draw the network.

        Parameters
        ----------
        nodes : list[hashable], optional
            A list of node identifiers.
            Default is None, in which case all nodes are drawn.
        edges : list[tuple[hashable, hashable]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        nodecolor : :class:`~compas.colors.Color` | dict[hashable, :class:`~compas.colors.Color`], optional
            The color specification for the nodes.
        edgecolor : :class:`~compas.colors.Color` | dict[tuple[hashable, hashable], :class:`~compas.colors.Color`], optional
            The color specification for the edges.

        Returns
        -------
        None

        """
        self.clear()
        if self.show_nodes:
            self.draw_nodes(nodes=nodes, color=nodecolor)
        if self.show_edges:
            self.draw_edges(edges=edges, color=edgecolor)

    def draw_nodes(
        self,
        nodes: Optional[List[int]] = None,
        color: Optional[Union[Color, Dict[int, Color]]] = None,
    ) -> List[bpy.types.Object]:
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list[hashable], optional
            A list of node identifiers.
            Default is None, in which case all nodes are drawn.
        color : :class:`~compas.colors.Color` | dict[hashable, :class:`~compas.colors.Color`], optional
            The color specification for the nodes.
            The default color of nodes is :attr:`default_nodecolor`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.node_color = color
        nodes = nodes or self.nodes
        points = []
        for node in nodes:
            points.append(
                {
                    "pos": self.node_xyz[node],
                    "name": f"{self.network.name}.node.{node}",
                    "color": self.node_color[node],
                    "radius": 0.05,
                }
            )
        return compas_blender.draw_points(points, self.nodecollection)

    def draw_edges(
        self,
        edges: Optional[Tuple[int, int]] = None,
        color: Optional[Union[Color, Dict[int, Color]]] = None,
    ) -> List[bpy.types.Object]:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[hashable, hashable]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[hashable, hashable], :class:`~compas.colors.Color`], optional
            The color specification for the edges.
            The default color of edges is :attr:`default_edgecolor`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.edge_color = color
        edges = edges or self.edges
        lines = []
        for edge in edges:
            u, v = edge
            lines.append(
                {
                    "start": self.node_xyz[u],
                    "end": self.node_xyz[v],
                    "color": self.edge_color[edge],
                    "name": f"{self.network.name}.edge.{u}-{v}",
                    "width": self.edge_width[edge],
                }
            )
        return compas_blender.draw_lines(lines, self.edgecollection)

    def draw_nodelabels(self, text: Optional[Dict[int, str]] = None) -> List[bpy.types.Object]:
        """Draw labels for a selection nodes.

        Parameters
        ----------
        text : dict[hashable, str], optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is None, in which case every vertex will be labeled with its key.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.node_text = text
        labels = []
        for node in self.node_text:
            labels.append(
                {
                    "pos": self.node_xyz[node],
                    "name": f"{self.network.name}.nodelabel.{node}",
                    "text": self.node_text[node],
                    "color": self.node_color[node],
                }
            )
        return compas_blender.draw_texts(labels, collection=self.nodelabelcollection)

    def draw_edgelabels(self, text: Optional[Dict[Tuple[int, int], str]] = None) -> List[bpy.types.Object]:
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict[tuple[hashable, hashable], str], optional
            A dictionary of edge labels as edge-text pairs.
            The default value is None, in which case every edge will be labeled with its key.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self.edge_text = text
        labels = []
        for edge in self.edge_text:
            u, v = edge
            labels.append(
                {
                    "pos": centroid_points([self.node_xyz[u], self.node_xyz[v]]),
                    "name": f"{self.network.name}.edgelabel.{u}-{v}",
                    "text": self.edge_text[edge],
                    "color": self.edge_color[edge],
                }
            )
        return compas_blender.draw_texts(labels, collection=self.edgelabelcollection)
