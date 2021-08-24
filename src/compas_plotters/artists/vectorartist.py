from typing import Tuple, List, Optional
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import ArrowStyle
from compas.geometry import Point, Vector
from compas_plotters.artists import Artist

Color = Tuple[float, float, float]


class VectorArtist(Artist):
    """Artist for COMPAS vectors."""

    zorder: int = 3000

    def __init__(self,
                 vector: Vector,
                 point: Optional[Point] = None,
                 draw_point: bool = False,
                 color: Color = (0, 0, 0)):
        super(VectorArtist, self).__init__(vector)
        self._mpl_vector = None
        self._point_artist = None
        self.draw_point = draw_point
        self.point = point or Point(0.0, 0.0, 0.0)
        self.vector = vector
        self.color = color

    @property
    def data(self) -> List[List[float]]:
        return [self.point[:2], (self.point + self.vector)[:2]]

    def draw(self) -> None:
        style = ArrowStyle("Simple, head_length=.1, head_width=.1, tail_width=.02")
        arrow = FancyArrowPatch(self.point[:2], (self.point + self.vector)[:2],
                                arrowstyle=style,
                                edgecolor=self.color,
                                facecolor=self.color,
                                zorder=self.zorder,
                                mutation_scale=100)
        if self.draw_point:
            self._point_artist = self.plotter.add(self.point, edgecolor=self.color)
        self._mpl_vector = self.plotter.axes.add_patch(arrow)

    def redraw(self):
        self._mpl_vector.set_positions(self.point[:2], (self.point + self.vector)[:2])
        if self.draw_point:
            self._point_artist.redraw()
