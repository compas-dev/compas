from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas.geometry import Sphere

from ._exceptions import ConversionError

from ._shapes import sphere_to_rhino
from ._shapes import sphere_to_compas

from ._geometry import RhinoGeometry


class RhinoSphere(RhinoGeometry):
    """Wrapper for Rhino spheres."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Sphere` | :class:`~compas.geometry.Sphere`
            The geometry object defining a sphere.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a sphere.
        """
        if not isinstance(geometry, Rhino.Geometry.Sphere):
            if isinstance(geometry, Rhino.Geometry.Brep):
                if geometry.Faces.Count != 1:
                    raise ConversionError("Object brep cannot be converted to a sphere.")
                face = geometry.Faces.Item[0]
                if not face.IsSphere():
                    raise ConversionError("Object brep cannot be converted to a sphere.")
                result, geometry = face.TryGetSphere()
                if not result:
                    raise ConversionError("Object brep cannot be converted to a sphere.")
            elif isinstance(geometry, Sphere):
                geometry = sphere_to_rhino(geometry)
            else:
                raise ConversionError("Geometry object cannot be converted to a sphere: {}".format(geometry))
        self._geometry = geometry

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`~compas.geometry.Sphere`
            A COMPAS sphere.
        """
        return sphere_to_compas(self.geometry)
