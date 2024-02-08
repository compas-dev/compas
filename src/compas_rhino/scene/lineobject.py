from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject


class RhinoLineObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing lines.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        A COMPAS line.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, line, **kwargs):
        super(RhinoLineObject, self).__init__(geometry=line, **kwargs)

    def draw(self):
        """Draw the line.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        attr = self.compile_attributes()
        geometry = line_to_rhino(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddLine(geometry, attr)]
        return self.guids
