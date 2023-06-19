from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from System.Drawing.Color import FromArgb
from Rhino.Geometry import Point3d

from compas.utilities import iterable_like
from compas.utilities import is_sequence_of_iterable

from .base import BaseConduit


class FacesConduit(BaseConduit):
    """A Rhino display conduit for faces.

    Parameters
    ----------
    vertices : list[[float, float, float] | :class:`~compas.geometry.Point`]
        The coordinates of the vertices of the faces.
    faces : list[list[int]]
        The faces defined as lists of indices in `vertices`.
    color : tuple[int, int, int] or list[tuple[int, int, int]], optional
        The colors of the faces.
        Default is None, in which case the default color is used for all faces (:attr:`FacesConduit.default_color`).

    Attributes
    ----------
    color : list[System.Drawing.Color]
        The color specification per face.

    Class Attributes
    ----------------
    default_color : System.Drawing.Color
        The default color is ``FromArgb(255, 255, 255)``.

    Examples
    --------
    .. code-block:: python

        from compas.geometry import Polyhedron
        from compas_rhino.conduits import FacesConduit

        polyhedron = Polyhedron.generate(6)
        conduit = FacesConduit(polyhedron.vertices, polyhedron.faces)

        with conduit.enabled():
            conduit.redraw(pause=5.0)

    """

    default_color = FromArgb(255, 255, 255)

    def __init__(self, vertices, faces, color=None, **kwargs):
        super(FacesConduit, self).__init__(**kwargs)
        self._color = None
        self.vertices = vertices or []
        self.faces = faces or []
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if not color:
            return
        if not is_sequence_of_iterable(color):
            color = [color]
        color = [FromArgb(*c) for c in iterable_like(self.faces, color, self.default_color)]
        self._color = color

    def DrawForeground(self, e):
        """Draw the faces as polygons.

        Parameters
        ----------
        e : Rhino.Display.DrawEventArgs

        Returns
        -------
        None

        """
        for i, face in enumerate(self.faces):
            points = [Point3d(*self.vertices[key]) for key in face]
            if self.color:
                e.Display.DrawPolygon(points, self.color[i], True)
            else:
                e.Display.DrawPolygon(points, self.default_color, True)
