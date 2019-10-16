from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import shutil

import subprocess

from contextlib import contextmanager

import matplotlib
import matplotlib.pyplot as plt

from matplotlib.patches import Circle

from compas_plotters.core.drawing import create_axes_xy
from compas_plotters.core.drawing import draw_xpoints_xy
from compas_plotters.core.drawing import draw_xlines_xy
from compas_plotters.core.drawing import draw_xpolylines_xy
from compas_plotters.core.drawing import draw_xpolygons_xy
from compas_plotters.core.drawing import draw_xarrows_xy


__all__ = ['Plotter2']


class Plotter2(object):
    """"""
    def __init__(self, figsize=(16.0, 12.0), tight=True, **kwargs):
        """Initialises a plotter object"""
        self._axes = None
        self.tight = tight
        self.figure_size = figsize
        self.figure_dpi = dpi
        self.figure_bgcolor = '#ffffff'
        self.axes_xlabel = None
        self.axes_ylabel = None
        self.defaults = {
            'point.radius'    : 0.1,
            'point.facecolor' : '#ffffff',
            'point.edgecolor' : '#000000',
            'point.edgewidth' : 0.5,
            'point.textcolor' : '#000000',
            'point.fontsize'  : kwargs.get('fontsize', 10),

            'line.width'    : 1.0,
            'line.color'    : '#000000',
            'line.textcolor': '#000000',
            'line.fontsize' : kwargs.get('fontsize', 10),

            'polygon.facecolor' : '#ffffff',
            'polygon.edgecolor' : '#000000',
            'polygon.edgewidth' : 0.1,
            'polygon.textcolor' : '#000000',
            'polygon.fontsize'  : kwargs.get('fontsize', 10),
        }

    @property
    def axes(self):
        """Returns the axes subplot matplotlib object.

        Returns
        -------
        Axes
            The matplotlib axes object.

        Notes
        -----
        For more info, see the documentation of the Axes class ([1]_) and the
        axis and tick API ([2]_).

        References
        ----------
        .. [1] https://matplotlib.org/api/axes_api.html
        .. [2] https://matplotlib.org/api/axis_api.html

        """
        if self._axes is None:
            self._axes = create_axes_xy(
                figsize=self.figure_size,
                dpi=self.figure_dpi,
                xlabel=self.axes_xlabel,
                ylabel=self.axes_ylabel)
        return self._axes

    @property
    def figure(self):
        """Returns the matplotlib figure instance.

        Returns
        -------
        Figure
            The matplotlib figure instance.

        Notes
        -----
        For more info, see the figure API ([1]_).

        References
        ----------
        .. [1] https://matplotlib.org/2.0.2/api/figure_api.html

        """
        return self.axes.get_figure()

    @property
    def canvas(self):
        """Returns the canvas of the figure instance.
        """
        return self.figure.canvas

    @property
    def bgcolor(self):
        """Returns the background color.

        Returns
        -------
        str
            The color as a string (hex colors).

        """
        return self.figure.get_facecolor()

    @bgcolor.setter
    def bgcolor(self, value):
        """Sets the background color.

        Parameters
        ----------
        value : str, tuple
            The color specififcation for the figure background.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of normalized RGB components.

        """
        self.figure.set_facecolor(value)

    @property
    def title(self):
        """Returns the title of the plot.

        Returns
        -------
        str
            The title of the plot.

        """
        return self.figure.canvas.get_window_title()

    @title.setter
    def title(self, value):
        """Sets the title of the plot.

        Parameters
        ----------
        value : str
            The title of the plot.

        """
        self.figure.canvas.set_window_title(value)

    def register_listener(self, listener):
        """Register a listener for pick events.

        Parameters
        ----------
        listener : callable
            The handler for pick events.

        Returns
        -------
        None

        Notes
        -----
        For more information, see the docs of ``mpl_connect`` ([1]_), and on event
        handling and picking ([2]_).

        References
        ----------
        .. [1] https://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.FigureCanvasBase.mpl_connect
        .. [2] https://matplotlib.org/users/event_handling.html

        Examples
        --------
        .. code-block:: python

            #

        """
        self.figure.canvas.mpl_connect('pick_event', listener)

    def draw(self):
        self.canvas.draw()

    def show(self, autoscale=True):
        """Displays the plot.

        """
        if autoscale:
            self.axes.autoscale()
        if self.tight:
            plt.tight_layout()
        plt.show()

    def save(self, filepath, **kwargs):
        """Saves the plot to a file.

        Parameters
        ----------
        filepath : str
            Full path of the file.

        Notes
        -----
        For an overview of all configuration options, see [1]_.

        References
        ----------
        .. [1] https://matplotlib.org/2.0.2/api/pyplot_api.html#matplotlib.pyplot.savefig

        """
        self.axes.autoscale()
        plt.savefig(filepath, **kwargs)

    def update(self, pause=0.0001):
        """Updates and pauses the plot.

        Parameters
        ----------
        pause : float
            Ammount of time to pause the plot in seconds.

        """
        self.axes.autoscale()
        if self.tight:
            plt.tight_layout()
        plt.pause(pause)

    def update_pointcollection(self, collection, centers, radius=1.0):
        """Updates the location and radii of a point collection.

        Parameters
        ----------
        collection : object
            The point collection to update.
        centers : list
            List of tuples or lists with XY(Z) location for the points in the collection.
        radius : float or list, optional
            The radii of the points. If a floar is given it will be used for all points.

        """
        try:
            len(radius)
        except Exception:
            radius = [radius] * len(centers)
        data = zip(centers, radius)
        circles = [Circle(c[0:2], r) for c, r in data]
        collection.set_paths(circles)

    def update_linecollection(self, collection, segments):
        """Updates a line collection.

        Parameters
        ----------
        collection : object
            The line collection to update.
        segments : list
            List of tuples or lists with XY(Z) location for the start and end
            points in each line in the collection.

        """
        collection.set_segments([(start[0:2], end[0:2]) for start, end in segments])

    def update_polygoncollection(self, collection, polygons):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas.geometry import smooth_centroid

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

    points = []
    for key in mesh.vertices():
        points.append({
            'pos': mesh.vertex_coordinates(key),
            'radius': 0.1,
            'facecolor': '#ff0000' if mesh.vertex_degree(key) == 2 else '#ffffff'
        })

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u),
            'end': mesh.vertex_coordinates(v),
            'width': 1.0
        })

    plotter = Plotter(figsize=(10, 6))

    pcoll = plotter.draw_points(points)
    lcoll = plotter.draw_lines(lines)

    def callback(k, args):
        plotter.update_pointcollection(pcoll, vertices, 0.1)

        segments = []
        for u, v in mesh.edges():
            a = vertices[u][0:2]
            b = vertices[v][0:2]
            segments.append([a, b])

        plotter.update_linecollection(lcoll, segments)
        plotter.update(pause=0.001)

    vertices = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    adjacency = [mesh.vertex_neighbors(key) for key in mesh.vertices()]

    smooth_centroid(vertices,
                    adjacency,
                    fixed=fixed,
                    kmax=100,
                    callback=callback)

    plotter.show()
