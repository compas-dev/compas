from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from System.Drawing.Color import FromArgb  # type: ignore
from Rhino.Geometry import Brep as RhinoBrep  # type: ignore
from Rhino.Geometry import PipeCapMode  # type: ignore
from Rhino.DocObjects.ObjectColorSource import ColorFromObject  # type: ignore
from Rhino.DocObjects import ObjectAttributes  # type: ignore

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import line_to_rhino_curve
from .artist import RhinoArtist


class CapsuleArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing capsule shapes.

    Parameters
    ----------
    capsule : :class:`~compas.geometry.Capsule`
        A COMPAS capsule.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ShapeArtist`.

    """

    def __init__(self, capsule, **kwargs):
        super(CapsuleArtist, self).__init__(geometry=capsule, **kwargs)

    def draw(self, color=None, u=16, v=16):
        """Draw the capsule associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the capsule.
            Default is :attr:`compas.artists.ShapeArtist.color`.
        u : int, optional
            Number of faces in the "u" direction.
            Default is 16.
        v : int, optional
            Number of faces in the "v" direction.
            Default is 16.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        # color = Color.coerce(color) or self.color
        # vertices, faces = self.geometry.to_vertices_and_faces(u=u, v=v)
        # vertices = [list(vertex) for vertex in vertices]
        # guid = compas_rhino.draw_mesh(
        #     vertices,
        #     faces,
        #     layer=self.layer,
        #     name=self.geometry.name,
        #     color=color.rgb255,  # type: ignore
        #     disjoint=True,
        # )
        # return [guid]

        color = Color.coerce(color) or self.color
        color = FromArgb(*color.rgb255)  # type: ignore

        abs_tol = sc.doc.ModelAbsoluteTolerance
        ang_tol = sc.doc.ModelAngleToleranceRadians

        radius = self.geometry.radius
        line = self.geometry.axis
        curve = line_to_rhino_curve(line)

        attr = ObjectAttributes()
        attr.ObjectColor = color
        attr.ColorSource = ColorFromObject

        breps = RhinoBrep.CreatePipe(curve, radius, False, PipeCapMode.Round, False, abs_tol, ang_tol)
        guids = [sc.doc.Objects.AddBrep(brep, attr) for brep in breps]

        return guids
