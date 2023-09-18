from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import box_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class BoxArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing box shapes.

    Parameters
    ----------
    box : :class:`~compas.geometry.Box`
        A COMPAS box.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, box, **kwargs):
        super(BoxArtist, self).__init__(geometry=box, **kwargs)

    def draw(self, color=None):
        """Draw the box associated with the artist.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the box.

        Returns
        -------
        System.Guid
            The GUID of the object created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = box_to_rhino(self.geometry)

        if self.transformation:
            transformation = transformation_to_rhino(self.transformation)
            geometry.Transform(transformation)

        return sc.doc.Objects.AddBox(geometry, attr)
