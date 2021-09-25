from typing import Dict
from typing import Tuple
from typing import List
from typing import Union
from typing import Optional
from typing import Any
from typing_extensions import Literal
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import Polygon as PolygonPatch
from matplotlib.patches import Circle
from compas.datastructures import Mesh
from compas.artists import MeshArtist
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class MeshArtist(PlotterArtist, MeshArtist):
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
                 vertices: Optional[List[int]] = None,
                 edges: Optional[List[int]] = None,
                 faces: Optional[List[int]] = None,
                 vertexsize: int = 5,
                 sizepolicy: Literal['relative', 'absolute'] = 'relative',
                 vertexcolor: Color = (1, 1, 1),
                 edgewidth: float = 1.0,
                 edgecolor: Color = (0, 0, 0),
                 facecolor: Color = (0.9, 0.9, 0.9),
                 **kwargs: Any):

        super().__init__(mesh=mesh, **kwargs)

        self._mpl_vertex_collection = None
        self._mpl_edge_collection = None
        self._mpl_face_collection = None
        self._edge_width = None
        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        self.vertexsize = vertexsize
        self.sizepolicy = sizepolicy
        self.edgewidth = edgewidth
        self.vertex_color = vertexcolor
        self.edge_color = edgecolor
        self.face_color = facecolor

    @property
    def item(self):
        return self.mesh

    @item.setter
    def item(self, item: Mesh):
        self.mesh = item

    @property
    def edge_width(self) -> Dict[Tuple[int, int], float]:
        """dict: Edge widths."""
        if not self._edge_width:
            self._edge_width = {edge: self.default_edgewidth for edge in self.mesh.edges()}
        return self._edge_width

    @edge_width.setter
    def edge_width(self, edgewidth: Union[float, Dict[Tuple[int, int], float]]):
        if isinstance(edgewidth, dict):
            self._edge_width = edgewidth
        elif isinstance(edgewidth, (int, float)):
            self._edge_width = {edge: edgewidth for edge in self.mesh.edges()}

    @property
    def data(self) -> List[List[float]]:
        return self.mesh.vertices_attributes('xy')

    def draw(self,
             vertices=None,
             edges=None,
             faces=None,
             vertexcolor=None,
             edgecolor=None,
             facecolor=None) -> None:
        """Draw the mesh."""
        if self.show_faces:
            self.draw_faces(faces=faces, color=facecolor)

        if self.show_edges:
            self.draw_edges(edges=edges, color=edgecolor)

        if self.show_vertices:
            self.draw_vertices(vertices=vertices, color=vertexcolor)

    def draw_vertices(self, vertices=None, color=None, text=None):
        if vertices:
            self.vertices = vertices
        if color:
            self.vertex_color = color

        if self.sizepolicy == 'absolute':
            size = self.vertexsize / self.plotter.dpi
        else:
            size = self.vertexsize / self.mesh.number_of_vertices()

        circles = []
        for vertex in self.vertices:
            x, y = self.vertex_xyz[vertex][:2]
            circle = Circle(
                [x, y],
                radius=size,
                facecolor=self.vertex_color.get(vertex, self.default_vertexcolor),
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
        self._mpl_vertex_collection = collection

    def draw_edges(self, edges=None, color=None, text=None):
        if edges:
            self.edges = edges
        if color:
            self.edge_color = color

        lines = []
        colors = []
        widths = []
        for edge in self.edges:
            lines.append([self.vertex_xyz[edge[0]][:2], self.vertex_xyz[edge[1]][:2]])
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
        self._mpl_edge_collection = collection

    def draw_faces(self, faces=None, color=None, text=None):
        if faces:
            self.faces = faces
        if color:
            self.face_color = color

        polygons = []
        facecolors = []
        edgecolors = []
        linewidths = []
        for face in self.faces:
            data = [self.vertex_xyz[vertex][:2] for vertex in self.mesh.face_vertices(face)]
            polygons.append(PolygonPatch(data))
            facecolors.append(self.face_color.get(face, self.default_facecolor))
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

    def redraw(self) -> None:
        raise NotImplementedError
