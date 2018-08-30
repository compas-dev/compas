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
from compas.utilities import color_to_colordict
from compas.utilities import color_to_rgb


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
                   bgcolor='#ffffff'):
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
    bgcolor : str or list, optional
        Background color as hex string or rgb tuple.
        Default is white.

    Returns
    -------
    object
        Matplotlib axes.

    """
    # mpl.rcParams['figure.figsize'] = figsize
    # mpl.rcParams['figure.dpi'] = dpi
    # mpl.rcParams['savefig.dpi'] = dpi
    fig = plt.figure(facecolor=bgcolor, figsize=figsize, dpi=dpi)
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
    fig = plt.figure(facecolor='white', figsize=size)
    axes = fig.add_subplot('111', projection='3d', aspect='equal')
    # axes.w_xaxis.set_pane_color((1, 1, 1, 1))
    # axes.w_yaxis.set_pane_color((1, 1, 1, 1))
    # axes.w_zaxis.set_pane_color((1, 1, 1, 1))
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
                   facecolor='#ffffff',
                   edgecolor='#000000',
                   linewidth=0.5,
                   radius=1.0):
    """Creates an XY point collection and adds it to the axis.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points.
    axes : object
        Matplotlib axes.
    facecolor : str or list, optional
        Color of the point face.
        Default is white.
    edgecolor : str or list, optional
        Color of the point edge.
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
    if isinstance(facecolor, basestring):
        facecolor = [facecolor] * p
    if isinstance(edgecolor, basestring):
        edgecolor = [edgecolor] * p
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
        facecolors=facecolor,
        edgecolors=edgecolor,
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
        * facecolor (rgb or hex color, optional): The color of the face of the circle. Default is white.
        * edgecolor (rgb or hex color, optional): The color of the edge of the cicrle. Default is black.
        * edgewidth (float, optional): The width of the edge of the circle. Default is 1.0.
        * textcolor (rgb or hex color, optional): Color of the text label. Default is black.
        * fontsize (int, optional): Font size of the text label. Default is 12.

    axes : object
        Matplotlib axes.

    Returns
    -------
    object
        The matplotlib point collection object.

    """
    circles = []
    facecolors = []
    edgecolors = []
    linewidths = []
    for point in points:
        pos = point['pos']
        radius    = point['radius']
        text      = point.get('text')
        fcolor    = point.get('facecolor') or '#ffffff'
        ecolor    = point.get('edgecolor') or '#000000'
        lwidth    = point.get('edgewidth') or 1.0
        textcolor = point.get('textcolor') or '#000000'
        fontsize  = point.get('fontsize') or 12
        circles.append(Circle(pos[0:2], radius=radius))
        facecolors.append(color_to_rgb(fcolor, normalize=True))
        edgecolors.append(color_to_rgb(ecolor, normalize=True))
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
                color=textcolor
            )
    coll = PatchCollection(
        circles,
        linewidths=linewidths,
        facecolors=facecolors,
        edgecolors=edgecolors,
        alpha=1.0,
        zorder=ZORDER_POINTS
    )
    axes.add_collection(coll)
    return coll


def draw_points_3d(points,
                   axes,
                   facecolor='#ffffff',
                   edgecolor='#000000'):
    """Creates a 3D point collection and adds it to the axis.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.
    axes : object
        Matplotlib axes.
    facecolor : str or list, optional
        Color of the face of the points.
        Default is white.
    edgecolor : str or list, optional
        Color of the edge of the points.
        Default is black.

    Returns
    -------
    object
        The matplotlib point collection object.

    """
    p = len(points)
    points = asarray(points)
    if isinstance(facecolor, basestring):
        facecolor = [facecolor] * p
    if isinstance(edgecolor, basestring):
        edgecolor = [edgecolor] * p
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    coll, _ = axes.plot(x, y, z, 'o', color=(1.0, 1.0, 1.0))
    return coll


# ==============================================================================
# lines
# ==============================================================================


def draw_lines_xy(lines,
                  axes,
                  linewidth=1.0,
                  linestyle='-',
                  color='#000000',
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
    color : str or list of str, optional
        Color of the lines.
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
    if isinstance(color, basestring):
        color = [color] * l
    # --------------------------------------------------------------------------
    coll = LineCollection(
        [(start[0:2], end[0:2]) for start, end in lines],
        linewidths=linewidth,
        colors=color,
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
        * color (rgb tuple or hex string, optional): The color of the line. Default is black.
        * text (str, optional): The text of the label. Default is ``None``.
        * textcolor (rgb tuple or hex string, optional): Color of the label text. Default is black.
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
    colors  = []
    for line in lines:
        sp        = line['start']
        ep        = line['end']
        width     = line.get('width', 1.0)
        color     = line.get('color', '#000000')
        text      = line.get('text', None)
        textcolor = line.get('textcolor') or '#000000'
        fontsize  = line.get('fontsize') or 6
        fromto.append((sp[0:2], ep[0:2]))
        widths.append(width)
        colors.append(color_to_rgb(color, normalize=True))
        if text:
            x, y, z = midpoint_line_xy((sp, ep))
            t = axes.text(x,
                          y,
                          text,
                          fontsize=fontsize,
                          zorder=ZORDER_LABELS,
                          ha='center',
                          va='center',
                          color=color_to_rgb(textcolor, normalize=True))
            t.set_bbox({'color': '#ffffff', 'alpha': 1.0, 'edgecolor': '#ffffff'})
    coll = LineCollection(
        fromto,
        linewidths=widths,
        colors=colors,
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
                  color='#000000'):
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
    color : str or list of str, optional
        Color of the lines.
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
    if isinstance(color, basestring):
        color = [color] * l

    coll = Line3DCollection(
        lines,
        linewidths=linewidth,
        colors=color,
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
        * textcolor (rgb tuple or hex string, optional): Color of the label text. Default is black.
        * fontsize (int, optional): The size of the font of the label text. Default is ```6``.
        * color (rgb tuple or hex string, optional): Color of the arrow. Default is black.
        * width (float): Width of the arrow. Default is ``1.0``.

    axes : object
        Matplotlib axes.

    """
    arrowprops = {
        'arrowstyle'      : '-|>,head_length=0.4,head_width=0.2',
        'connectionstyle' : 'arc3,rad=0.0',
        'linewidth'       : 1.0,
        'color'           : '#000000',
        'shrinkB'         : 0.05,
    }
    for line in lines:
        sp        = line['start']
        ep        = line['end']
        text      = line.get('text', None)
        textcolor = line.get('textcolor') or '#000000'
        fontsize  = line.get('fontsize') or 6
        arrowprops['color']     = color_to_rgb(line.get('color', '#000000'), normalize=True)
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
                          color=color_to_rgb(textcolor, normalize=True))
            t.set_bbox({'color': '#ffffff', 'alpha': 1.0, 'edgecolor': '#ffffff'})


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
        color     = label.get('color') or '#ffffff'
        textcolor = label.get('textcolor') or '#000000'
        bbox      = dict(color=color_to_rgb(color, normalize=True),
                         edgecolor=color_to_rgb(color, normalize=True),
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
            color=color_to_rgb(textcolor, normalize=True)
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
        * textcolor (rgb tuple or hex string, optional): Color of the label text. Default is black.
        * fontsize (int, optional): The size of the font of the label text. Default is ```12``.
        * facecolor (rgb tuple or hex string, optional): Color of the polygon face. Default is white.
        * edgecolor (rgb tuple or hex string, optional): Color of the edge of the polygon. Default is black.
        * edgewidth (float): Width of the polygon edge. Default is ``1.0``.

    axes : object
        Matplotlib axes.

    Returns
    -------
    object
        The matplotlib polygon collection object.

    """
    facecolors = []
    edgecolors = []
    linewidths = []
    patches = []
    for attr in polygons:
        points    = attr['points']
        text      = attr.get('text')
        textcolor = color_to_rgb(attr.get('textcolor', '#000000'), normalize=True)
        facecolors.append(color_to_rgb(attr.get('facecolor', '#ffffff'), normalize=True))
        edgecolors.append(color_to_rgb(attr.get('edgecolor', '#000000'), normalize=True))
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
                color=textcolor
            )
    coll = PatchCollection(
        patches,
        facecolor=facecolors,
        edgecolor=edgecolors,
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
