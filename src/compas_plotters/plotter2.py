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
    """Definition of a plotter object based on matplotlib.

    Parameters
    ----------
    figsize : tuple, optional
        The size of the plot in inches (width, length). Default is ``(16.0, 12.0)``.

    Other Parameters
    ----------------
    dpi : float, optional
        The resolution of the plot.
        Default is ``100.0``.
    tight : bool, optional
        Produce a plot with limited padding between the plot and the edge of the figure.
        Default is ``True``.
    fontsize : int, optional
        The size of the font used in labels. Default is ``10``.
    axes : matplotlib.axes.Axes, optional
        An instance of ``matplotlib`` ``Axes``.
        For example to share the axes of a figure between different plotters.
        Default is ``None`` in which case the plotter will make its own axes.

    Attributes
    ----------
    defaults : dict
        Dictionary containing default attributes for vertices and edges.

        * point.radius      : ``0.1``
        * point.facecolor   : ``'#ffffff'``
        * point.edgecolor   : ``'#000000'``
        * point.edgewidth   : ``0.5``
        * point.textcolor   : ``'#000000'``
        * point.fontsize    : ``10``
        * line.width        : ``1.0``
        * line.color        : ``'#000000'``
        * line.textcolor    : ``'#000000'``
        * line.fontsize     : ``10``
        * polygon.facecolor : ``'#ffffff'``
        * polygon.edgecolor : ``'#000000'``
        * polygon.edgewidth : ``0.1``
        * polygon.textcolor : ``'#000000'``
        * polygon.fontsize  : ``10``

    Examples
    --------
    >>>

    """
    def __init__(self, figsize=(16.0, 12.0), tight=True, **kwargs):
        """Initialises a plotter object"""
        self._axes = None
        self.tight = tight
        self.figure_size = figsize
        self.figure_dpi = dpi
        self.figure_bgcolor = '#ffffff'
        self.axes_xlabel = None
        self.axes_ylabel = None

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
                ylabel=self.axes_ylabel
            )

        return self._axes

    @axes.setter
    def axes(self, axes):
        self._axes = axes

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



# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
