from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import bpy
from functools import partial

import compas_blender
from compas_blender.utilities import RGBColor
from compas.datastructures import Network
from compas.geometry import centroid_points
from compas.utilities import color_to_colordict
from compas.artists import NetworkArtist
from .artist import BlenderArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=True)


class NetworkArtist(BlenderArtist, NetworkArtist):
    """Artist for drawing network data structures in Blender.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A COMPAS network.
    collection : str or :blender:`bpy.types.Collection`
        The name of the collection the object belongs to.
    nodes : list[hashable], optional
        A list of node identifiers.
        Default is None, in which case all nodes are drawn.
    edges : list[tuple[hashable, hashable]], optional
        A list of edge keys (as uv pairs) identifying which edges to draw.
        The default is None, in which case all edges are drawn.
    nodecolor : rgb-tuple or dict[hashable, rgb-tuple], optional
        The color specification for the nodes.
    edgecolor : rgb-tuple or dict[tuple[hashable, hashable]], rgb-tuple], optional
        The color specification for the edges.
    show_nodes : bool, optional
        If True, draw the nodes of the network.
    show_edges : bool, optional
        If True, draw the edges of the network.

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

    def __init__(self,
                 network: Network,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 nodes: Optional[List[int]] = None,
                 edges: Optional[List[int]] = None,
                 nodecolor: RGBColor = (1, 1, 1),
                 edgecolor: RGBColor = (0, 0, 0),
                 show_nodes: bool = True,
                 show_edges: bool = True,
                 **kwargs: Any):

        super().__init__(network=network, collection=collection or network.name, **kwargs)

        self.nodes = nodes
        self.edges = edges
        self.node_color = nodecolor
        self.edge_color = edgecolor
        self.show_nodes = show_nodes
        self.show_edges = show_edges

    @property
    def nodecollection(self) -> bpy.types.Collection:
        if not self._nodecollection:
            self._nodecollection = compas_blender.create_collection('Nodes', parent=self.collection)
        return self._nodecollection

    @property
    def edgecollection(self) -> bpy.types.Collection:
        if not self._edgecollection:
            self._edgecollection = compas_blender.create_collection('Edges', parent=self.collection)
        return self._edgecollection

    @property
    def nodelabelcollection(self) -> bpy.types.Collection:
        if not self._nodelabelcollection:
            self._nodelabelcollection = compas_blender.create_collection('NodeLabels', parent=self.collection)
        return self._nodelabelcollection

    @property
    def edgelabelcollection(self) -> bpy.types.Collection:
        if not self._edgelabelcollection:
            self._edgelabelcollection = compas_blender.create_collection('EdgeLabels', parent=self.collection)
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

    def draw(self,
             nodes: Optional[List[int]] = None,
             edges: Optional[Tuple[int, int]] = None,
             nodecolor: Optional[Union[str, RGBColor, List[RGBColor], Dict[int, RGBColor]]] = None,
             edgecolor: Optional[Union[str, RGBColor, List[RGBColor], Dict[int, RGBColor]]] = None
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
        nodecolor : rgb-tuple or dict[hashable, rgb-tuple], optional
            The color specification for the nodes.
        edgecolor : rgb-tuple or dict[tuple[hashable, hashable], rgb-tuple], optional
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

    def draw_nodes(self,
                   nodes: Optional[List[int]] = None,
                   color: Optional[Union[str, RGBColor, List[RGBColor], Dict[int, RGBColor]]] = None
                   ) -> List[bpy.types.Object]:
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list[hashable], optional
            A list of node identifiers.
            Default is None, in which case all nodes are drawn.
        color : rgb-tuple or dict[hashable, rgb-tuple], optional
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
            points.append({
                'pos': self.node_xyz[node],
                'name': f"{self.network.name}.node.{node}",
                'color': self.node_color.get(node, self.default_nodecolor),
                'radius': 0.05
            })
        return compas_blender.draw_points(points, self.nodecollection)

    def draw_edges(self,
                   edges: Optional[Tuple[int, int]] = None,
                   color: Optional[Union[str, RGBColor, List[RGBColor], Dict[int, RGBColor]]] = None
                   ) -> List[bpy.types.Object]:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[hashable, hashable]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        color : rgb-tuple or dict[tuple[hashable, hashable], rgb-tuple], optional
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
            lines.append({
                'start': self.node_xyz[edge[0]],
                'end': self.node_xyz[edge[1]],
                'color': self.edge_color.get(edge, self.default_edgecolor),
                'name': f"{self.network.name}.edge.{edge[0]}-{edge[1]}",
                'width': 0.02
            })
        return compas_blender.draw_lines(lines, self.edgecollection)

    def draw_nodelabels(self,
                        text: Optional[Dict[int, str]] = None,
                        color: Optional[Union[str, RGBColor, List[RGBColor], Dict[int, RGBColor]]] = None
                        ) -> List[bpy.types.Object]:
        """Draw labels for a selection nodes.

        Parameters
        ----------
        text : dict[hashable, str], optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is None, in which case every vertex will be labeled with its key.
        color : rgb-tuple or dict[hashable, rgb-tuple], optional
            The color specification of the labels.
            The default color is the same as the default vertex color.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        if not text or text == 'key':
            node_text = {vertex: str(vertex) for vertex in self.nodes}
        elif text == 'index':
            node_text = {vertex: str(index) for index, vertex in enumerate(self._nodes)}
        elif isinstance(text, dict):
            node_text = text
        else:
            raise NotImplementedError
        node_color = colordict(color, node_text, default=self.default_nodecolor)
        labels = []
        for node in node_text:
            labels.append({
                'pos': self.node_xyz[node],
                'name': "{}.nodelabel.{}".format(self.network.name, node),
                'text': node_text[node],
                'color': node_color[node]
            })
        return compas_blender.draw_texts(labels, collection=self.nodelabelcollection)

    def draw_edgelabels(self,
                        text: Optional[Dict[Tuple[int, int], str]] = None,
                        color: Optional[Union[str, RGBColor, List[RGBColor], Dict[int, RGBColor]]] = None
                        ) -> List[bpy.types.Object]:
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict[tuple[hashable, hashable], str], optional
            A dictionary of edge labels as edge-text pairs.
            The default value is None, in which case every edge will be labeled with its key.
        color : rgb-tuple or dict[tuple[hashable, hashable], rgb-tuple], optional
            The color specification of the labels.
            The default color is the same as the default color for edges.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        if text is None:
            edge_text = {(u, v): "{}-{}".format(u, v) for u, v in self.edges}
        elif isinstance(text, dict):
            edge_text = text
        else:
            raise NotImplementedError
        edge_color = colordict(color, edge_text, default=self.default_edgecolor)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([self.node_xyz[edge[0]], self.node_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.network.name, *edge),
                'text': edge_text[edge]
            })
        return compas_blender.draw_texts(labels, collection=self.edgelabelcollection, color=edge_color)
