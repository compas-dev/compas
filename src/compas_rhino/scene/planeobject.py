from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.geometry import Frame
from compas.scene import GeometryObject
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino

from .sceneobject import RhinoSceneObject


class RhinoPlaneObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing planes.

    Parameters
    ----------
    scale : float, optional
        Scale factor.
        Default is ``1.0``.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    scale : float
        Scale factor.
        Default is ``1.0``.

    """

    def __init__(self, scale=1.0, **kwargs):
        super(RhinoPlaneObject, self).__init__(**kwargs)
        self.scale = scale

    def draw(self):
        """Draw the plane.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        frame = Frame.from_plane(self._item)

        guids = [
            sc.doc.Objects.AddLine(
                point_to_rhino(frame.to_world_coordinates([0, 0, 0])),
                point_to_rhino(frame.to_world_coordinates([0, 0, self.scale])),
            )
        ]

        vertices = [
            frame.to_world_coordinates([-self.scale, -self.scale, 0]),
            frame.to_world_coordinates([self.scale, -self.scale, 0]),
            frame.to_world_coordinates([self.scale, self.scale, 0]),
            frame.to_world_coordinates([-self.scale, self.scale, 0]),
        ]
        faces = [[0, 1, 2, 3]]
        mesh = vertices_and_faces_to_rhino(vertices, faces)
        guids.append(sc.doc.Objects.AddMesh(mesh))

        transformation = transformation_to_rhino(self.worldtransformation)
        for guid in guids:
            obj = sc.doc.Objects.Find(guid)
            if obj:
                obj.Geometry.Transform(transformation)
                obj.CommitChanges()

        self._guids = guids
        return self.guids
