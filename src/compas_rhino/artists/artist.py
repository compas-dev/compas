from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time

import compas
import compas_rhino
from compas.geometry import Object3D

try:
    import rhinoscriptsyntax as rs

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['Artist']


_ITEM_ARTIST = {}


class Artist(Object3D):
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

    def __init__(self, geometry=None, attributes=None, layer=None):
        self._layer = None
        self.layer = layer
        self.defaults = {
            'color.point'   : (255, 255, 255),
            'color.line'    : (0, 0, 0),
            'color.polygon' : (210, 210, 210),
        }

        self._last_transformation = None
        super(Artist, self).__init__(geometry, attributes)

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

    @staticmethod
    def register(item_type, artist_type):
        _ITEM_ARTIST[item_type] = artist_type

    @staticmethod
    def build(item, **kwargs):
        artist_type = _ITEM_ARTIST[type(item)]
        artist = artist_type(item, **kwargs)
        return artist

    def add(self, item, **kwargs):
        if isinstance(item, Artist):
            artist = item
        else:
            artist = self.build(item, **kwargs)
        self.add_child(artist)
        return artist

    def remove(self, item):
        self.remove_child(item)

    def _update_to_rhino(self):
        if hasattr(self, 'GUID'):
            T = self.transformation_world
            if self._last_transformation is not None:
                T = self._last_transformation.inverse() * T
            rs.TransformObject(self.GUID, T.matrix)
            self._last_transformation = self.transformation_world.copy()

    def draw(self, timeout=None):
        """Update and draw the bounded compas geometry in rhino"""
        self._update_to_rhino()
        for c in self.children:
            c._update_to_rhino()
        self.redraw(timeout)

    def hide(self):
        rs.HideObject(self.GUID)

    def show(self):
        rs.ShowObject(self.GUID)

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
            Default is ``None``, in which case the current layer is used.
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

        Notes
        -----
        The attributes required for drawing a point are stored in a dictionary per point.
        The dictionary has the following structure:

        .. code-block:: none

            {
                'pos'   : point,
                'name'  : str,         # optional
                'color' : rgb or hex,  # optional
                'layer' : str          # optional, defaults to the value of the parameter ``layer``.
            }

        """
        layer = layer or self.layer
        return compas_rhino.draw_points(points, layer=layer, clear=clear_layer, redraw=redraw)

    def draw_lines(self, lines, layer=None, clear_layer=False, redraw=False):
        """Draw a collection of lines.

        Parameters
        ----------
        lines : list of dict
            The lines to draw.
        layer : str, optional
            The layer to draw the points in.
            Default is ``None``, in which case the current layer is used.
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

        Notes
        -----
        The attributes required for drawing a line are stored in a dictionary per line.
        The dictionary has the following structure:

        .. code-block:: none

            {
                'start' : point,
                'end'   : point,
                'name'  : str,                      # optional
                'color' : rgb or hex,               # optional
                'layer' : str,                      # optional, defaults to the value of the parameter ``layer``.
                'width' : float,                    # optional, modifies the plot weight if not None.
                'arrow' : {'start', 'end', 'both'}  # optional
            }

        """
        layer = layer or self.layer
        return compas_rhino.draw_lines(lines, layer=layer, clear=clear_layer, redraw=redraw)

    def draw_polylines(self, polylines, layer=None, clear_layer=False, redraw=False):
        """Draw a collection of polygons.

        Parameters
        ----------
        polylines : list of dict
            The polylines to draw.
        layer : str, optional
            The layer to draw the points in.
            Default is ``None``, in which case the current layer is used.
        clear_layer : bool, optional
            Clear the specified layer.
            Default is ``False``.
        redraw : bool, optional
            Redraw the Rhino view.
            Default is ``False``.

        Returns
        -------
        list of guid
            The GUIDs of the polyline objects.

        Notes
        -----
        The attributes required for drawing a polyline are stored in a dictionary per polyline.
        The dictionary has the following structure:

        .. code-block:: none

            {
                'points' : list of point,
                'name'   : str,                      # optional
                'color'  : rgb or hex,               # optional
                'layer'  : str,                      # optional, defaults to the value of the parameter ``layer``.
                'width'  : float,                    # optional, modifies the plot weight if not None.
                'arrow'  : {'start', 'end', 'both'}  # optional
            }

        """
        layer = layer or self.layer
        return compas_rhino.draw_polylines(polylines, layer=layer, clear=clear_layer, redraw=redraw)

    def draw_polygons(self, polygons, layer=None, clear_layer=False, redraw=False):
        """Draw a collection of polygons.

        Parameters
        ----------
        polylines : list of dict
            The polygons to draw.
        layer : str, optional
            The layer to draw the points in.
            Default is ``None``, in which case the current layer is used.
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

        Notes
        -----
        The attributes required for drawing a polygon are stored in a dictionary per polygon.
        The dictionary has the following structure:

        .. code-block:: none

            {
                'points' : list of point,
                'name'   : str,                      # optional
                'color'  : rgb or hex,               # optional
                'layer'  : str,                      # optional, defaults to the value of the parameter ``layer``.
                'width'  : float,                    # optional, modifies the plot weight if not None.
                'arrow'  : {'start', 'end', 'both'}  # optional
            }

        Note that the draing of polygons currently falls back on the drawing of polylines.
        The polygon should therefore be closed expicitly, but this is done for you,
        on te fly...

        """
        layer = layer or self.layer
        for polygon in polygons:
            if polygon['points'][0] != polygon['points'][-1]:
                polygon['points'] = polygon['points'][:] + polygon['points'][:1]
        return compas_rhino.draw_polylines(polygons, layer=layer, clear=clear_layer, redraw=redraw)

    def draw_circles(self, circles, layer=None, clear_layer=False, redraw=False):
        """Draw a collection of circles.

        Parameters
        ----------
        circles : list of dict
            The circles to draw.
        layer : str, optional
            The layer to draw the points in.
            Default is ``None``, in which case the current layer is used.
        clear_layer : bool, optional
            Clear the specified layer.
            Default is ``False``.
        redraw : bool, optional
            Redraw the Rhino view.
            Default is ``False``.

        Returns
        -------
        list of guid
            The GUIDs of the circle objects.

        Notes
        -----
        The attributes required for drawing a circle are stored in a dictionary per circle.
        The dictionary has the following structure:

        .. code-block:: none

            {
                'plane'  : (point, normal),
                'radius' : float
                'name'   : str,              # optional
                'color'  : rgb or hex,       # optional
                'layer'  : str               # optional, defaults to the value of the parameter ``layer``.
            }

        """
        layer = layer or self.layer
        return compas_rhino.draw_circles(circles, layer=layer, clear=clear_layer, redraw=redraw)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas_rhino.utilities import unload_modules
    unload_modules("compas")
    unload_modules("compas_rhino")

    from compas.geometry import Point
    from compas.geometry import Rotation
    from compas_rhino.artists import PointArtist
    from compas_rhino.artists import Artist
    import math

    # create a artist as container to draw everything inside it
    artist = Artist()

    # add point directly
    artist.add(Point(10, 0, 0))

    # add point with attributes
    artist.add(Point(0, 10, 0), attributes={'color': (255, 0, 0)})

    # add point through PointArtist
    pa1 = PointArtist(Point(-10, 0, 0))
    artist.add(pa1)

    # add point with attributes through PointArtist
    pa2 = PointArtist(Point(0, -10, 0), attributes={'color': (0, 255, 0)})
    artist.add(pa2)

    R = Rotation.from_axis_and_angle([0, 0, 1], math.pi / 40)

    for i in range(0, 20):
        artist.apply_transformation(R)
        artist.draw(0.1)

    print('finished!')
