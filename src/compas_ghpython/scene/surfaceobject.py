from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class SurfaceObject(GHSceneObject, GeometryObject):
    """Scene object for drawing surfaces."""

    def draw(self):
        """Draw the surface.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Surface`]
            The created Rhino surfaces.

        """
        geometry = conversions.surface_to_rhino(self.geometry)
        geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [geometry]
        return self.guids
