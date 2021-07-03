from typing import Literal, Tuple, List
from matplotlib.patches import Ellipse as EllipsePatch
from compas.geometry import Ellipse
from compas_plotters.artists import Artist

Color = Tuple[float, float, float]


class EllipseArtist(Artist):
    """Artist for COMPAS ellipses."""

    zorder: int = 1000

    def __init__(self,
                 ellipse: Ellipse,
                 linewidth: float = 1.0,
                 linestyle: Literal['solid', 'dotted', 'dashed', 'dashdot'] = 'solid',
                 facecolor: Color = (1.0, 1.0, 1.0),
                 edgecolor: Color = (0, 0, 0),
                 fill: bool = True,
                 alpha: float = 1.0):
        super(EllipseArtist, self).__init__(ellipse)
        self._mpl_ellipse = None
        self.ellipse = ellipse
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.fill = fill
        self.alpha = alpha

    @property
    def data(self) -> List[List[float, float]]:
        points = [
            self.ellipse.center[:2],
            self.ellipse.center[:2],
            self.ellipse.center[:2],
            self.ellipse.center[:2]
        ]
        points[0][0] -= self.ellipse.major
        points[1][0] += self.ellipse.major
        points[2][1] -= self.ellipse.minor
        points[3][1] += self.ellipse.minor
        return points

    def update_data(self) -> None:
        self.plotter.axes.update_datalim(self.data)

    def draw(self) -> None:
        ellipse = EllipsePatch(
            self.ellipse.center[:2],
            width=2*self.ellipse.major,
            height=2*self.ellipse.minor,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            fill=self.fill,
            zorder=self.zorder)
        self._mpl_ellipse = self.plotter.axes.add_artist(ellipse)

    def redraw(self) -> None:
        self._mpl_ellipse.center = self.ellipse.center[:2]
        self._mpl_ellipse.set_width(2*self.ellipse.major)
        self._mpl_ellipse.set_height(2*self.ellipse.minor)
        self._mpl_ellipse.set_edgecolor(self.edgecolor)
        self._mpl_ellipse.set_facecolor(self.facecolor)
