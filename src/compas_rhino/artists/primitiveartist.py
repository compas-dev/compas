from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

try:
    import rhinoscriptsyntax as rs

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['PrimitiveArtist']


class PrimitiveArtist(object):

    __module__ = "compas_rhino.artists"

    # ==========================================================================
    # drawing functions
    # ==========================================================================

    @staticmethod
    def draw_points(points, layer=None, clear_layer=False, redraw=False):
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
        return compas_rhino.draw_points(points, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_lines(lines, layer=None, clear_layer=False, redraw=False):
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
        return compas_rhino.draw_lines(lines, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_polylines(polylines, layer=None, clear_layer=False, redraw=False):
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
        return compas_rhino.draw_polylines(polylines, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
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
        for polygon in polygons:
            if polygon['points'][0] != polygon['points'][-1]:
                polygon['points'] = polygon['points'][:] + polygon['points'][:1]
        return compas_rhino.draw_polylines(polygons, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_circles(circles, layer=None, clear_layer=False, redraw=False):
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
        return compas_rhino.draw_circles(circles, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_labels(labels, layer=None, clear_layer=False, redraw=False):
        """Draw labels as text dots and optionally set individual font, fontsize, name and color.

        Parameters
        ----------
        labels : list of dict
            A list of labels dictionaries.
            A label dictionary has the following structure:

            .. code-block:: python

                {
                    'pos'  : [x, y, z],
                    'text' : '',
                    'name' : ''
                }

        """
        return compas_rhino.draw_labels(labels, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_geodesics(geodesics, layer=None, clear_layer=False, redraw=False):
        """Draw geodesic lines on specified surfaces, and optionally set individual
        name, color, arrow, and layer properties.
        """
        return compas_rhino.draw_labels(geodesics, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_breps(faces, srf=None, u=10, v=10, trim=True, tangency=True, spacing=0.1, flex=1.0, pull=1.0, layer=None, clear_layer=False, redraw=False):
        """Draw polygonal faces as Breps, and optionally set individual name, color,
        and layer properties.
        """
        return compas_rhino.draw_breps(faces, srf, u, v, trim, tangency, spacing, flex, pull, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_cylinders(cylinders, cap=False, layer=None, clear_layer=False, redraw=False):
        return compas_rhino.draw_cylinders(cylinders, cap, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_pipes(pipes, cap=2, fit=1.0, layer=None, clear_layer=False, redraw=False):
        return compas_rhino.draw_pipes(pipes, cap, fit, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_spheres(spheres, layer=None, clear_layer=False, redraw=False):
        return compas_rhino.draw_spheres(spheres, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_mesh(vertices, faces, name=None, color=None, disjoint=False, layer=None, clear_layer=False, redraw=False):
        return compas_rhino.draw_mesh(vertices, faces, name, color, disjoint, layer=layer, clear=clear_layer, redraw=redraw)

    @staticmethod
    def draw_faces(faces, layer=None, clear_layer=False, redraw=False):
        return compas_rhino.draw_faces(faces, layer=layer, clear=clear_layer, redraw=redraw)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
