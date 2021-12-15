from typing import Tuple
from typing import List
from typing import Any

from matplotlib.patches import Circle
from matplotlib.transforms import ScaledTranslation
from compas.geometry import Point

from compas.artists import PrimitiveArtist
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class PointArtist(PlotterArtist, PrimitiveArtist):
    """Artist for COMPAS points."""

    def __init__(self,
                 point: Point,
                 size: int = 5,
                 facecolor: Color = (1.0, 1.0, 1.0),
                 edgecolor: Color = (0, 0, 0),
                 zorder: int = 9000,
                 **kwargs: Any):

        super().__init__(primitive=point, **kwargs)

        self._mpl_circle = None
        self._size = None
        self.size = size
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.zorder = zorder

    @property
    def point(self):
        return self.primitive

    @point.setter
    def point(self, point):
        self.primitive = point

    @property
    def _T(self):
        F = self.plotter.figure.dpi_scale_trans
        S = ScaledTranslation(self.point[0], self.point[1], self.plotter.axes.transData)
        T = F + S
        return T

    @property
    def size(self) -> float:
        return self._size / self.plotter.dpi

    @size.setter
    def size(self, size: int):
        self._size = size

    @property
    def data(self) -> List[List[float]]:
        return [self.point[:2]]

    def draw(self) -> None:
        circle = Circle(
            [0, 0],
            radius=self.size,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            transform=self._T,
            zorder=self.zorder
        )
        self._mpl_circle = self.plotter.axes.add_artist(circle)
        self.update_data()

    def redraw(self) -> None:
        self._mpl_circle.set_radius(self.size)
        self._mpl_circle.set_edgecolor(self.edgecolor)
        self._mpl_circle.set_facecolor(self.facecolor)
        self._mpl_circle.set_transform(self._T)
        self.update_data()
