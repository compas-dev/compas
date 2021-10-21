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
    """Artist for COMPAS circles."""

    def __init__(self,
                 circle: Circle,
                 linewidth: float = 1.0,
                 linestyle: Literal['solid', 'dotted', 'dashed', 'dashdot'] = 'solid',
                 facecolor: Color = (1.0, 1.0, 1.0),
                 edgecolor: Color = (0, 0, 0),
                 fill: bool = True,
                 alpha: float = 1.0,
                 zorder: int = 1000,
                 **kwargs: Any):

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
            self.circle.center[:2]
        ]
        points[0][0] -= self.circle.radius
        points[1][0] += self.circle.radius
        points[2][1] -= self.circle.radius
        points[3][1] += self.circle.radius
        return points

    def draw(self) -> None:
        circle = CirclePatch(
            self.circle.center[:2],
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            radius=self.circle.radius,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            fill=self.fill,
            alpha=self.alpha,
            zorder=self.zorder
        )
        self._mpl_circle = self.plotter.axes.add_artist(circle)
        self.update_data()

    def redraw(self) -> None:
        self._mpl_circle.center = self.circle.center[:2]
        self._mpl_circle.set_radius(self.circle.radius)
        self._mpl_circle.set_edgecolor(self.edgecolor)
        self._mpl_circle.set_facecolor(self.facecolor)
        self.update_data()
