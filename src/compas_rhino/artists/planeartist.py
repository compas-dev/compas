from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import compas_rhino
from compas_rhino.artists._primitiveartist import PrimitiveArtist


__all__ = ['PlaneArtist']


class PlaneArtist(PrimitiveArtist):

    def draw(self):
        """Draw the plane.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        raise NotImplementedError
