from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import surface_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from .helpers import attributes


class SurfaceObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing surfaces.

    Parameters
    ----------
    surface : :class:`compas.geometry.Geometry`
        A COMPAS surface.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, surface, **kwargs):
        super(SurfaceObject, self).__init__(geometry=surface, **kwargs)

    def draw(self):
        """Draw the surface.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        attr = attributes(name=self.geometry.name, color=self.color, layer=self.layer)
        surface = surface_to_rhino(self.geometry)
        surface.Transform(transformation_to_rhino(self.worldtransformation))
        self._guids = [sc.doc.Objects.AddSurface(surface, attr)]
        return self.guids
