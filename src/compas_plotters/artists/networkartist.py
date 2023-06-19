from typing import Dict
from typing import Tuple
from typing import List
from typing import Union
from typing import Optional
from typing_extensions import Literal

from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import Circle

from compas.datastructures import Network
from compas.artists import NetworkArtist
from compas.utilities.colors import is_color_light
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class NetworkArtist(PlotterArtist, NetworkArtist):
    """Artist for COMPAS network data structures.

    Parameters
    ----------
    network : :class:`~compas.datastructures.Network`
        A COMPAS network.
    nodes : list[int], optional
        Selection of node identifiers.
        Default is None, in which case all nodes are drawn.
    edges : list[tuple[int, int]], optional
        Selection of edge identifiers.
        The default is None, in which case all edges are drawn.
    nodecolor : tuple[float, float, float] | dict[int, tuple[float, float, float]], optional
        Color specification for the nodes.
    edgecolor : tuple[float, float, float] | dict[tuple[int, int], tuple[float, float, float]], optional
        Color specification for the edges.
    show_nodes : bool, optional
        If True, draw the nodes of the network.
    show_edges : bool, optional
        If True, draw the edges of the network.
    nodesize : int, optional
        The size of the nodes.
    sizepolicy : {'relative', 'absolute'}, optional
        The policy for sizing the nodes.
        If ``'relative'``, the value of `nodesize` is scaled by the number of nodes.
        If ``'absolute'``, the value of `nodesize` is scaled by the resolution of the plotter (:attr:NetworkArtist.plotter.dpi).

    Attributes
    ----------
    node_size : dict[int, float]
        Mapping between node identifiers and node sizes.
    zorder_edges : int, read-only
        The stacking order of the edges relative to the base stacking order of the network.
    zorder_nodes : int, read-only
        The stacking order of the nodes relative to the base stacking order of the network.

    """

    def __init__(
        self,
        network: Network,
        nodes: Optional[List[int]] = None,
        edges: Optional[List[int]] = None,
        nodecolor: Color = (1.0, 1.0, 1.0),
        edgecolor: Color = (0.0, 0.0, 0.0),
        edgewidth: float = 1.0,
        show_nodes: bool = True,
        show_edges: bool = True,
        nodesize: int = 5,
        sizepolicy: Literal["relative", "absolute"] = "relative",
        zorder: int = 1000,
        **kwargs,
    ):

        super().__init__(network=network, **kwargs)

        self.sizepolicy = sizepolicy
        self.nodes = nodes
        self.edges = edges
        self.node_color = nodecolor
        self.node_size = nodesize
        self.edge_color = edgecolor
        self.edge_width = edgewidth
        self.show_nodes = show_nodes
        self.show_edges = show_edges
        self.zorder = zorder

    @property
    def zorder_edges(self):
        return self.zorder + 10

    @property
    def zorder_nodes(self):
        return self.zorder + 20

    @property
    def item(self):
        """Network: Alias for ``~NetworkArtist.network``"""
        return self.network

    @item.setter
    def item(self, item: Network):
        self.network = item

    @property
    def data(self) -> List[List[float]]:
        return self.network.nodes_attributes("xy")

    @property
    def node_size(self):
        if not self._node_size:
            factor = self.plotter.dpi if self.sizepolicy == "absolute" else self.network.number_of_nodes()
            size = self.default_nodesize / factor
            self._node_size = {node: size for node in self.network.nodes()}
        return self._node_size

    @node_size.setter
    def node_size(self, nodesize):
        factor = self.plotter.dpi if self.sizepolicy == "absolute" else self.network.number_of_nodes()
        if isinstance(nodesize, dict):
            self.node_size.update({node: size / factor for node, size in nodesize.items()})
        elif isinstance(nodesize, (int, float)):
            self._node_size = {node: nodesize / factor for node in self.network.nodes()}

    # ==============================================================================
    # clear and draw
    # ==============================================================================

    def clear_nodes(self):
        """Clear the current nodes from the canvas.

        Returns
        -------
        None

        """
        if self._nodecollection:
            self._nodecollection.remove()
        self._nodecollection = None

    def clear_edges(self):
        """Clear the current edges from the canvas.

        Returns
        -------
        None

        """
        if self._edgecollection:
            self._edgecollection.remove()
        self._edgecollection = None

    def draw(
        self,
        nodes: Optional[List[int]] = None,
        edges: Optional[Tuple[int, int]] = None,
        nodecolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
        edgecolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
    ) -> None:
        """Draw the network.

        Parameters
        ----------
        nodes : list[int], optional
            A list of node identifiers.
            Default is None, in which case all nodes are drawn.
        edges : list[tuple[int, int]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        nodecolor : tuple[float, float, float] | dict[int, tuple[float, float, float]], optional
            The color specification for the nodes.
        edgecolor : tuple[float, float, float] | dict[tuple[int, int], tuple[float, float, float]], optional
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
        color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
    ) -> None:
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list[int], optional
            A list of node identifiers.
            Default is None, in which case all nodes are drawn.
        color : tuple[float, float, float] | dict[int, tuple[float, float, float]], optional
            The color specification for the nodes.

        Returns
        -------
        None

        """
        self.clear_nodes()
        if nodes:
            self.nodes = nodes
        if color:
            self.node_color = color

        circles = []
        for node in self.nodes:
            x, y = self.node_xyz[node][:2]
            circle = Circle(
                [x, y],
                radius=self.node_size.get(node, self.default_nodesize),
                facecolor=self.node_color.get(node, self.default_nodecolor),
                edgecolor=(0, 0, 0),
                lw=0.3,
            )
            circles.append(circle)

        collection = PatchCollection(circles, match_original=True, zorder=self.zorder_nodes, alpha=1.0)
        self.plotter.axes.add_collection(collection)
        self._nodecollection = collection

    def draw_edges(
        self,
        edges: Optional[Tuple[int, int]] = None,
        color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
    ) -> None:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        color : tuple[float, float, float] | dict[tuple[int, int], tuple[float, float, float]], optional
            The color specification for the edges.

        Returns
        -------
        None

        """
        self.clear_edges()
        if edges:
            self.edges = edges
        if color:
            self.edge_color = color

        lines = []
        colors = []
        widths = []
        for edge in self.edges:
            lines.append([self.node_xyz[edge[0]][:2], self.node_xyz[edge[1]][:2]])
            colors.append(self.edge_color.get(edge, self.default_edgecolor))
            widths.append(self.edge_width.get(edge, self.default_edgewidth))

        collection = LineCollection(
            lines,
            linewidths=widths,
            colors=colors,
            linestyle="solid",
            alpha=1.0,
            zorder=self.zorder_edges,
        )
        self.plotter.axes.add_collection(collection)
        self._edgecollection = collection

    def draw_nodelabels(self, text: Optional[Dict[int, str]] = None) -> None:
        """Draw a selection of node labels.

        Parameters
        ----------
        text : dict[int, str], optional
            A node-label map.

        Returns
        -------
        None

        """
        if self._nodelabelcollection:
            for artist in self._nodelabelcollection:
                artist.remove()

        if text:
            self.node_text = text

        labels = []
        for node in self.nodes:
            bgcolor = self.node_color.get(node, self.default_nodecolor)
            color = (0, 0, 0) if is_color_light(bgcolor) else (1, 1, 1)

            text = self.node_text.get(node, None)
            if text is None:
                continue

            x, y = self.node_xyz[node][:2]
            artist = self.plotter.axes.text(
                x,
                y,
                f"{text}",
                fontsize=self.plotter.fontsize,
                family="monospace",
                ha="center",
                va="center",
                zorder=10000,
                color=color,
            )
            labels.append(artist)

        self._nodelabelcollection = labels

    def draw_edgelabels(self, text: Optional[Dict[int, str]] = None) -> None:
        """Draw a selection of edge labels.

        Parameters
        ----------
        text : dict[tuple[int, int], str]
            An edge-label map.

        Returns
        -------
        None

        """
        if self._edgelabelcollection:
            for artist in self._edgelabelcollection:
                artist.remove()

        if text:
            self.edge_text = text

        labels = []
        for edge in self.edges:
            u, v = edge
            text = self.edge_text.get(edge, self.edge_text.get((v, u), None))
            if text is None:
                continue

            x0, y0 = self.node_xyz[edge[0]][:2]
            x1, y1 = self.node_xyz[edge[1]][:2]
            x = 0.5 * (x0 + x1)
            y = 0.5 * (y0 + y1)

            artist = self.plotter.axes.text(
                x,
                y,
                f"{text}",
                fontsize=self.plotter.fontsize,
                family="monospace",
                ha="center",
                va="center",
                zorder=10000,
                color=(0, 0, 0),
                bbox=dict(
                    boxstyle="round, pad=0.3",
                    facecolor=(1, 1, 1),
                    edgecolor=None,
                    linewidth=0,
                ),
            )
            labels.append(artist)

        self._edgelabelcollection = labels
