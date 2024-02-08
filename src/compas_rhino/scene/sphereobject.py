from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from .helpers import attributes


class SphereObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing sphere shapes.

    Parameters
    ----------
    sphere : :class:`compas.geometry.Sphere`
        A COMPAS sphere.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, sphere, **kwargs):
        super(SphereObject, self).__init__(geometry=sphere, **kwargs)

    def draw(self):
        """Draw the sphere associated with the scene object.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        attr = attributes(name=self.geometry.name, color=self.color, layer=self.layer)
        geometry = sphere_to_rhino(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddSphere(geometry, attr)]
        return self.guids
