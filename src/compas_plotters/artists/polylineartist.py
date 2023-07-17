from typing import Tuple
from typing import List
from typing import Any
from typing_extensions import Literal

from matplotlib.lines import Line2D
from compas.geometry import Polyline

from compas.artists import PrimitiveArtist
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class PolylineArtist(PlotterArtist, PrimitiveArtist):
    """Artist for COMPAS polylines.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        A COMPAS polyline.
    linewidth : float, optional
        Width of the polyline edge lines.
    linestyle : {'solid', 'dotted', 'dashed', 'dashdot'}, optional
        Style of the line.
    facecolor : tuple[float, float, float], optional
        Color of the interior face of the polyline.
    edgecolor : tuple[float, float, float], optional
        Color of the boundary of the polyline.
    zorder : int, optional
        Stacking order of the polyline on the canvas.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_plotters.artists.PlotterArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    Attributes
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        The line associated with the artist.

    """

    def __init__(
        self,
        polyline: Polyline,
        draw_points: bool = True,
        linewidth: float = 1.0,
        linestyle: Literal["solid", "dotted", "dashed", "dashdot"] = "solid",
        color: Color = (0, 0, 0),
        zorder: int = 1000,
        **kwargs: Any
    ):

        super().__init__(primitive=polyline, **kwargs)

        self._mpl_line = None
        self._point_artists = []
        self.draw_points = draw_points
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.color = color
        self.zorder = zorder

    @property
    def polyline(self):
        return self.primitive

    @polyline.setter
    def polyline(self, polyline):
        self.primitive = polyline

    @property
    def data(self) -> List[List[float]]:
        return [point[:2] for point in self.polyline.points]

    def draw(self) -> None:
        """Draw the polyline.

        Returns
        -------
        None

        """
        x, y, _ = zip(*self.polyline.points)
        line2d = Line2D(
            x,
            y,
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            color=self.color,
            zorder=self.zorder,
        )
        self._mpl_line = self.plotter.axes.add_line(line2d)
        if self.draw_points:
            for point in self.polyline:
                self._point_artists.append(self.plotter.add(point))

    def redraw(self) -> None:
        """Update the polyline using the current geometry and visualization settings.

        Returns
        -------
        None

        """
        x, y, _ = zip(*self.polyline.points)
        self._mpl_line.set_xdata(x)
        self._mpl_line.set_ydata(y)
        self._mpl_line.set_color(self.color)
        self._mpl_line.set_linewidth(self.linewidth)
