from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import ellipse_to_rhino

from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class EllipseObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing ellipses.

    Parameters
    ----------
    ellipse : :class:`compas.geometry.Ellipse`
        A COMPAS ellipse.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, ellipse, **kwargs):
        super(EllipseObject, self).__init__(geometry=ellipse, **kwargs)

    def draw(self, color=None):
        """Draw the ellipse.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the ellipse.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        ellipse = ellipse_to_rhino(self.geometry)
        ellipse = ellipse.ToNurbsCurve()
        ellipse.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddCurve(ellipse, attr)]
        return self.guids
