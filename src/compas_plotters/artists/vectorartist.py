from typing import Tuple
from typing import List
from typing import Any
from typing import Optional

from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import ArrowStyle
from compas.geometry import Point, Vector

from compas.artists import PrimitiveArtist
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class VectorArtist(PlotterArtist, PrimitiveArtist):
    """Artist for COMPAS vectors.

    Parameters
    ----------
    vector : :class:`~compas.geometry.Vector`
        A COMPAS vector.
    point : :class:`~compas.geometry.Point`, optional
        A COMPAS point as base point for the vector.
        Default is the origin of the world coordinate system.
    draw_point : bool, optional
        If True, draw the point of application of the vector.
    color : tuple[float, float, float], optional
        Color of the vector.
    zorder : int, optional
        Stacking order of the vector on the canvas.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_plotters.artists.PlotterArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    Attributes
    ----------
    vector : :class:`~compas.geometry.Vector`
        The vector associated with the artist.

    """

    def __init__(
        self,
        vector: Vector,
        point: Optional[Point] = None,
        draw_point: bool = False,
        color: Color = (0, 0, 0),
        zorder: int = 3000,
        **kwargs: Any
    ):

        super().__init__(primitive=vector, **kwargs)

        self._mpl_vector = None
        self._point_artist = None
        self.draw_point = draw_point
        self.point = point or Point(0.0, 0.0, 0.0)
        self.color = color
        self.zorder = zorder

    @property
    def vector(self):
        return self.primitive

    @vector.setter
    def vector(self, vector):
        self.primitive = vector

    @property
    def data(self) -> List[List[float]]:
        return [self.point[:2], (self.point + self.vector)[:2]]

    def draw(self) -> None:
        """Draw the vector.

        Returns
        -------
        None

        """
        style = ArrowStyle("Simple, head_length=0.1, head_width=0.1, tail_width=0.02")
        arrow = FancyArrowPatch(
            self.point[:2],
            (self.point + self.vector)[:2],
            arrowstyle=style,
            edgecolor=self.color,
            facecolor=self.color,
            zorder=self.zorder,
            mutation_scale=100,
        )
        if self.draw_point:
            self._point_artist = self.plotter.add(self.point, edgecolor=self.color)
        self._mpl_vector = self.plotter.axes.add_patch(arrow)

    def redraw(self):
        """Update the vector using the current geometry and visualization settings.

        Returns
        -------
        None

        """
        self._mpl_vector.set_positions(self.point[:2], (self.point + self.vector)[:2])
        if self.draw_point:
            self._point_artist.redraw()
