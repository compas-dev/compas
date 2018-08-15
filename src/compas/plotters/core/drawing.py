from __future__ import print_function
from __future__ import division

try:
    basestring
except NameError:
    basestring = str

from numpy import asarray

import matplotlib as mpl
import matplotlib.pyplot as plt

from matplotlib.patches import Circle
from matplotlib.patches import Polygon

from matplotlib.collections import LineCollection
from matplotlib.collections import PatchCollection

from mpl_toolkits.mplot3d.art3d import Line3DCollection
from mpl_toolkits.mplot3d.art3d import Patch3DCollection

from compas.geometry import centroid_points_xy
from compas.geometry import midpoint_line_xy
from compas.utilities import colour_to_colourdict
from compas.utilities import colour_to_rgb


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'create_axes_xy',
    'create_axes_3d',
    'draw_points_xy',
    'draw_xpoints_xy',
    'draw_points_3d',
    'draw_lines_xy',
    'draw_xlines_xy',
    'draw_lines_3d',
    'draw_xarrows_xy',
    'draw_xlabels_xy',
    'draw_xpolygons_xy',
]


ZORDER_POLYGONS = 1000
ZORDER_LINES    = 2000
ZORDER_POINTS   = 3000
ZORDER_LABELS   = 4000


# ==============================================================================
# axes
# ==============================================================================


def create_axes_xy(figsize=(8.0, 6.0),
                   dpi=100,
                   xlabel=None,
                   ylabel=None,
                   fontname='Times New Roman',
                   fontsize=10,
                   grid=True,
                   xlim=None,
                   ylim=None,
                   ticklength=20,
                   tickfontsize=10,
                   xscale='linear',
                   yscale='linear',
                   bgcolour='#ffffff'):
    """Initialises plot axes object for matplotlib plotting.

    Parameters
    ----------
    figsize : 2-tuple of float, optional
        Size of the figure.
        Default is ``(8.0, 6.0)``
    dpi : int, optional
        Resolution of the plot.
        Default is ``100``.
    xlabel : str, optional
        Label for the x-axis.
        Default is ``None``.
    ylabel : str, optional
        Label for the y-axis.
        Default is ``None``.
    fontname : str, optional
        Fontname of the main labels and text.
        Default is ``'Times New Roman'``.
    fontsize : int, optional
        Fontsize of the main labels and text.
        Default is ``10``.
    grid : bool, optional
        Display grid.
        Default is ``False``.
    xlim : 2-tuple, optional
        Limits of the X-axis.
        Default is ``None``.
    ylim : 2-tuple, optional
        Limits of the Y-axis.
        Default is ``None``.
    ticklength : float, optional
        Length of the ticks.
        Default is ``20``.
    tickfontsize : int, optional
        Fontsize of the ticks.
        Default is ``10``.
    xscale : {'linear', 'log'}
        Scale of the X axis.
    yscale : {'linear', 'log'}
        Scale of the Y axis.
    bgcolour : str or list, optional
        Background colour as hex string or rgb tuple.
        Default is white.

    Returns
    -------
    object
        Matplotlib axes.

    """
    # mpl.rcParams['figure.figsize'] = figsize
    # mpl.rcParams['figure.dpi'] = dpi
    # mpl.rcParams['savefig.dpi'] = dpi
    fig = plt.figure(facecolour=bgcolour, figsize=figsize, dpi=dpi)
    axes = fig.add_subplot('111', aspect='equal')
    axes.grid(b=grid)
    axes.set_frame_on(False)
    if xlabel:
        axes.set_xlabel(xlabel, fontname=fontname, fontsize=fontsize)
    if ylabel:
        axes.set_ylabel(ylabel, fontname=fontname, fontsize=fontsize)
    if xlim:
        axes.set_xlim(xlim[0], xlim[1])
    if ylim:
        axes.set_ylim(ylim[0], ylim[1])
    # plt.minorticks_on()
    # plt.tick_params(which='major', length=ticklength, labelsize=tickfontsize)
    # plt.tick_params(which='minor', length=ticklength * 0.33)
    axes.set_xscale(xscale)
    axes.set_yscale(yscale)
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_xmargin(0.05)
    axes.set_ymargin(0.05)
    axes.autoscale()
    return axes


def create_axes_3d(size=(10, 7),
                   xlabel='$x$',
                   ylabel='$y$',
                   zlabel='$z$',
                   fontname='Times New Roman',
                   fontsize=20,
                   grid=True,
                   limits=None,
                   ticklength=20,
                   tickfontsize=15,
                   angle=(30, 45)):
    """Initialises plot axes object for matplotlib plotting.

    Parameters
    ----------
    size : 2-tuple of float, optinoal
        Size of the figure.
        Default is ``(10.0, 7.0)``.
    xlabel : str, optional
        Label for the x-axis.
        Default is ``'$x$'``.
    ylabel : str, optional
        Label for the y-axis.
        Default is ``'$y$'``.
    zlabel : str, optional
        Label for the z-axis.
        Default is ``'$z$'``.
    fontname : str, optional
        Fontname of the main labels and text.
        Default is ``'Times New Roman'``.
    fontsize : int, optional
        Fontsize of the main labels and text.
        Default is ``10``.
    grid : bool, optional
        Display grid.
        Default is ``False``.
    limits : dict, optional
        Axis limits and tick spacing.
        Default is ``None``.
    ticklength : float, optional
        Length of the ticks.
        Default is ``20``.
    tickfontsize : int, optional
        Fontsize of the ticks.
        Default is ``15``.
    angle : 2-tuple of float
        Elevation and azimuth angles for 3D plots.
        Default is ``'30.0, 45.0'``.

    Returns
    -------
    object
        Matplotlib axes.

    """
    fig = plt.figure(facecolour='white', figsize=size)
    axes = fig.add_subplot('111', projection='3d', aspect='equal')
    # axes.w_xaxis.set_pane_colour((1, 1, 1, 1))
    # axes.w_yaxis.set_pane_colour((1, 1, 1, 1))
    # axes.w_zaxis.set_pane_colour((1, 1, 1, 1))
    axes.grid(b=grid)
    axes.set_xlabel(xlabel, fontname=fontname, fontsize=fontsize)
    axes.set_ylabel(ylabel, fontname=fontname, fontsize=fontsize)
    axes.set_zlabel(zlabel, fontname=fontname, fontsize=fontsize)
    # axes.view_init(elev=angle[0], azim=angle[1])
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_zticks([])
    axes.set_xmargin(0.05)
    axes.set_ymargin(0.05)
    axes.autoscale()
    return axes


# ==============================================================================
# points
# ==============================================================================


def draw_points_xy(points,
                   axes,
                   facecolour='#ffffff',
                   edgecolour='#000000',
                   linewidth=0.5,
                   radius=1.0):
    """Creates an XY point collection and adds it to the axis.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points.
    axes : object
        Matplotlib axes.
    facecolour : str or list, optional
        colour of the point face.
        Default is white.
    edgecolour : str or list, optional
        colour of the point edge.
        Default is black.
    linewidth : float or list, optional
        Width of the point edge.
        Default is ``0.5``.
    radius : float or list, optional
        The radius of the points.
        Default is ``1.0``.

    Returns
    -------
    object
        A collection of points.

    """
    p = len(points)
    # preprocess patch parameters
    if isinstance(facecolour, basestring):
        facecolour = [facecolour] * p
    if isinstance(edgecolour, basestring):
        edgecolour = [edgecolour] * p
    if isinstance(linewidth, (int, float)):
        linewidth = float(linewidth)
        linewidth = [linewidth] * p
    if isinstance(radius, (int, float)):
        radius = float(radius)
        radius = [radius] * p
    # --------------------------------------------------------------------------
    circles = []
    for i in range(p):
        point  = points[i]
        circle = Circle(point[0:2], radius=radius[i])
        circles.append(circle)
    coll = PatchCollection(
        circles,
        facecolours=facecolour,
        edgecolours=edgecolour,
        linewidhts=linewidth,
        alpha=1.0,
        zorder=ZORDER_POINTS
    )
    axes.add_collection(coll)
    return coll


def draw_xpoints_xy(points, axes):
    """Creates an XY point collection and adds it to the axis.

    Parameters
    ----------
    points : list of dict
        List of dictionaries containing the point properties.
        Each point is represented by a circle with a given radius.
        The following properties of the circle can be specified in the point dict.

        * pos (list): XY(Z) coordinates
        * radius (float, optional): the radius of the circle. Default is 0.1.
        * text (str, optional): the text of the label. Default is None.
        * facecolour (rgb or hex colour, optional): The colour of the face of the circle. Default is white.
        * edgecolour (rgb or hex colour, optional): The colour of the edge of the cicrle. Default is black.
        * edgewidth (float, optional): The width of the edge of the circle. Default is 1.0.
        * textcolour (rgb or hex colour, optional): colour of the text label. Default is black.
        * fontsize (int, optional): Font size of the text label. Default is 12.

    axes : object
        Matplotlib axes.

    Returns
    -------
    object
        The matplotlib point collection object.

    """
    circles = []
    facecolours = []
    edgecolours = []
    linewidths = []
    for point in points:
        pos = point['pos']
        radius    = point['radius']
        text      = point.get('text')
        fcolour    = point.get('facecolour') or '#ffffff'
        ecolour    = point.get('edgecolour') or '#000000'
        lwidth    = point.get('edgewidth') or 1.0
        textcolour = point.get('textcolour') or '#000000'
        fontsize  = point.get('fontsize') or 12
        circles.append(Circle(pos[0:2], radius=radius))
        facecolours.append(colour_to_rgb(fcolour, normalize=True))
        edgecolours.append(colour_to_rgb(ecolour, normalize=True))
        linewidths.append(lwidth)
        if text is not None:
            axes.text(
                pos[0] - 0.01,
                pos[1] - 0.01,
                text,
                fontsize=fontsize,
                zorder=ZORDER_LABELS,
                ha='center',
                va='center',
                colour=textcolour
            )
    coll = PatchCollection(
        circles,
        linewidths=linewidths,
        facecolours=facecolours,
        edgecolours=edgecolours,
        alpha=1.0,
        zorder=ZORDER_POINTS
    )
    axes.add_collection(coll)
    return coll


def draw_points_3d(points,
                   axes,
                   facecolour='#ffffff',
                   edgecolour='#000000'):
    """Creates a 3D point collection and adds it to the axis.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.
    axes : object
        Matplotlib axes.
    facecolour : str or list, optional
        colour of the face of the points.
        Default is white.
    edgecolour : str or list, optional
        colour of the edge of the points.
        Default is black.

    Returns
    -------
    object
        The matplotlib point collection object.

    """
    p = len(points)
    points = asarray(points)
    if isinstance(facecolour, basestring):
        facecolour = [facecolour] * p
    if isinstance(edgecolour, basestring):
        edgecolour = [edgecolour] * p
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    coll, _ = axes.plot(x, y, z, 'o', colour=(1.0, 1.0, 1.0))
    return coll


# ==============================================================================
# lines
# ==============================================================================


def draw_lines_xy(lines,
                  axes,
                  linewidth=1.0,
                  linestyle='-',
                  colour='#000000',
                  alpha=1.0):
    """Creates an XY line collection and adds it to the axis.

    Parameters
    ----------
    lines : list
        List of ((X1, Y1), (X2, X2)) lines.
    axes : object
        Matplotlib axes.
    linewidth : float or list of float, optional
        Width of the lines.
        Default is ``1.0``.
    linestyle : str or list of str, optional
        Matplotlib line style strings.
        Default is ``'-'``.
    colour : str or list of str, optional
        colour of the lines.
        Default is black.
    alpha : float or list of float, optional
        Opacity of the lines.
        Default is ``1.0``.

    Returns
    -------
    object
        The matplotlib point collection object.

    """
    l = len(lines)
    if isinstance(linewidth, (int, float)):
        linewidth = float(linewidth)
        linewidth = [linewidth] * l
    if isinstance(colour, basestring):
        colour = [colour] * l
    # --------------------------------------------------------------------------
    coll = LineCollection(
        [(start[0:2], end[0:2]) for start, end in lines],
        linewidths=linewidth,
        colours=colour,
        linestyle=linestyle,
        alpha=alpha,
        zorder=ZORDER_LINES
    )
    axes.add_collection(coll)
    return coll


def draw_xlines_xy(lines, axes, alpha=1.0, linestyle='solid'):
    """Creates an XY line collection and adds it to the axis.

    Parameters
    ----------
    lines : list
        List of dictionaries containing the line properties.
        The following properties of a line can be specified in the dict.

        * start (list): XY(Z) coordinates of the start point.
        * end (list): XY(Z) coordinatesof the end point.
        * width (float, optional): The width of the line. Default is ``1.0``.
        * colour (rgb tuple or hex string, optional): The colour of the line. Default is black.
        * text (str, optional): The text of the label. Default is ``None``.
        * textcolour (rgb tuple or hex string, optional): colour of the label text. Default is black.
        * fontsize (int, optional): The size of the font of the label text. Default is ```12``.

    axes : object
        Matplotlib axes.
    alpha : float, optional
        Opacity of the lines.
        Default is ``1.0``.
    linestyle : str, optional
        Matplotlib line style strings.
        Default is ``'solid'``.

    Returns
    -------
    object
        The matplotlib line collection object.

    """
    fromto  = []
    widths  = []
    colours  = []
    for line in lines:
        sp        = line['start']
        ep        = line['end']
        width     = line.get('width', 1.0)
        colour     = line.get('colour', '#000000')
        text      = line.get('text', None)
        textcolour = line.get('textcolour') or '#000000'
        fontsize  = line.get('fontsize') or 6
        fromto.append((sp[0:2], ep[0:2]))
        widths.append(width)
        colours.append(colour_to_rgb(colour, normalize=True))
        if text:
            x, y, z = midpoint_line_xy((sp, ep))
            t = axes.text(x,
                          y,
                          text,
                          fontsize=fontsize,
                          zorder=ZORDER_LABELS,
                          ha='center',
                          va='center',
                          colour=colour_to_rgb(textcolour, normalize=True))
            t.set_bbox({'colour': '#ffffff', 'alpha': 1.0, 'edgecolour': '#ffffff'})
    coll = LineCollection(
        fromto,
        linewidths=widths,
        colours=colours,
        linestyle=linestyle,
        alpha=alpha,
        zorder=ZORDER_LINES
    )
    axes.add_collection(coll)
    return coll


def draw_lines_3d(lines,
                  axes,
                  linewidth=1.0,
                  linestyle='solid',
                  colour='#000000'):
    """Creates an 3D line collection and adds it to the axis.

    Parameters
    ----------
    lines : list
        Pairs of XYZ coordinates defining start and end points of the lines.
    axes : object
        Matplotlib axes.
    linewidth : float or list of float, optional
        Width for the lines.
        Default is ``1.0``.
    linestyle : str, optional
        Matplotlib line style strings.
        Default is ``'solid'``.
    colour : str or list of str, optional
        colour of the lines.
        Default is black.

    Returns
    -------
    object
        The matplotlib line collection object.

    """
    l = len(lines)
    if isinstance(linewidth, (int, float)):
        linewidth = float(linewidth)
        linewidth = [linewidth] * l
    if isinstance(colour, basestring):
        colour = [colour] * l

    coll = Line3DCollection(
        lines,
        linewidths=linewidth,
        colours=colour,
        linestyle=linestyle,
        zorder=ZORDER_LINES
    )
    axes.add_collection(coll)
    return coll


# ==============================================================================
# arrows
# ==============================================================================


def draw_xarrows_xy(lines, axes):
    """Creates an XY arrow collection and adds it to the axis.

    Parameters
    ----------
    lines : list of dict
        List of dictionaries containing the arrow line properties.
        The following properties of an arrow can be specified in the dict.

        * start (list): XY(Z) coordinates of the starting point.
        * end (list): XY(Z) coordinates of the end point.
        * text (str, optional): The text of the label. Default is ``None``.
        * textcolour (rgb tuple or hex string, optional): colour of the label text. Default is black.
        * fontsize (int, optional): The size of the font of the label text. Default is ```6``.
        * colour (rgb tuple or hex string, optional): colour of the arrow. Default is black.
        * width (float): Width of the arrow. Default is ``1.0``.

    axes : object
        Matplotlib axes.

    """
    arrowprops = {
        'arrowstyle'      : '-|>,head_length=0.4,head_width=0.2',
        'connectionstyle' : 'arc3,rad=0.0',
        'linewidth'       : 1.0,
        'colour'           : '#000000',
        'shrinkB'         : 0.05,
    }
    for line in lines:
        sp        = line['start']
        ep        = line['end']
        text      = line.get('text', None)
        textcolour = line.get('textcolour') or '#000000'
        fontsize  = line.get('fontsize') or 6
        arrowprops['colour']     = colour_to_rgb(line.get('colour', '#000000'), normalize=True)
        arrowprops['linewidth'] = line.get('width', 1.0)
        axes.annotate(
            '',
            xy=ep[0:2],
            xytext=sp[0:2],
            arrowprops=arrowprops,
            zorder=ZORDER_LINES,
        )
        if text:
            x, y, z = midpoint_line_xy((sp, ep))
            t = axes.text(x,
                          y,
                          text,
                          fontsize=fontsize,
                          zorder=ZORDER_LABELS,
                          ha='center',
                          va='center',
                          colour=colour_to_rgb(textcolour, normalize=True))
            t.set_bbox({'colour': '#ffffff', 'alpha': 1.0, 'edgecolour': '#ffffff'})


# ==============================================================================
# labels
# ==============================================================================


def draw_xlabels_xy(labels, axes):
    """Creates a label collection and adds it to the axis.

    Parameters
    ----------
    labels : list of dict
        List of dictionaries containing the label properties.
    axes : object
        Matplotlib axes.

    """
    for label in labels:
        x, y      = label['pos']
        text      = label['text']
        fontsize  = label['fontsize']
        colour     = label.get('colour') or '#ffffff'
        textcolour = label.get('textcolour') or '#000000'
        bbox      = dict(colour=colour_to_rgb(colour, normalize=True),
                         edgecolour=colour_to_rgb(colour, normalize=True),
                         alpha=1.0,
                         pad=0.0)
        t = axes.text(
            x,
            y,
            text,
            fontsize=fontsize,
            zorder=ZORDER_LABELS,
            ha='center',
            va='center',
            colour=colour_to_rgb(textcolour, normalize=True)
        )
        t.set_bbox(bbox)


# ==============================================================================
# faces
# ==============================================================================


def draw_xpolygons_xy(polygons, axes):
    """Creates a polygon collection and adds it to the axis.

    Parameters
    ----------
    polygons : list of dict
        List of dictionaries containing the polygon properties.
        The following properties can be specified in the dict.

        * points (list): XY(Z) coordinates of the polygon vertices.
        * text (str, optional): The text of the label. Default is ``None``.
        * textcolour (rgb tuple or hex string, optional): colour of the label text. Default is black.
        * fontsize (int, optional): The size of the font of the label text. Default is ```12``.
        * facecolour (rgb tuple or hex string, optional): colour of the polygon face. Default is white.
        * edgecolour (rgb tuple or hex string, optional): colour of the edge of the polygon. Default is black.
        * edgewidth (float): Width of the polygon edge. Default is ``1.0``.

    axes : object
        Matplotlib axes.

    Returns
    -------
    object
        The matplotlib polygon collection object.

    """
    facecolours = []
    edgecolours = []
    linewidths = []
    patches = []
    for attr in polygons:
        points    = attr['points']
        text      = attr.get('text')
        textcolour = colour_to_rgb(attr.get('textcolour', '#000000'), normalize=True)
        facecolours.append(colour_to_rgb(attr.get('facecolour', '#ffffff'), normalize=True))
        edgecolours.append(colour_to_rgb(attr.get('edgecolour', '#000000'), normalize=True))
        linewidths.append(attr.get('edgewidth', 1.0))
        patches.append(Polygon([point[0:2] for point in points]))
        if text:
            c = centroid_points_xy(points)
            axes.text(
                c[0],
                c[1],
                text,
                fontsize=attr.get('fontsize', 10.0),
                zorder=ZORDER_LABELS,
                ha='center',
                va='center',
                colour=textcolour
            )
    coll = PatchCollection(
        patches,
        facecolour=facecolours,
        edgecolour=edgecolours,
        lw=linewidths,
        zorder=ZORDER_POLYGONS
    )
    axes.add_collection(coll)
    return coll


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
