from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time

import compas
import compas_rhino

try:
    import rhinoscriptsyntax as rs

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['Artist']


class Artist(object):
    """The base ``Artist`` defines functionality for drawing geometric primitives in Rhino.

    Parameters
    ----------
    layer : str, optional
        The name of the layer that will contain the mesh.

    Attributes
    ----------
    layer : str
        The layer that will contain the drawing results.
    defaults : dict
        Default values for the representation of primitives.
        The following defaults are built in.

        * ``'color.point'`` : (255, 255, 255)
        * ``'color.line'`` : (0, 0, 0)
        * ``'color.polygon'`` : (210, 210, 210)

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas_rhino.artists import MeshArtist

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        artist = Artist(layer='COMPAS::MeshArtist')
        artist.clear_layer()
        artist.redraw()

    """

    __module__ = "compas_rhino.artists"

    def __init__(self, layer=None):
        self._layer = None
        self.layer = layer
        self.defaults = {
            'color.point'   : (255, 255, 255),
            'color.line'    : (0, 0, 0),
            'color.polygon' : (210, 210, 210),
        }

    @property
    def layer(self):
        """str: The layer that contains the mesh."""
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value

    def redraw(self, timeout=None):
        """Redraw the Rhino view.

        Parameters
        ----------
        timeout : float, optional
            The amount of time the artist waits before updating the Rhino view.
            The time should be specified in seconds.
            Default is ``None``.

        """
        if timeout:
            time.sleep(timeout)
        rs.EnableRedraw(True)
        rs.Redraw()

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)
        else:
            compas_rhino.clear_current_layer()

    # ==========================================================================
    # save image, video, gif, ...
    # ==========================================================================

    def save(self, path, width=1920, height=1080, scale=1,
             draw_grid=False, draw_world_axes=False, draw_cplane_axes=False, background=False):
        """Save the current screen view.

        Parameters
        ----------
        path : str
            The path where the screenshot should be saved.
        width : int, optional
            The width of the saved image.
            Default is ``1920``.
        height : int, optional
            The height of the saved image.
            Default is ``1080``.
        scale : float, optional
            Scaling factor for the saved view.
            Default is ``1``.
        draw_grid : bool, optional
            Include the grid in the screenshot.
            Default is ``False``.
        draw_world_axes : bool, optional
            Include the world axes in the screenshot.
            Default is ``False``.
        draw_cplane_axes : bool, optional
            Include the CPlane axes in the screenshot.
            Default is ``False``.
        background : bool, optional
            Include the current background in the screenshot.
            Default is ``False``.

        Returns
        -------
        str
            The path where the file was saved.

        """
        return compas_rhino.screenshot_current_view(path,
                                                    width=width,
                                                    height=height,
                                                    scale=scale,
                                                    draw_grid=draw_grid,
                                                    draw_world_axes=draw_world_axes,
                                                    draw_cplane_axes=draw_cplane_axes,
                                                    background=background)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
