""""""
import matplotlib
# matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

from matplotlib.patches import Circle

from compas.plotters.core.drawing import create_axes_xy
from compas.plotters.core.drawing import draw_xpoints_xy
from compas.plotters.core.drawing import draw_xlines_xy
from compas.plotters.core.drawing import draw_xpolygons_xy
from compas.plotters.core.drawing import draw_xarrows_xy


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['Plotter', ]


# https://matplotlib.org/faq/usage_faq.html#what-is-interactive-mode
# https://matplotlib.org/api/pyplot_summary.html
# https://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure
# https://matplotlib.org/api/axes_api.html
# https://matplotlib.org/api/index.html


class Plotter(object):
    """Definition of a plotter object based on matplotlib.

    Parameters
    ----------
    figsize : tuple, optional [16.0, 12.0]
        The size of the plot in inches (width, length).
    dpi : float, optional [100.0]
        The resolution of the plot.

    Attributes
    ----------
    figure_size : tuple
        The size of the plot in inches (width, length).
    figure_dpi : float
        The resolution of the plot.
    figure_bgcolor : str, tuple, dict
        The color specififcation for the figure background.
        Colors should be specified in the form of a string (hex colors) or
        as a tuple of RGB components.
    axes_xlabel : str
        The label on the X axis of the plot.
    axes_ylabel : str
        The label on the Y axis of the plot.
    defaults : dict
        Dictionary containing default attributes for points, edges, lines, text
        and polygons.


    References
    ----------
    * Hunter, J. D., 2007. Matplotlib: A 2D graphics environment. Computing In Science & Engineering (9) 3, p.90-95.
      Available at: http://ieeexplore.ieee.org/document/4160265/citations

    """
    def __init__(self, figsize=(16.0, 12.0), dpi=100.0, interactive=False, tight=False, **kwargs):
        """Initialises a plotter object"""
        self._interactive = False
        self._axes = None
        # use descriptors for these
        # to help the user set these attributes in the right format
        # figure attributes
        self.figure_size = figsize
        self.figure_dpi = dpi
        self.figure_bgcolor = '#ffffff'
        # axes attributes
        self.axes_xlabel = None
        self.axes_ylabel = None
        # drawing defaults
        # z-order
        # color
        # size/thickness
        self.defaults = {
            'point.radius'    : 0.15,
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
        self.interactive = interactive
        self.tight = tight

    @property
    def interactive(self):
        """Returns a boolean describing of the plot is interactive.

        Returns
        -------
        bool
            True if plot is interactive.
        """
        return self._interactive

    @interactive.setter
    def interactive(self, value):
        """Sets the interactive plot on or off.

        Parameters
        ----------
        value : bool
            Interactive plot on or off.

        """
        self._interactive = value
        # interactive mode seems to be intended for other things
        # see: https://matplotlib.org/faq/usage_faq.html#what-is-interactive-mode
        # if value:
        #     plt.ion()
        # else:
        #     plt.ioff()

    @property
    def axes(self):
        """Returns the axes subplot matplotlib object.

        Returns
        -------
        object
            The matplotlib axes object.

        """
        if self._axes is None:
            # customise the use of this function
            # using attributes of the plotter class
            self._axes = create_axes_xy(
                figsize=self.figure_size,
                dpi=self.figure_dpi,
                xlabel=self.axes_xlabel,
                ylabel=self.axes_ylabel
            )

        return self._axes

    @property
    def figure(self):
        """Returns the matplotlib figure instance.

        Returns
        -------
        object
            The matplotlib figure instance.
        """
        return self.axes.get_figure()

    @property
    def canvas(self):
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
            as a tuple of RGB components.

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
        """"""
        self.figure.canvas.mpl_connect('pick_event', listener)

    def clear_collection(self, collection):
        """Clears a matplotlib collection object.

        Parameters
        ----------
        collection : object
            The matplotlib collection object.

        """
        collection.remove()

    def show(self):
        """Displays the plot."""
        self.axes.autoscale()
        if self.tight:
            plt.tight_layout()
        plt.show()

    # def top(self):
    #     self.figure.canvas.manager.show()

    def save(self, filepath, **kwargs):
        """Saves the plot on a file.

        Parameters
        ----------
        filepath : str
            Full path of the file.

        """
        self.axes.autoscale()
        plt.savefig(filepath, **kwargs)

    # def init_gif(self, filepath, **kwargs):
    #     """Saves the plot on a file.

    #     Parameters
    #     ----------
    #     filepath : str
    #         Full path of the file.

    #     """
    #     self.axes.autoscale()
    #     plt.savefig(filepath, **kwargs)

    # def save_gifimage(self):
    #     pass

    def update(self, pause=0.0001):
        """Updates and pauses the plot.

        Parameters
        ----------
        pause : float
            Ammount of time to pause the plot in seconds.
        """
        self.axes.autoscale()
        # self.figure.canvas.draw_idle()
        plt.pause(pause)

    def update_pointcollection(self, collection, centers, radius=1.0):
        """Updates the location and radii of a point collection.

        Parameters
        ----------
        collection : object
            The point collection to update.
        centers : list
            List of tuples or lists with XY location for the points in the collection.
        radius : float, list
            The radii of the points. If a floar is given it will be used for all points.

        """
        try:
            len(radius)
        except Exception:
            radius = [radius] * len(centers)
        data = zip(centers, radius)
        circles = [Circle(c, r) for c, r in data]
        collection.set_paths(circles)

    def update_linecollection(self, collection, segments):
        """Updates a line collection.

        Parameters
        ----------
        collection : object
            The line collection to update.
        segments : list
            List of tuples or lists with XY location for the start and end
            points in each line in the collection.
        """
        collection.set_segments(segments)

    def update_polygoncollection(self, collection, polygons):
        pass

    def draw_points(self, points):
        """Draws points on a 2D plot.

        Parameters
        ----------

        points : list
            List of dictionaries containing the point properties.

        Returns
        -------
        object
            The matplotlib point collection object.
        """
        return draw_xpoints_xy(points, self.axes)

    def draw_lines(self, lines):
        """Draws lines on a 2D plot.

        Parameters
        ----------
        lines : list
            List of dictionaries containing the line properties.

        Returns
        -------
        object
            The matplotlib line collection object.
        """
        return draw_xlines_xy(lines, self.axes)

    def draw_polygons(self, polygons):
        """Draws polygons on a 2D plot.

        Parameters
        ----------
        polygons : list
            List of dictionaries containing the polygon properties.

        Returns
        -------
        object
            The matplotlib polygon collection object.
        """
        return draw_xpolygons_xy(polygons, self.axes)

    def draw_arrows(self, arrows):
        """Draws arrows on a 2D plot.

        Parameters
        ----------
        arrows : list
            List of dictionaries containing the arrow properties.

        Returns
        -------
        object
            The matplotlib arrow collection object.
        """
        return draw_xarrows_xy(arrows, self.axes)


# ==============================================================================
# Debugging
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
            'pos': mesh.vertex_coordinates(key, 'xy'),
            'radius': 0.1,
            'facecolor': '#ff0000' if mesh.vertex_degree(key) == 2 else '#ffffff'
        })

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end': mesh.vertex_coordinates(v, 'xy'),
            'width': 1.0
        })


    plotter = Plotter(figsize=(10, 6))

    pcoll = plotter.draw_points(points)
    lcoll = plotter.draw_lines(lines)


    def callback(vertices, k, args):
        pos = [vertices[key][0:2] for key in mesh.vertex]
        plotter.update_pointcollection(pcoll, pos, 0.1)

        segments = []
        for u, v in mesh.edges():
            a = vertices[u][0:2]
            b = vertices[v][0:2]
            segments.append([a, b])

        plotter.update_linecollection(lcoll, segments)
        plotter.update(pause=0.001)


    vertices = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
    adjacency = {key: mesh.vertex_neighbours(key) for key in mesh.vertices()}


    smooth_centroid(vertices,
                    adjacency,
                    fixed=fixed,
                    kmax=100,
                    callback=callback)


    plotter.show()
