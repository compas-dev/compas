from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas.geometry import Cone

from ._exceptions import ConversionError

from ._shapes import cone_to_rhino
from ._shapes import cone_to_compas

from ._geometry import RhinoGeometry


class RhinoCone(RhinoGeometry):
    """Wrapper for Rhino cones."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Cone` | :class:`~compas.geometry.Cone`
            The geometry object defining a cone.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a cone.
        """
        if not isinstance(geometry, Rhino.Geometry.Cone):
            if isinstance(geometry, Rhino.Geometry.Brep):
                if geometry.Faces.Count > 2:
                    raise ConversionError("Object brep cannot be converted to a cone.")
                faces = geometry.Faces
                geometry = None
                for face in faces:
                    if face.IsCone():
                        result, geometry = face.TryGetCone()
                        if result:
                            break
                if not geometry:
                    raise ConversionError("Object brep cannot be converted to a cone.")
            elif isinstance(geometry, Cone):
                geometry = cone_to_rhino(geometry)
            else:
                raise ConversionError("Geometry object cannot be converted to a cone: {}".format(geometry))
        self._geometry = geometry

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`~compas.geometry.Cone`
            A COMPAS cone.
        """
        return cone_to_compas(self.geometry)
