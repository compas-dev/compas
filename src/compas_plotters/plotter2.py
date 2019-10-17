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
from matplotlib.collections import CircleCollection

from compas_plotters.core.drawing import create_axes_xy
from compas_plotters.core.drawing import draw_xpoints_xy
from compas_plotters.core.drawing import draw_xlines_xy
from compas_plotters.core.drawing import draw_xpolylines_xy
from compas_plotters.core.drawing import draw_xpolygons_xy
from compas_plotters.core.drawing import draw_xarrows_xy


__all__ = ['Plotter2']


class Plotter2(object):
    """"""
    def __init__(self, figsize=(8, 5), tight=True, **kwargs):
        """Initialises a plotter object"""
        self._points = None
        self._lines = None
        self._axes = None
        self.tight = tight
        self.figure_size = figsize
        self.figure_dpi = 100
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
            self._axes = create_axes_xy(figsize=self.figure_size)
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
        self.figure.canvas.draw()

    def show(self):
        """Displays the plot.

        """
        self.axes.autoscale()
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

    def set_points(self, points):
        xys = []
        circles = []
        for point in points:
            pos = point['pos'][:2]
            radius = point.get('radius', self.defaults['point.radius'])
            circle = Circle(pos, radius=radius)
            circles.append(self.axes.add_artist(circle))
            xys.append(pos)
        self.axes.update_datalim(xys)
        return circles

    # def set_points2(self, points):
    #     circles = []
    #     sizes = []
    #     for point in points:
    #         pos = point['pos'][:2]
    #         radius = point.get('radius', self.defaults['point.radius'])
    #         # circle = Circle(pos, radius=radius)
    #         # circles.append(circle)
    #         sizes.append(radius)
    #     collection = CircleCollection(sizes)
    #     self.axes.add_collection(collection, autolim=True)
    #     return collection

    def clear_points(self):
        self._points = None

    # def update_pointcollection(self, collection, centers, radius=1.0):
    #     """Updates the location and radii of a point collection.

    #     Parameters
    #     ----------
    #     collection : object
    #         The point collection to update.
    #     centers : list
    #         List of tuples or lists with XY(Z) location for the points in the collection.
    #     radius : float or list, optional
    #         The radii of the points. If a floar is given it will be used for all points.

    #     """
    #     try:
    #         len(radius)
    #     except Exception:
    #         radius = [radius] * len(centers)
    #     data = zip(centers, radius)
    #     circles = [Circle(c[0:2], r) for c, r in data]
    #     collection.set_paths(circles)

    # def update_linecollection(self, collection, segments):
    #     """Updates a line collection.

    #     Parameters
    #     ----------
    #     collection : object
    #         The line collection to update.
    #     segments : list
    #         List of tuples or lists with XY(Z) location for the start and end
    #         points in each line in the collection.

    #     """
    #     collection.set_segments([(start[0:2], end[0:2]) for start, end in segments])

    # def update_polygoncollection(self, collection, polygons):
    #     raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import time

    plotter = Plotter2(figsize=(10, 6))
    plotter.bgcolor = '#cccccc'
    circles = plotter.set_points([{'pos': [2, 3], 'radius': 1.0}, {'pos': [5, 0], 'radius': 1.0}])
    # plotter.axes.set_xlim(0, 10)
    # plotter.axes.set_ylim(0, 6)
    for i in range(10):
        if i % 2:
            circles[0].center[0] += 0.5
        else:
            circles[1].center[1] += 1.0
        plotter.update(pause=0.1)

    plotter.show()
