from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import surface_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class SurfaceObject(RhinoSceneObject, GeometryObject):
    """Sceneobject for drawing surfaces.

    Parameters
    ----------
    surface : :class:`~compas.geometry.Geometry`
        A COMPAS surface.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, surface, **kwargs):
        super(SurfaceObject, self).__init__(geometry=surface, **kwargs)

    def draw(self, color=None):
        """Draw the surface.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the surface.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)
        surface = surface_to_rhino(self.geometry)
        return sc.doc.Objects.AddSurface(surface, attr)
