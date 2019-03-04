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

from compas.plotters.core.drawing import create_axes_xy
from compas.plotters.core.drawing import draw_xpoints_xy
from compas.plotters.core.drawing import draw_xlines_xy
from compas.plotters.core.drawing import draw_xpolylines_xy
from compas.plotters.core.drawing import draw_xpolygons_xy
from compas.plotters.core.drawing import draw_xarrows_xy


__all__ = ['Plotter']


class Plotter(object):
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

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Hunter, J. D., 2007. *Matplotlib: A 2D graphics environment*.
           Computing In Science & Engineering (9) 3, p.90-95.
           Available at: http://ieeexplore.ieee.org/document/4160265/citations.

    Examples
    --------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.plotters import Plotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        plotter = Plotter(figsize=(10, 7))

        points = []
        for key in mesh.vertices():
            points.append({
                'pos'      : mesh.vertex_coordinates(key),
                'radius'   : 0.1,
                'facecolor': '#ffffff'
            })

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u),
                'end'  : mesh.vertex_coordinates(v),
                'width': 1.0
            })

        plotter.draw_points(points)
        plotter.draw_lines(lines)
        plotter.show()

    """
    def __init__(self, figsize=(16.0, 12.0), dpi=100.0, tight=True, axes=None, **kwargs):
        """Initialises a plotter object"""
        self._axes = None
        self.axes = axes
        self.tight = tight
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

    def clear_collection(self, collection):
        """Clears a matplotlib collection object.

        Parameters
        ----------
        collection : object
            The matplotlib collection object.

        Notes
        -----
        For more info, see [1]_ and [2]_.

        References
        ----------
        .. [1] https://matplotlib.org/2.0.2/api/collections_api.html
        .. [2] https://matplotlib.org/2.0.2/api/collections_api.html#matplotlib.collections.Collection.remove

        """
        collection.remove()

    def show(self, autoscale=True):
        """Displays the plot.

        """
        self.axes.autoscale()
        if self.tight:
            plt.tight_layout()
        plt.show()

    def top(self):
        """Bring the plotting window to the top.

        Warning
        -------
        This seems to work only for some back-ends.

        Notes
        -----
        For more info, see this SO post [1]_.

        References
        ----------
        .. [1] https://stackoverflow.com/questions/20025077/how-do-i-display-a-matplotlib-figure-window-on-top-of-all-other-windows-in-spyde

        """
        self.figure.canvas.manager.show()

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

    @contextmanager
    def gifified(self, func, tempfolder, outfile, pattern='image_{}.png'):
        """Create a context for making animated gifs using a callback for updating the plot.

        Parameters
        ----------
        func : callable
            The callback function used to update the plot.
        tempfolder : str
            The path to a folder for storing temporary image frames.
        outfile : str
            Path to the file where the resultshould be saved.
        pattern : str, optional
            Pattern for the filename of the intermediate frames.
            The pattern should contain a replacement placeholder for the number
            of the frame. Default is ``'image_{}.png'``.

        Examples
        --------
        .. code-block:: python

            #

        """
        images = []

        def gifify(f):
            def wrapper(*args, **kwargs):
                f(*args, **kwargs)
                image = os.path.join(tempfolder, pattern.format(len(images)))
                images.append(image)
                self.save(image)
            return wrapper

        if not os.path.exists(tempfolder) or not os.path.isdir(tempfolder):
            os.makedirs(tempfolder)

        for file in os.listdir(tempfolder):
            filepath = os.path.join(tempfolder, file)
            try:
                if os.path.isfile(filepath):
                    os.remove(filepath)
            except Exception as e:
                print(e)

        image = os.path.join(tempfolder, pattern.format(len(images)))
        images.append(image)
        self.save(image)
        #
        yield gifify(func)
        #
        self.save_gif(outfile, images)
        shutil.rmtree(tempfolder)
        print('done gififying!')

    def save_gif(self, filepath, images, delay=10, loop=0):
        """Save a series of images as an animated gif.

        Parameters
        ----------
        filepath : str
            The full path to the output file.
        images : list
            A list of paths to input files.
        delay : int, optional
            The delay between frames in milliseconds. Default is ``10``.
        loop : int, optional
            The number of loops. Default is ``0``.

        Returns
        -------
        None

        Warning
        -------
        This function assumes ImageMagick is installed on your system, and on
        *convert* being on your system path.

        Examples
        --------
        .. code-block:: python

            #

        """
        command = ['convert', '-delay', '{}'.format(delay), '-loop', '{}'.format(loop), '-layers', 'optimize']
        subprocess.call(command + images + [filepath])

    def draw_points(self, points):
        """Draws points on a 2D plot.

        Parameters
        ----------

        points : list of dict
            List of dictionaries containing the point properties.
            Each point is represented by a circle with a given radius.
            The following properties of the circle can be specified in the point dict.

            * pos (list): XY(Z) coordinates
            * radius (float, optional): the radius of the circle. Default is 0.1.
            * text (str, optional): the text of the label. Default is None.
            * facecolor (rgb or hex color, optional): The color of the face of the circle. Default is white.
            * edgecolor (rgb or hex color, optional): The color of the edge of the cicrle. Default is black.
            * edgewidth (float, optional): The width of the edge of the circle. Default is 1.0.
            * textcolor (rgb or hex color, optional): Color of the text label. Default is black.
            * fontsize (int, optional): Font size of the text label. Default is 12.

        Returns
        -------
        object
            The matplotlib point collection object.

        Notes
        -----
        ...

        See Also
        --------
        :func:`compas.plotters.core.draw_xpoints_xy`

        Examples
        --------
        >>>

        """
        return draw_xpoints_xy(points, self.axes)

    def draw_lines(self, lines):
        """Draws lines on a 2D plot.

        Parameters
        ----------
        lines : list of dict
            List of dictionaries containing the line properties.
            The following properties of a line can be specified in the dict.

            * start (list): XY(Z) coordinates of the start point.
            * end (list): XY(Z) coordinatesof the end point.
            * width (float, optional): The width of the line. Default is ``1.0``.
            * color (rgb tuple or hex string, optional): The color of the line. Default is black.
            * text (str, optional): The text of the label. Default is ``None``.
            * textcolor (rgb tuple or hex string, optional): Color of the label text. Default is black.
            * fontsize (int, optional): The size of the font of the label text. Default is ```12``.

        Returns
        -------
        object
            The matplotlib line collection object.

        See Also
        --------
        :func:`compas.plotters.core.draw_xlines_xy`

        """
        return draw_xlines_xy(lines, self.axes)

    def draw_polylines(self, polylines):
        """Draw polylines on a 2D plot.

        Parameters
        ----------
        polylines : list of dict
            A list of dictionaries containing the polyline properties.
            The following properties are supported:

            * points (list): XY(Z) coordinates of the polygon vertices.
            * text (str, optional): The text of the label. Default is ``None``.
            * textcolor (rgb tuple or hex string, optional): Color of the label text. Default is black.
            * fontsize (int, optional): The size of the font of the label text. Default is ```12``.
            * facecolor (rgb tuple or hex string, optional): Color of the polygon face. Default is white.
            * edgecolor (rgb tuple or hex string, optional): Color of the edge of the polygon. Default is black.
            * edgewidth (float): Width of the polygon edge. Default is ``1.0``.

        Returns
        -------
        object
            The matplotlib polyline collection object.

        """
        return draw_xpolylines_xy(polylines, self.axes)

    def draw_polygons(self, polygons):
        """Draws polygons on a 2D plot.

        Parameters
        ----------
        polygons : list of dict
            List of dictionaries containing the polygon properties.
            The following properties can be specified in the dict.

            * points (list): XY(Z) coordinates of the polygon vertices.
            * text (str, optional): The text of the label. Default is ``None``.
            * textcolor (rgb tuple or hex string, optional): Color of the label text. Default is black.
            * fontsize (int, optional): The size of the font of the label text. Default is ```12``.
            * facecolor (rgb tuple or hex string, optional): Color of the polygon face. Default is white.
            * edgecolor (rgb tuple or hex string, optional): Color of the edge of the polygon. Default is black.
            * edgewidth (float): Width of the polygon edge. Default is ``1.0``.

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
        arrows : list of dict
            List of dictionaries containing the arrow properties.
            The following properties of an arrow can be specified in the dict.

            * start (list): XY(Z) coordinates of the starting point.
            * end (list): XY(Z) coordinates of the end point.
            * text (str, optional): The text of the label. Default is ``None``.
            * textcolor (rgb tuple or hex string, optional): Color of the label text. Default is black.
            * fontsize (int, optional): The size of the font of the label text. Default is ```6``.
            * color (rgb tuple or hex string, optional): Color of the arrow. Default is black.
            * width (float): Width of the arrow. Default is ``1.0``.

        Returns
        -------
        object
            The matplotlib arrow collection object.

        See Also
        --------
        :func:`compas.plotters.core.draw_xarrows_xy`

        """
        return draw_xarrows_xy(arrows, self.axes)

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
