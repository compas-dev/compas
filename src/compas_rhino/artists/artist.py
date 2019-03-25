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

    # ==========================================================================
    # drawing functions
    # ==========================================================================

    def draw_points(self, points, layer=None, clear_layer=False, redraw=False):
        """Draw a collection of points.

        Parameters
        ----------
        points : list of dict
            The points to draw.
        layer : str, optional
            The layer to draw the points in.
            Default is ``None``.
        clear_layer : bool, optional
            Clear the specified layer.
            Default is ``False``.
        redraw : bool, optional
            Redraw the Rhino view.
            Default is ``False``.

        Returns
        -------
        list of guid
            The GUIDs of the point objects.

        """
        layer = layer or self.layer
        return compas_rhino.xdraw_points(points, layer=layer, clear=clear_layer, redraw=redraw)

    def draw_lines(self, lines, layer=None, clear_layer=False, redraw=False):
        """Draw a collection of lines.

        Parameters
        ----------
        lines : list of dict
            The lines to draw.
        layer : str, optional
            The layer to draw the points in.
            Default is ``None``.
        clear_layer : bool, optional
            Clear the specified layer.
            Default is ``False``.
        redraw : bool, optional
            Redraw the Rhino view.
            Default is ``False``.

        Returns
        -------
        list of guid
            The GUIDs of the line objects.

        """
        layer = layer or self.layer
        return compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer, redraw=redraw)

    def draw_polygons(self, polygons, layer=None, clear_layer=False, redraw=False):
        """Draw a collection of polygons.

        Parameters
        ----------
        points : list of dict
            The points to draw.
        layer : str, optional
            The layer to draw the points in.
            Default is ``None``.
        clear_layer : bool, optional
            Clear the specified layer.
            Default is ``False``.
        redraw : bool, optional
            Redraw the Rhino view.
            Default is ``False``.

        Returns
        -------
        list of guid
            The GUIDs of the polygon objects.

        """
        layer = layer or self.layer
        return compas_rhino.xdraw_polylines(polygons, layer=layer, clear=clear_layer, redraw=redraw)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures import Mesh
    from compas.geometry import Polyhedron

    from compas_rhino.artists.meshartist import MeshArtist

    poly = Polyhedron.generate(12)

    mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

    artist = MeshArtist(mesh)

    artist.clear()

    artist.draw_vertices()
    artist.redraw(0.0)

    artist.draw_vertexlabels()
    artist.redraw(1.0)

    artist.draw_faces()
    artist.redraw(1.0)

    artist.draw_facelabels()
    artist.redraw(1.0)

    artist.draw_edges()
    artist.redraw(1.0)

    artist.draw_edgelabels()
    artist.redraw(1.0)
