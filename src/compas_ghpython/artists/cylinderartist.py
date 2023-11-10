from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .artist import GHArtist


class CylinderArtist(GHArtist, GeometryObject):
    """Artist for drawing cylinder shapes.

    Parameters
    ----------
    cylinder : :class:`~compas.geometry.Cylinder`
        A COMPAS cylinder.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, cylinder, **kwargs):
        super(CylinderArtist, self).__init__(geometry=cylinder, **kwargs)

    def draw(self, color=None, u=16):
        """Draw the cylinder associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the box.
        u : int, optional
            Number of faces in the "u" direction.

        Returns
        -------
        :rhino:`Rhino.Geometry.Mesh`

        """
        geometry = conversions.cylinder_to_rhino_brep(self.geometry)

        if self.transformation:
            geometry.Transform(conversions.transformation_to_rhino(self.transformation))

        return geometry
