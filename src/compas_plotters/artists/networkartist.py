from typing import Dict, Tuple, List, Union
from typing_extensions import Literal
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import Circle
from compas.datastructures import Network
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class NetworkArtist(PlotterArtist):
    """Artist for COMPAS network data structures."""

    default_nodecolor: Color = (1, 1, 1)
    default_edgecolor: Color = (0, 0, 0)

    default_nodesize: int = 5
    default_edgewidth: float = 1.0

    zorder_edges: int = 2000
    zorder_nodes: int = 3000

    def __init__(self,
                 network: Network,
                 show_nodes: bool = True,
                 show_edges: bool = True,
                 nodesize: int = 5,
                 sizepolicy: Literal['relative', 'absolute'] = 'relative',
                 nodecolor: Color = (1, 1, 1),
                 edgewidth: float = 1.0,
                 edgecolor: Color = (0, 0, 0)):

        super().__init__(network)

        self._mpl_node_collection = None
        self._mpl_edge_collection = None
        self._nodecolor = None
        self._edgecolor = None
        self._edgewidth = None
        self.network = network
        self.show_nodes = show_nodes
        self.show_edges = show_edges
        self.nodesize = nodesize
        self.sizepolicy = sizepolicy
        self.nodecolor = nodecolor
        self.edgewidth = edgewidth
        self.edgecolor = edgecolor

    @property
    def nodecolor(self) -> Dict[int, Color]:
        """dict: Vertex colors."""
        return self._nodecolor

    @nodecolor.setter
    def nodecolor(self, nodecolor: Union[Color, Dict[int, Color]]):
        if isinstance(nodecolor, dict):
            self._nodecolor = nodecolor
        elif len(nodecolor) == 3 and all(isinstance(c, (int, float)) for c in nodecolor):
            self._nodecolor = {node: nodecolor for node in self.network.nodes()}
        else:
            self._nodecolor = {}

    @property
    def edgecolor(self) -> Dict[Tuple[int, int], Color]:
        """dict: Edge colors."""
        return self._edgecolor

    @edgecolor.setter
    def edgecolor(self, edgecolor: Union[Color, Dict[Tuple[int, int], Color]]):
        if isinstance(edgecolor, dict):
            self._edgecolor = edgecolor
        elif len(edgecolor) == 3 and all(isinstance(c, (int, float)) for c in edgecolor):
            self._edgecolor = {edge: edgecolor for edge in self.network.edges()}
        else:
            self._edgecolor = {}

    @property
    def edgewidth(self) -> Dict[Tuple[int, int], float]:
        """dict: Edge widths."""
        return self._edgewidth

    @edgewidth.setter
    def edgewidth(self, edgewidth: Union[float, Dict[Tuple[int, int], float]]):
        if isinstance(edgewidth, dict):
            self._edgewidth = edgewidth
        elif isinstance(edgewidth, (int, float)):
            self._edgewidth = {edge: edgewidth for edge in self.network.edges()}
        else:
            self._edgewidth = {}

    @property
    def data(self) -> List[List[float]]:
        return self.network.nodes_attributes('xy')

    def draw(self) -> None:
        """Draw the network."""
        node_xy = {node: self.network.node_attributes(node, 'xy') for node in self.network.nodes()}

        if self.show_nodes:
            lines = []
            colors = []
            widths = []
            for edge in self.network.edges():
                lines.append([node_xy[edge[0]], node_xy[edge[1]]])
                colors.append(self.edgecolor.get(edge, self.default_edgecolor))
                widths.append(self.edgewidth.get(edge, self.default_edgewidth))
            collection = LineCollection(
                lines,
                linewidths=widths,
                colors=colors,
                linestyle='solid',
                alpha=1.0,
                zorder=self.zorder_edges
            )
            self.plotter.axes.add_collection(collection)
            self._mpl_edge_collection = collection

        if self.show_nodes:
            if self.sizepolicy == 'absolute':
                size = self.nodesize / self.plotter.dpi
            else:
                size = self.nodesize / self.network.number_of_nodes()
            circles = []
            for node in self.network.nodes():
                x, y = node_xy[node]
                circle = Circle(
                    [x, y],
                    radius=size,
                    facecolor=self.nodecolor.get(node, self.default_nodecolor),
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

    def redraw(self) -> None:
        raise NotImplementedError
