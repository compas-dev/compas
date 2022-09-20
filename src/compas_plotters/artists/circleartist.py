from typing import Tuple
from typing import List
from typing import Any
from typing_extensions import Literal

from matplotlib.patches import Circle as CirclePatch
from compas.geometry import Circle

from compas.artists import PrimitiveArtist
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class CircleArtist(PlotterArtist, PrimitiveArtist):
    """Artist for COMPAS circles.

    Parameters
    ----------
    circle : :class:`~compas.geometry.Circle`
        A COMPAS circle.
    linewidth : float, optional
        Width of the circle boundary.
    linestyle : {'solid', 'dotted', 'dashed', 'dashdot'}, optional
        Style of the circle boundary.
    facecolor : tuple[float ,float, float], optional
        Color of the interior of the circle.
    edgecolor : tuple[float, float, float], optional
        Color of the boundary of the circle.
    fill : bool, optional
        If True, draw the interior of the circle.
    alpha : float, optional
        Transparency of the circle.
    zorder : int, optional
        Stacking order of the circle on the canvas.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_plotters.artists.PlotterArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    Attributes
    ----------
    circle : :class:`~compas.geometry.Circle`
        The circle associated with the artist.

    """

    def __init__(
        self,
        circle: Circle,
        linewidth: float = 1.0,
        linestyle: Literal["solid", "dotted", "dashed", "dashdot"] = "solid",
        facecolor: Color = (1.0, 1.0, 1.0),
        edgecolor: Color = (0, 0, 0),
        fill: bool = True,
        alpha: float = 1.0,
        zorder: int = 1000,
        **kwargs: Any
    ):

        super().__init__(primitive=circle, **kwargs)

        self._mpl_circle = None
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.fill = fill
        self.alpha = alpha
        self.zorder = zorder

    @property
    def circle(self):
        return self.primitive

    @circle.setter
    def circle(self, circle):
        self.primitive = circle

    @property
    def data(self) -> List[List[float]]:
        points = [
            self.circle.center[:2],
            self.circle.center[:2],
            self.circle.center[:2],
            self.circle.center[:2],
        ]
        points[0][0] -= self.circle.radius
        points[1][0] += self.circle.radius
        points[2][1] -= self.circle.radius
        points[3][1] += self.circle.radius
        return points

    def draw(self) -> None:
        """Draw the circle on the plotter canvas.

        Returns
        -------
        None

        """
        circle = CirclePatch(
            self.circle.center[:2],
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            radius=self.circle.radius,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            fill=self.fill,
            alpha=self.alpha,
            zorder=self.zorder,
        )
        self._mpl_circle = self.plotter.axes.add_artist(circle)
        self.update_data()

    def redraw(self) -> None:
        """Update the circle using the current geometry and visualization settings.

        Returns
        -------
        None

        """
        self._mpl_circle.center = self.circle.center[:2]
        self._mpl_circle.set_radius(self.circle.radius)
        self._mpl_circle.set_edgecolor(self.edgecolor)
        self._mpl_circle.set_facecolor(self.facecolor)
        self.update_data()
