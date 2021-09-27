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
    """Artist for COMPAS mesh data structures.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    vertices : list of int, optional
        A list of vertex identifiers.
        Default is ``None``, in which case all vertices are drawn.
    edges : list, optional
        A list of edge keys (as uv pairs) identifying which edges to draw.
        The default is ``None``, in which case all edges are drawn.
    faces : list, optional
        A list of face identifiers.
        The default is ``None``, in which case all faces are drawn.
    vertexcolor : rgb-tuple or dict of rgb-tuples, optional
        The color specification for the vertices.
    edgecolor : rgb-tuple or dict of rgb-tuples, optional
        The color specification for the edges.
    facecolor : rgb-tuple or dict of rgb-tuples, optional
        The color specification for the faces.
    show_vertices : bool, optional
    show_edges : bool, optional
    show_faces : bool, optional
    vertexsize : int, optional
    sizepolicy : {'relative', 'absolute'}, optional

    Attributes
    ----------
    vertexcollection : :class:`PatchCollection`
        The collection containing the vertices.
    edgecollection : :class:`LineCollection`
        The collection containing the edges.
    facecollection : :class:`PatchCollection`
        The collection containing the faces.

    Class Attributes
    ----------------
    default_vertexsize : int
    default_edgewidth : float
    zorder_vertices : int
    zorder_edges : int
    zorder_faces : int
    """

    default_vertexsize: int = 5
    default_edgewidth: float = 1.0

    zorder_faces: int = 1000
    zorder_edges: int = 2000
    zorder_vertices: int = 3000

    def __init__(self,
                 mesh: Mesh,
                 vertices: Optional[List[int]] = None,
                 edges: Optional[List[int]] = None,
                 faces: Optional[List[int]] = None,
                 vertexcolor: Color = (1, 1, 1),
                 edgecolor: Color = (0, 0, 0),
                 facecolor: Color = (0.9, 0.9, 0.9),
                 edgewidth: float = 1.0,
                 show_vertices: bool = True,
                 show_edges: bool = True,
                 show_faces: bool = True,
                 vertexsize: int = 5,
                 sizepolicy: Literal['relative', 'absolute'] = 'relative',
                 **kwargs: Any):

        super().__init__(mesh=mesh, **kwargs)

        self._edge_width = None

        self._vertexcollection = None
        self._edgecollection = None
        self._facecollection = None
        self._vertexnormalcollection = None
        self._facenormalcollection = None
        self._vertexlabelcollection = None
        self._edgelabelcollection = None
        self._facelabelcollection = None

        self.vertices = vertices
        self.edges = edges
        self.faces = faces

        self.vertex_color = vertexcolor
        self.edge_color = edgecolor
        self.face_color = facecolor
        self.edge_width = edgewidth

        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces

        self.vertexsize = vertexsize
        self.sizepolicy = sizepolicy

    @property
    def item(self):
        """Mesh: Alias for ``~MeshArtist.mesh``"""
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

    def clear(self):
        self.clear_vertices()
        self.clear_edges()
        self.clear_faces()

    def clear_vertices(self) -> None:
        if self._vertexcollection:
            self.plotter.axes.remove_collection(self._vertexcollection)
        self._vertexcollection = None

    def clear_edges(self) -> None:
        if self._edgecollection:
            self.plotter.axes.remove_collection(self._edgecollection)
        self._edgecollection = None

    def clear_faces(self) -> None:
        if self._facecollection:
            self.plotter.axes.remove_collection(self._facecollection)
        self._facecollection = None

    def draw(self,
             vertices: Optional[List[int]] = None,
             edges: Optional[List[Tuple[int, int]]] = None,
             faces: Optional[List[int]] = None,
             vertexcolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
             edgecolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
             facecolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None
             ) -> None:
        """Draw the mesh.

        Parameters
        ----------
        vertices : list of int, optional
            A list of vertex identifiers.
            Default is ``None``, in which case all vertices are drawn.
        edges : list, optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        faces : list, optional
            A list of face identifiers.
            The default is ``None``, in which case all faces are drawn.
        vertexcolor : rgb-tuple or dict of rgb-tuples, optional
            The color specification for the vertices.
        edgecolor : rgb-tuple or dict of rgb-tuples, optional
            The color specification for the edges.
        facecolor : rgb-tuple or dict of rgb-tuples, optional
            The color specification for the faces.
        """
        self.clear()
        if self.show_vertices:
            self.draw_vertices(vertices=vertices, color=vertexcolor)
        if self.show_edges:
            self.draw_edges(edges=edges, color=edgecolor)
        if self.show_faces:
            self.draw_faces(faces=faces, color=facecolor)

    def redraw(self) -> None:
        raise NotImplementedError

    def draw_vertices(self,
                      vertices: Optional[List[int]] = None,
                      color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
                      text: Optional[Dict[int, str]] = None) -> None:
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list of int, optional
            A list of vertex identifiers.
            Default is ``None``, in which case all vertices are drawn.
        color : rgb-tuple or dict of rgb-tuples, optional
            The color specification for the vertices.

        Returns
        -------
        None
        """
        self.clear_vertices()

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
        self._vertexcollection = collection

    def draw_edges(self,
                   edges: Optional[List[Tuple[int, int]]] = None,
                   color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
                   text: Optional[Dict[int, str]] = None) -> None:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list, optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : rgb-tuple or dict of rgb-tuples, optional
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
        self._edgecollection = collection

    def draw_faces(self,
                   faces: Optional[List[int]] = None,
                   color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
                   text: Optional[Dict[int, str]] = None) -> None:
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list, optional
            A list of face identifiers.
            The default is ``None``, in which case all faces are drawn.
        color : rgb-tuple or dict of rgb-tuples, optional
            The color specification for the faces.

        Returns
        -------
        None
        """
        self.clear_faces()

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
        self._facecollection = collection
