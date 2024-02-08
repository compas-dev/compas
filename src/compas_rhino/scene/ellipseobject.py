from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import ellipse_to_rhino

from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject


class RhinoEllipseObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing ellipses.

    Parameters
    ----------
    ellipse : :class:`compas.geometry.Ellipse`
        A COMPAS ellipse.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, ellipse, **kwargs):
        super(RhinoEllipseObject, self).__init__(geometry=ellipse, **kwargs)

    def draw(self):
        """Draw the ellipse.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        attr = self.compile_attributes()
        ellipse = ellipse_to_rhino(self.geometry)
        ellipse = ellipse.ToNurbsCurve()
        ellipse.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddCurve(ellipse, attr)]
        return self.guids
