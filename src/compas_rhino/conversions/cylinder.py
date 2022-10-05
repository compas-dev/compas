from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas.geometry import Cylinder

from ._exceptions import ConversionError

from ._shapes import cylinder_to_rhino
from ._shapes import cylinder_to_compas

from ._geometry import RhinoGeometry


class RhinoCylinder(RhinoGeometry):
    """Wrapper for Rhino cylinders."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Cylinder` | :class:`~compas.geometry.Cylinder`
            The geometry object defining a cylinder.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a cylinder.
        """
        if not isinstance(geometry, Rhino.Geometry.Cylinder):
            if isinstance(geometry, Rhino.Geometry.Extrusion):
                geometry = geometry.ToBrep()
            if isinstance(geometry, Rhino.Geometry.Brep):
                if geometry.Faces.Count > 3:
                    raise ConversionError("Object brep cannot be converted to a cylinder.")
                faces = geometry.Faces
                geometry = None
                for face in faces:
                    # being too strict about what is considered a cylinder
                    # results in cylinders created by Rhino itself
                    # to not be recognized...
                    if face.IsCylinder(0.001):
                        result, geometry = face.TryGetFiniteCylinder(0.001)
                        if result:
                            break
                if not geometry:
                    raise ConversionError("Object brep cannot be converted to a cylinder.")
            elif isinstance(geometry, Cylinder):
                geometry = cylinder_to_rhino(geometry)
            else:
                raise ConversionError("Geometry object cannot be converted to a cylinder: {}".format(geometry))
        self._geometry = geometry

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`~compas.geometry.Cylinder`
            A COMPAS cylinder.
        """
        return cylinder_to_compas(self.geometry)
