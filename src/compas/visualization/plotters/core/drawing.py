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
                   fontsize=10.0,
                   grid=True,
                   xlim=None,
                   ylim=None,
                   ticklength=20,
                   tickfontsize=10.0,
                   xscale='linear',
                   yscale='linear',
                   bgcolor='#ffffff'):
    """Initialises plot axes object for matplotlib plotting.

    Parameters:
        figsize (tuple): (horizontal, vertical) size of the figure.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        fontname (str): Fontname of the main labels and text.
        fontsize (int): Fontsize of the main labels and text.
        grid (boolean): Display grid.
        xlim (tuple): Limits of the X-axis.
        ylim (tuple) : Limits of the Y-axis.
        ticklength (float): length of the ticks.
        tickfontsize (int): Fontsize of the ticks.
        xscale (str): normal 'linear' or logarithmic 'log' x axis.
        yscale (str): normal 'linear' or logarithmic 'log' y axis.

    Returns:
        object: Matplotlib axes.

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

    Parameters:
        size (tuple): (horizontal, vertical) size of the figure.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        zlabel (str): Label for the z-axis.
        fontname (str): Fontname of the main labels and text.
        fontsize (int): Fontsize of the main labels and text.
        grid (boolean): Display grid.
        limits (dic): Axis limits and tick spacing.
        ticklength (float): length of the ticks.
        tickfontsize (int): Fontsize of the ticks.
        angle (tuple): elev and azim angles for 3D plots.

    Returns:
        object: Matplotlib axes.
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
    """"""
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


def draw_xpoints_xy(points, axes):
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
        fontsize  = point.get('fontsize') or 24
        circles.append(Circle(pos, radius=radius))
        facecolors.append(fcolor)
        edgecolors.append(ecolor)
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
    """"""
    p = len(points)
    points = asarray(points)
    if isinstance(facecolor, basestring):
        facecolor = [facecolor] * p
    if isinstance(edgecolor, basestring):
        edgecolor = [edgecolor] * p
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    axes.plot(x, y, z, 'o', color=(1.0, 1.0, 1.0))


# ==============================================================================
# lines
# ==============================================================================


def draw_lines_xy(lines,
                  axes,
                  linewidth=1.0,
                  linestyle='-',
                  color='#000000',
                  alpha=1.0):
    """"""
    l = len(lines)
    if isinstance(linewidth, (int, float)):
        linewidth = float(linewidth)
        linewidth = [linewidth] * l
    if isinstance(color, basestring):
        color = [color] * l
    # --------------------------------------------------------------------------
    coll = LineCollection(
        lines,
        linewidths=linewidth,
        colors=color,
        linestyle=linestyle,
        alpha=alpha,
        zorder=ZORDER_LINES
    )
    axes.add_collection(coll)


def draw_xlines_xy(lines, axes, alpha=1.0, linestyle='solid'):
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
        fontsize  = line.get('fontsize') or 24
        fromto.append((sp, ep))
        widths.append(width)
        colors.append(color)
        if text:
            x, y, z = midpoint_line_xy((sp, ep))
            t = axes.text(x,
                          y,
                          text,
                          fontsize=fontsize,
                          zorder=ZORDER_LABELS,
                          ha='center',
                          va='center',
                          color=textcolor)
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
    """"""
    l = len(lines)
    if isinstance(linewidth, (int, float)):
        linewidth = float(linewidth)
        linewidth = [linewidth] * l
    if isinstance(color, basestring):
        color = [color] * l
    # --------------------------------------------------------------------------
    coll = Line3DCollection(
        lines,
        linewidths=linewidth,
        colors=color,
        linestyle=linestyle,
        zorder=ZORDER_LINES
    )
    axes.add_collection(coll)


# ==============================================================================
# arrows
# ==============================================================================


def draw_xarrows_xy(lines, axes):
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
        arrowprops['color']     = line.get('color', '#000000')
        arrowprops['linewidth'] = line.get('width', 1.0)
        axes.annotate(
            '',
            xy=ep,
            xytext=sp,
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
                          color=textcolor)
            t.set_bbox({'color': '#ffffff', 'alpha': 1.0, 'edgecolor': '#ffffff'})


# ==============================================================================
# labels
# ==============================================================================


def draw_xlabels_xy(labels, axes):
    for label in labels:
        x, y      = label['pos']
        text      = label['text']
        fontsize  = label['fontsize']
        color     = label.get('color') or '#ffffff'
        textcolor = label.get('textcolor') or '#000000'
        bbox      = dict(color=color, edgecolor=color, alpha=1.0, pad=0.0)
        t = axes.text(
            x,
            y,
            text,
            fontsize=fontsize,
            zorder=ZORDER_LABELS,
            ha='center',
            va='center',
            color=textcolor
        )
        t.set_bbox(bbox)


# ==============================================================================
# faces
# ==============================================================================


def draw_xpolygons_xy(polygons, axes):
    facecolors = []
    edgecolors = []
    linewidths = []
    patches = []
    for attr in polygons:
        points    = attr['points']
        text      = attr.get('text')
        textcolor = attr.get('textcolor', '#000000')
        facecolors.append(attr.get('facecolor', '#ffffff'))
        edgecolors.append(attr.get('edgecolor', '#000000'))
        linewidths.append(attr.get('edgewidth', 1.0))
        patches.append(Polygon(points))
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
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
