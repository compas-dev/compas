from typing import Dict
from typing import Tuple
from typing import List
from typing import Union
from typing import Optional
from typing_extensions import Literal

from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import Circle

from compas.datastructures import Network
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class NetworkArtist(PlotterArtist):
    """Artist for COMPAS network data structures.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A COMPAS network.
    layer : str, optional
        The parent layer of the network.
    nodes : list of int, optional
        A list of node identifiers.
        Default is ``None``, in which case all nodes are drawn.
    edges : list, optional
        A list of edge keys (as uv pairs) identifying which edges to draw.
        The default is ``None``, in which case all edges are drawn.
    nodecolor : rgb-tuple or dict of rgb-tuples, optional
        The color specification for the nodes.
    edgecolor : rgb-tuple or dict of rgb-tuples, optional
        The color specification for the edges.
    show_nodes : bool, optional
    show_edges : bool, optional
    nodesize : int, optional
    sizepolicy : {'relative', 'absolute'}, optional

    Attributes
    ----------
    nodecollection : :class:`PatchCollection`
        The collection containing the nodes.
    edgecollection : :class:`LineCollection`
        The collection containing the edges.

    Class Attributes
    ----------------
    default_nodesize : int
    default_edgewidth : float
    zorder_nodes : int
    zorder_edges : int
    """

    default_nodesize: int = 5
    default_edgewidth: float = 1.0

    zorder_edges: int = 2000
    zorder_nodes: int = 3000

    def __init__(self,
                 network: Network,
                 nodes: Optional[List[int]] = None,
                 edges: Optional[List[int]] = None,
                 nodecolor: Color = (1, 1, 1),
                 edgecolor: Color = (0, 0, 0),
                 edgewidth: float = 1.0,
                 show_nodes: bool = True,
                 show_edges: bool = True,
                 nodesize: int = 5,
                 sizepolicy: Literal['relative', 'absolute'] = 'relative',
                 **kwargs):

        super().__init__(network=network, **kwargs)

        self._nodecollection = None
        self._edgecollection = None
        self._edge_width = None

        self.nodes = nodes
        self.edges = edges
        self.node_color = nodecolor
        self.edge_color = edgecolor
        self.edge_width = edgewidth
        self.show_nodes = show_nodes
        self.show_edges = show_edges

        self.nodesize = nodesize
        self.sizepolicy = sizepolicy

    @property
    def item(self):
        """Network: Alias for ``~NetworkArtist.network``"""
        return self.network

    @item.setter
    def item(self, item: Network):
        self.network = item

    @property
    def edge_width(self) -> Dict[Tuple[int, int], float]:
        """dict: Edge widths."""
        return self._edge_width

    @edge_width.setter
    def edge_width(self, edgewidth: Union[float, Dict[Tuple[int, int], float]]):
        if isinstance(edgewidth, dict):
            self._edge_width = edgewidth
        elif isinstance(edgewidth, (int, float)):
            self._edge_width = {edge: edgewidth for edge in self.network.edges()}
        else:
            self._edge_width = {}

    @property
    def data(self) -> List[List[float]]:
        return self.network.nodes_attributes('xy')

    def clear(self):
        self.clear_nodes()
        self.clear_edges()

    def clear_nodes(self):
        if self._nodecollection:
            self.plotter.axes.remove_collection(self._nodecollection)
        self._nodecollection = None

    def clear_edges(self):
        if self._edgecollection:
            self.plotter.axes.remove_collection(self._edgecollection)
        self._edgecollection = None

    def draw(self,
             nodes: Optional[List[int]] = None,
             edges: Optional[Tuple[int, int]] = None,
             nodecolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
             edgecolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> None:
        """Draw the network.

        Parameters
        ----------
        nodes : list of int, optional
            A list of node identifiers.
            Default is ``None``, in which case all nodes are drawn.
        edges : list, optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        nodecolor : rgb-tuple or dict of rgb-tuples, optional
            The color specification for the nodes.
        edgecolor : rgb-tuple or dict of rgb-tuples, optional
            The color specification for the edges.
        """
        self.clear()
        if self.show_nodes:
            self.draw_nodes(nodes=nodes, color=nodecolor)
        if self.show_edges:
            self.draw_edges(edges=edges, color=edgecolor)

    def redraw(self) -> None:
        raise NotImplementedError

    def draw_nodes(self,
                   nodes: Optional[List[int]] = None,
                   color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> None:
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list of int, optional
            A list of node identifiers.
            Default is ``None``, in which case all nodes are drawn.
        color : rgb-tuple or dict of rgb-tuples, optional
            The color specification for the nodes.
        """
        self.clear_nodes()

        if nodes:
            self.nodes = nodes
        if color:
            self.node_color = color

        if self.sizepolicy == 'absolute':
            size = self.nodesize / self.plotter.dpi
        else:
            size = self.nodesize / self.network.number_of_nodes()

        circles = []
        for node in self.nodes:
            x, y = self.node_xyz[node][:2]
            circle = Circle(
                [x, y],
                radius=size,
                facecolor=self.node_color.get(node, self.default_nodecolor),
                edgecolor=(0, 0, 0),
                lw=0.3,
            )
            circles.append(circle)

        collection = PatchCollection(
            circles,
            match_original=True,
            zorder=self.zorder_nodes,
            alpha=1.0
        )
        self.plotter.axes.add_collection(collection)
        self._nodecollection = collection

    def draw_edges(self,
                   edges: Optional[Tuple[int, int]] = None,
                   color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None) -> None:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list, optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : rgb-tuple or dict of rgb-tuples, optional
            The color specification for the edges.
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
            linestyle='solid',
            alpha=1.0,
            zorder=self.zorder_edges
        )
        self.plotter.axes.add_collection(collection)
        self._edgecollection = collection
