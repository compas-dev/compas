from typing import Dict, Literal, Tuple, List, Union
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import Polygon as PolygonPatch
from matplotlib.patches import Circle
from compas.datastructures import Mesh
from compas_plotters.artists import Artist

Color = Tuple[float, float, float]


class MeshArtist(Artist):
    """Artist for COMPAS mesh data structures."""

    default_vertexcolor: Color = (1, 1, 1)
    default_edgecolor: Color = (0, 0, 0)
    default_facecolor: Color = (0.9, 0.9, 0.9)

    default_vertexsize: int = 5
    default_edgewidth: float = 1.0

    zorder_faces: int = 1000
    zorder_edges: int = 2000
    zorder_vertices: int = 3000

    def __init__(self,
                 mesh: Mesh,
                 show_vertices: bool = True,
                 show_edges: bool = True,
                 show_faces: bool = True,
                 vertexsize: int = 5,
                 sizepolicy: Literal['relative', 'absolute'] = 'relative',
                 vertexcolor: Color = (1, 1, 1),
                 edgewidth: float = 1.0,
                 edgecolor: Color = (0, 0, 0),
                 facecolor: Color = (0.9, 0.9, 0.9)):
        super(MeshArtist, self).__init__(mesh)
        self._mpl_vertex_collection = None
        self._mpl_edge_collection = None
        self._mpl_face_collection = None
        self._vertexcolor = None
        self._edgecolor = None
        self._facecolor = None
        self._edgewidth = None
        self.mesh = mesh
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        self.vertexsize = vertexsize
        self.sizepolicy = sizepolicy
        self.vertexcolor = vertexcolor
        self.edgewidth = edgewidth
        self.edgecolor = edgecolor
        self.facecolor = facecolor

    @property
    def vertexcolor(self) -> Dict[int, Color]:
        """dict: Vertex colors."""
        return self._vertexcolor

    @vertexcolor.setter
    def vertexcolor(self, vertexcolor: Union[Color, Dict[int, Color]]):
        if isinstance(vertexcolor, dict):
            self._vertexcolor = vertexcolor
        elif len(vertexcolor) == 3 and all(isinstance(c, (int, float)) for c in vertexcolor):
            self._vertexcolor = {vertex: vertexcolor for vertex in self.mesh.vertices()}
        else:
            self._vertexcolor = {}

    @property
    def edgecolor(self) -> Dict[Tuple[int, int], Color]:
        """dict: Edge colors."""
        return self._edgecolor

    @edgecolor.setter
    def edgecolor(self, edgecolor: Union[Color, Dict[Tuple[int, int], Color]]):
        if isinstance(edgecolor, dict):
            self._edgecolor = edgecolor
        elif len(edgecolor) == 3 and all(isinstance(c, (int, float)) for c in edgecolor):
            self._edgecolor = {edge: edgecolor for edge in self.mesh.edges()}
        else:
            self._edgecolor = {}

    @property
    def facecolor(self) -> Dict[int, Color]:
        """dict: Face colors."""
        return self._facecolor

    @facecolor.setter
    def facecolor(self, facecolor: Union[Color, Dict[int, Color]]):
        if isinstance(facecolor, dict):
            self._facecolor = facecolor
        elif len(facecolor) == 3 and all(isinstance(c, (int, float)) for c in facecolor):
            self._facecolor = {face: facecolor for face in self.mesh.faces()}
        else:
            self._facecolor = {}

    @property
    def edgewidth(self) -> Dict[Tuple[int, int], float]:
        """dict: Edge widths."""
        return self._edgewidth

    @edgewidth.setter
    def edgewidth(self, edgewidth: Union[float, Dict[Tuple[int, int], float]]):
        if isinstance(edgewidth, dict):
            self._edgewidth = edgewidth
        elif isinstance(edgewidth, (int, float)):
            self._edgewidth = {edge: edgewidth for edge in self.mesh.edges()}
        else:
            self._edgewidth = {}

    @property
    def data(self) -> List[List[float]]:
        return self.mesh.vertices_attributes('xy')

    def draw(self) -> None:
        """Draw the mesh."""
        vertex_xy = {vertex: self.mesh.vertex_attributes(vertex, 'xy') for vertex in self.mesh.vertices()}

        if self.show_faces:
            polygons = []
            facecolors = []
            edgecolors = []
            linewidths = []
            for face in self.mesh.faces():
                data = [vertex_xy[vertex] for vertex in self.mesh.face_vertices(face)]
                polygons.append(PolygonPatch(data))
                facecolors.append(self.facecolor.get(face, self.default_facecolor))
                edgecolors.append((0, 0, 0))
                linewidths.append(0.1)
            collection = PatchCollection(
                polygons,
                facecolors=facecolors,
                edgecolors=edgecolors,
                lw=linewidths,
                alpha=1.0,
                linestyle='solid',
                zorder=self.zorder_faces
            )
            self.plotter.axes.add_collection(collection)
            self._mpl_face_collection = collection

        if self.show_edges:
            lines = []
            colors = []
            widths = []
            for edge in self.mesh.edges():
                lines.append([vertex_xy[edge[0]], vertex_xy[edge[1]]])
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

        if self.show_vertices:
            if self.sizepolicy == 'absolute':
                size = self.vertexsize / self.plotter.dpi
            else:
                size = self.vertexsize / self.mesh.number_of_vertices()
            circles = []
            for vertex in self.mesh.vertices():
                x, y = vertex_xy[vertex]
                circle = Circle(
                    [x, y],
                    radius=size,
                    facecolor=self.vertexcolor.get(vertex, self.default_vertexcolor),
                    edgecolor=(0, 0, 0),
                    lw=0.3,
                )
                circles.append(circle)
            collection = PatchCollection(
                circles,
                match_original=True,
                zorder=self.zorder_vertices,
                alpha=1.0
            )
            self.plotter.axes.add_collection(collection)

    def redraw(self) -> None:
        raise NotImplementedError
