from typing import Tuple
from typing import List
from typing import Any
from typing_extensions import Literal

from matplotlib.patches import Polygon as PolygonPatch
from compas.geometry import Polygon

from compas.artists import PrimitiveArtist
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class PolygonArtist(PlotterArtist, PrimitiveArtist):
    """Artist for COMPAS polygons.

    Parameters
    ----------
    polygon : :class:`~compas.geometry.Polygon`
        A COMPAS polygon.
    linewidth : float, optional
        Width of the polygon edge lines.
    linestyle : {'solid', 'dotted', 'dashed', 'dashdot'}, optional
        Style of the line.
    facecolor : tuple[float, float, float], optional
        Color of the interior face of the polygon.
    edgecolor : tuple[float, float, float], optional
        Color of the boundary of the polygon.
    zorder : int, optional
        Stacking order of the polygon on the canvas.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_plotters.artists.PlotterArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    Attributes
    ----------
    polygon : :class:`~compas.geometry.Polygon`
        The polygon associated with the artist.

    """

    def __init__(
        self,
        polygon: Polygon,
        linewidth: float = 1.0,
        linestyle: Literal["solid", "dotted", "dashed", "dashdot"] = "solid",
        facecolor: Color = (1.0, 1.0, 1.0),
        edgecolor: Color = (0, 0, 0),
        fill: bool = True,
        alpha: float = 1.0,
        zorder: int = 1000,
        **kwargs: Any
    ):

        super().__init__(primitive=polygon, **kwargs)

        self._mpl_polygon = None
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.fill = fill
        self.alpha = alpha
        self.zorder = zorder

    @property
    def polygon(self):
        return self.primitive

    @polygon.setter
    def polygon(self, polygon):
        self.primitive = polygon

    @property
    def data(self) -> List[List[float]]:
        return [point[:2] for point in self.polygon.points]

    def draw(self) -> None:
        """Draw the polygon.

        Returns
        -------
        None

        """
        polygon = PolygonPatch(
            self.data,
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            zorder=self.zorder,
            alpha=self.alpha,
            fill=self.fill,
        )
        self._mpl_polygon = self.plotter.axes.add_patch(polygon)

    def redraw(self) -> None:
        """Update the polygon using the current geometry and visualization settings.

        Returns
        -------
        None

        """
        self._mpl_polygon.set_xy(self.data)
        self._mpl_polygon.set_facecolor(self.facecolor)
        self._mpl_polygon.set_edgecolor(self.edgecolor)
        self._mpl_polygon.set_linewidth(self.linewidth)
