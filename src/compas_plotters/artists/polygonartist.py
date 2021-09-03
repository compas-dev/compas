from typing import Literal, Tuple, List
from matplotlib.patches import Polygon as PolygonPatch
from compas.geometry import Polygon
from compas_plotters.artists import Artist

Color = Tuple[float, float, float]


class PolygonArtist(Artist):
    """Artist for COMPAS polygons."""

    zorder: int = 1000

    def __init__(self,
                 polygon: Polygon,
                 linewidth: float = 1.0,
                 linestyle: Literal['solid', 'dotted', 'dashed', 'dashdot'] = 'solid',
                 facecolor: Color = (1.0, 1.0, 1.0),
                 edgecolor: Color = (0, 0, 0),
                 fill: bool = True,
                 alpha: float = 1.0):
        super(PolygonArtist, self).__init__(polygon)
        self._mpl_polygon = None
        self.polygon = polygon
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.fill = fill
        self.alpha = alpha

    @property
    def data(self) -> List[List[float]]:
        return [point[:2] for point in self.polygon.points]

    def draw(self) -> None:
        polygon = PolygonPatch(self.data,
                               linewidth=self.linewidth,
                               linestyle=self.linestyle,
                               facecolor=self.facecolor,
                               edgecolor=self.edgecolor,
                               zorder=self.zorder,
                               alpha=self.alpha,
                               fill=self.fill)
        self._mpl_polygon = self.plotter.axes.add_patch(polygon)

    def redraw(self) -> None:
        self._mpl_polygon.set_xy(self.data)
        self._mpl_polygon.set_facecolor(self.facecolor)
        self._mpl_polygon.set_edgecolor(self.edgecolor)
        self._mpl_polygon.set_linewidth(self.linewidth)
