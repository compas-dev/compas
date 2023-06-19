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

from compas.geometry import centroid_points_xy
from compas.geometry import Line
from compas.geometry import offset_line
from compas.geometry import Frame
from compas.geometry import Scale
from compas.datastructures import Mesh
from compas.artists import MeshArtist
from compas.utilities import is_color_rgb
from compas.utilities.colors import is_color_light

from .artist import PlotterArtist

Color = Tuple[float, float, float]


class MeshArtist(PlotterArtist, MeshArtist):
    """Artist for COMPAS mesh data structures.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A COMPAS mesh.
    vertices : list[int], optional
        Selection of vertex identifiers.
        Default is None, in which case all vertices are drawn.
    edges : list[tuple[int, int]], optional
        Selection of edge identifiers.
        The default is None, in which case all edges are drawn.
    faces : list[int], optional
        Selection of face identifiers.
        The default is None, in which case all faces are drawn.
    vertexcolor : tuple[float, float, float] | dict[int, tuple[float, float, float]], optional
        Color specification for the vertices.
    edgecolor : tuple[float, float, float] | dict[tuple[int, int], tuple[float, float, float]], optional
        Color specification for the edges.
    facecolor : tuple[float, float, float] | dict[int, tuple[float, float, float]], optional
        Color specification for the faces.
    show_vertices : bool, optional
        If True, draw the vertices of the mesh.
    show_edges : bool, optional
        If True, draw the edges of the mesh.
    show_faces : bool, optional
        If True, draw the faces of the mesh.
    vertexsize : int, optional
        Size of the vertices.
    vertextext : str | dict[int, str], optional
        Labels for the vertices.
    edgetext : str | dict[tuple[int, int], str], optional
        Labels for the edges.
    facetext : str | dict[int, str], optional
        Labels for the faces.
    sizepolicy : {'relative', 'absolute'}, optional
        The policy for sizing the vertices.
        If ``'relative'``, the value of `vertexsize` is scaled by the number of vertices.
        If ``'absolute'``, the value of `vertexsize` is scaled by the resolution of the plotter (:attr:MeshArtist.plotter.dpi).
    zorder : int, optional
        The base stacking order of the components of the mesh on the canvas.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_plotters.artists.PlotterArtist` and :class:`~compas.artists.MeshArtist` for more info.

    Attributes
    ----------
    halfedges : list[tuple[int, int]]
        The halfedges to include in the drawing.
    vertex_size : dict[int, float]
        Mapping between vertex identifiers and vertex sizes.
    halfedge_color : dict[tuple[int, int], tuple[float, float, float]]
        Mapping between halfedge identifiers and halfedge colors.
    zorder_faces : int, read-only
        The stacking order of the faces relative to the base stacking order of the mesh.
    zorder_edges : int, read-only
        The stacking order of the edges relative to the base stacking order of the mesh.
    zorder_vertices : int, read-only
        The stacking order of the vertices relative to the base stacking order of the mesh.

    """

    default_halfedgecolor = (0.7, 0.7, 0.7)

    def __init__(
        self,
        mesh: Mesh,
        vertices: Optional[List[int]] = None,
        edges: Optional[List[int]] = None,
        faces: Optional[List[int]] = None,
        vertexcolor: Color = (1.0, 1.0, 1.0),
        edgecolor: Color = (0.0, 0.0, 0.0),
        facecolor: Color = (0.9, 0.9, 0.9),
        edgewidth: float = 1.0,
        show_vertices: bool = True,
        show_edges: bool = True,
        show_faces: bool = True,
        vertexsize: int = 5,
        vertextext: Optional[Union[str, Dict[int, str]]] = None,
        edgetext: Optional[Union[str, Dict[Tuple[int, int], str]]] = None,
        facetext: Optional[Union[str, Dict[int, str]]] = None,
        sizepolicy: Literal["relative", "absolute"] = "relative",
        zorder: int = 1000,
        **kwargs: Any,
    ):

        super().__init__(mesh=mesh, **kwargs)

        self.sizepolicy = sizepolicy
        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        self.vertex_color = vertexcolor
        self.vertex_size = vertexsize
        self.vertex_text = vertextext
        self.edge_color = edgecolor
        self.edge_width = edgewidth
        self.face_color = facecolor
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        self.zorder = zorder

        self._halfedges = None
        self._halfedgecollection = None
        self._halfedge_color = None

    @property
    def halfedges(self):
        if not self._halfedges:
            self._halfedges = [(u, v) for u in self.mesh.halfedge for v in self.mesh.halfedge[u]]
        return self._halfedges

    @halfedges.setter
    def halfedges(self, halfedges):
        self._halfedges = halfedges

    @property
    def vertex_size(self):
        if not self._vertex_size:
            factor = self.plotter.dpi if self.sizepolicy == "absolute" else self.mesh.number_of_vertices()
            size = self.default_vertexsize / factor
            self._vertex_size = {vertex: size for vertex in self.mesh.vertices()}
        return self._vertex_size

    @vertex_size.setter
    def vertex_size(self, vertexsize):
        factor = self.plotter.dpi if self.sizepolicy == "absolute" else self.mesh.number_of_vertices()
        if isinstance(vertexsize, dict):
            self.vertex_size.update({vertex: size / factor for vertex, size in vertexsize.items()})
        elif isinstance(vertexsize, (int, float)):
            self._vertex_size = {vertex: vertexsize / factor for vertex in self.mesh.vertices()}

    @property
    def halfedge_color(self):
        if self._halfedge_color is None:
            self._halfedge_color = {
                (u, v): self.default_halfedgecolor for u in self.mesh.halfedge for v in self.mesh.halfedge[u]
            }
        return self._halfedge_color

    @halfedge_color.setter
    def halfedge_color(self, halfedge_color):
        if isinstance(halfedge_color, dict):
            self._halfedge_color = halfedge_color
        elif is_color_rgb(halfedge_color):
            self._halfedge_color = {(u, v): halfedge_color for u in self.mesh.halfedge for v in self.mesh.halfedge[u]}

    @property
    def zorder_faces(self):
        return self.zorder + 10

    @property
    def zorder_edges(self):
        return self.zorder + 20

    @property
    def zorder_vertices(self):
        return self.zorder + 30

    @property
    def item(self):
        """Mesh: Alias for ``~MeshArtist.mesh``"""
        return self.mesh

    @item.setter
    def item(self, item: Mesh):
        self.mesh = item

    @property
    def data(self) -> List[List[float]]:
        return self.mesh.vertices_attributes("xy")

    # ==============================================================================
    # clear and draw
    # ==============================================================================

    def clear(self) -> None:
        pass

    def clear_vertices(self) -> None:
        """Clear the current vertices from the canvas.

        Returns
        -------
        None

        """
        if self._vertexcollection:
            self._vertexcollection.remove()
        self._vertexcollection = None

    def clear_edges(self) -> None:
        """Clear the current edges from the canvas.

        Returns
        -------
        None

        """
        if self._edgecollection:
            self._edgecollection.remove()
        self._edgecollection = None

    def clear_halfedges(self) -> None:
        """Clear the current halfedges from the canvas.

        Returns
        -------
        None

        """
        if self._halfedgecollection:
            for artist in self._halfedgecollection:
                artist.remove()
        self._halfedgecollection = None

    def clear_faces(self) -> None:
        """Clear the current faces from the canvas.

        Returns
        -------
        None

        """
        if self._facecollection:
            self._facecollection.remove()
        self._facecollection = None

    def draw(
        self,
        vertices: Optional[List[int]] = None,
        edges: Optional[List[Tuple[int, int]]] = None,
        faces: Optional[List[int]] = None,
        vertexcolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
        edgecolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
        facecolor: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
    ) -> None:
        """Draw the mesh.

        Parameters
        ----------
        vertices : list[int], optional
            A list of vertex identifiers.
            Default is None, in which case all vertices are drawn.
        edges : list[tuple[int, int]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        faces : list[int], optional
            A list of face identifiers.
            The default is None, in which case all faces are drawn.
        vertexcolor : rgb-tuple | dict[int, rgb-tuple], optional
            The color specification for the vertices.
        edgecolor : rgb-tuple | dict[tuple[int, int], rgb-tuple], optional
            The color specification for the edges.
        facecolor : rgb-tuple | dict[int, rgb-tuple], optional
            The color specification for the faces.

        Returns
        -------
        None

        """
        self.clear()
        if self.show_vertices:
            self.draw_vertices(vertices=vertices, color=vertexcolor)
        if self.show_edges:
            self.draw_edges(edges=edges, color=edgecolor)
        if self.show_faces:
            self.draw_faces(faces=faces, color=facecolor)

    def draw_mesh(self):
        raise NotImplementedError

    def draw_vertices(
        self,
        vertices: Optional[List[int]] = None,
        color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
    ) -> None:
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A list of vertex identifiers.
            Default is None, in which case all vertices are drawn.
        color : rgb-tuple | dict[int, rgb-tuple], optional
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

        circles = []
        for vertex in self.vertices:
            x, y = self.vertex_xyz[vertex][:2]
            circle = Circle(
                [x, y],
                radius=self.vertex_size.get(vertex, self.default_vertexsize),
                facecolor=self.vertex_color.get(vertex, self.default_vertexcolor),
                edgecolor=(0, 0, 0),
                lw=0.3,
            )
            circles.append(circle)

        collection = PatchCollection(
            circles,
            match_original=True,
            zorder=self.zorder_vertices,
            alpha=1.0,
            picker=5,
        )
        self.plotter.axes.add_collection(collection)
        self._vertexcollection = collection

    def draw_edges(
        self,
        edges: Optional[List[Tuple[int, int]]] = None,
        color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
    ) -> None:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        color : rgb-tuple | dict[tuple[int, int], rgb-tuple], optional
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
            u, v = edge
            lines.append([self.vertex_xyz[edge[0]][:2], self.vertex_xyz[edge[1]][:2]])
            colors.append(self.edge_color.get(edge, self.edge_color.get((v, u), self.default_edgecolor)))
            widths.append(self.edge_width.get(edge, self.edge_width.get((v, u), self.default_edgewidth)))

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

    def draw_halfedges(
        self,
        halfedges: Optional[List[Tuple[int, int]]] = None,
        color: Union[str, Color, List[Color], Dict[int, Color]] = (0.7, 0.7, 0.7),
        distance: float = 0.05,
        width: float = 0.01,
        shrink: float = 0.8,
    ) -> None:
        """Draw a selection of halfedges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of halfedges to draw.
            The default is None, in which case all halfedges are drawn.
        color : rgb-tuple | dict[tuple[int, int], rgb-tuple], optional
            The color specification for the halfedges.

        Returns
        -------
        None

        """
        self.clear_halfedges()
        self._halfedgecollection = []

        if color:
            self.halfedge_color = color

        if halfedges:
            self.halfedges = halfedges

        for u, v in self.halfedges:
            face = self.mesh.halfedge_face(u, v)

            if face is None:
                normal = self.mesh.face_normal(self.mesh.halfedge_face(v, u))
            else:
                normal = self.mesh.face_normal(face)

            a, b = self.mesh.edge_coordinates(u, v)
            line = Line(*offset_line((a, b), distance, normal))
            frame = Frame(line.midpoint, [1, 0, 0], [0, 1, 0])
            scale = Scale.from_factors([shrink, shrink, shrink], frame=frame)
            line.transform(scale)

            artist = self.plotter.axes.arrow(
                line.start[0],
                line.start[1],
                line.vector[0],
                line.vector[1],
                width=width,
                head_width=10 * width,
                head_length=10 * width,
                length_includes_head=True,
                shape="right",
                color=self.halfedge_color.get((u, v), self.default_halfedgecolor),
                zorder=10000,
            )
            self._halfedgecollection.append(artist)

    def draw_faces(
        self,
        faces: Optional[List[int]] = None,
        color: Optional[Union[str, Color, List[Color], Dict[int, Color]]] = None,
    ) -> None:
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A list of face identifiers.
            The default is None, in which case all faces are drawn.
        color : rgb-tuple | dict[int, rgb-tuple], optional
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
            linestyle="solid",
            zorder=self.zorder_faces,
        )
        self.plotter.axes.add_collection(collection)
        self._facecollection = collection

    def draw_vertexlabels(self, text: Optional[Dict[int, str]] = None) -> None:
        """Draw a selection of vertex labels.

        Parameters
        ----------
        text : dict[int, str], optional
            A vertex-label map.

        Returns
        -------
        None

        """
        if self._vertexlabelcollection:
            for artist in self._vertexlabelcollection:
                artist.remove()

        if text:
            self.vertex_text = text

        labels = []
        for vertex in self.vertices:
            bgcolor = self.vertex_color.get(vertex, self.default_vertexcolor)
            color = (0, 0, 0) if is_color_light(bgcolor) else (1, 1, 1)

            text = self.vertex_text.get(vertex, None)
            if text is None:
                continue

            x, y = self.vertex_xyz[vertex][:2]
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

        self._vertexlabelcollection = labels

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

            x0, y0 = self.vertex_xyz[edge[0]][:2]
            x1, y1 = self.vertex_xyz[edge[1]][:2]
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

    def draw_facelabels(self, text: Optional[Dict[int, str]] = None) -> None:
        """Draw a selection of face labels.

        Parameters
        ----------
        text : dict[int, str]
            A face-label map.

        Returns
        -------
        None

        """
        if self._facelabelcollection:
            for artist in self._facelabelcollection:
                artist.remove()

        if text:
            self.face_text = text

        labels = []
        for face in self.faces:
            text = self.face_text.get(face, None)
            if text is None:
                continue

            x, y, _ = centroid_points_xy([self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)])

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
                    boxstyle="circle, pad=0.5",
                    facecolor=(1, 1, 1),
                    edgecolor=(0.5, 0.5, 0.5),
                    linestyle=":",
                ),
            )
            labels.append(artist)

        self._facelabelcollection = labels

    def redraw(self) -> None:
        """Redraw the mesh using the current geometry.

        Returns
        -------
        None

        """
        pass

    def update_vertexcolors(self, colors):
        """Update the colors of the vertices.

        Parameters
        ----------
        colors : dict[int, tuple[float, float, float]]
            Mapping between vertex identifiers and colors.
            Missing vertices get the default color: :attr:`MeshArtist.default_vertexcolor`.

        Returns
        -------
        None

        """
        facecolors = []
        for vertex in self.vertices:
            if vertex in colors:
                color = colors[vertex]
            else:
                color = self.vertex_color.get(vertex, self.default_vertexcolor)
            facecolors.append(color)
        self._vertexcollection.set_facecolors(facecolors)

    def update_edgecolors(self, colors):
        """Update the colors of the edges.

        Parameters
        ----------
        colors : dict[tuple[int, int], tuple[float, float, float]]
            Mapping between edge identifiers and colors.
            Missing edge get the default color: :attr:`MeshArtist.default_edgecolor`.

        Returns
        -------
        None

        """
        edgecolors = []
        for edge in self.edges:
            if edge in colors:
                color = colors[edge]
            else:
                color = self.edge_color.get(edge, self.default_edgecolor)
            edgecolors.append(color)
        self._edgecollection.set_colors(edgecolors)

    def update_edgewidths(self, widths):
        """Update the widths of the edges.

        Parameters
        ----------
        widths : dict[tuple[int, int], float]
            Mapping between edge identifiers and linewidths.
            Missing edges get the default edge linewidth: :attr:`MeshArtist.default_edgewidth`.

        Returns
        -------
        None

        """
        edgewidths = []
        for edge in self.edges:
            if edge in widths:
                w = widths[edge]
            else:
                w = self.edge_width.get(edge, self.default_edgewidth)
            edgewidths.append(w)
        self._edgecollection.set_linewidths(edgewidths)
