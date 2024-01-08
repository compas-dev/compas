*********************
Colors and Color Maps
*********************

.. rst-class:: lead

In COMPAS colors are defined in RGB color space, with components in the range of 0-1.

Basic Usage
===========


Color Spaces
============


Color Information
=================


The RGB Color Circle
====================

The color class (:class:`compas.colors.Color`) provides constructor methods
for the primary, secondary, and tertiary colors of the RGB color wheel or color circle.

Primary Colors
--------------

>>> Color.red()
Color(1.0, 0.0, 0.0, 1.0)
>>> Color.green()
Color(0.0, 1.0, 0.0, 1.0)
>>> Color.blue()
Color(0.0, 0.0, 1.0, 1.0)

Secondary Colors
----------------

>>> Color.yellow()
Color(1.0, 1.0, 0.0, 1.0)
>>> Color.cyan()
Color(0.0, 1.0, 1.0, 1.0)
>>> Color.magenta()
Color(1.0, 0.0, 1.0, 1.0)

Tertiary Colors
---------------

>>> Color.orange()
Color(1.0, 0.5, 0.0, 1.0)
>>> Color.lime()
Color(0.5, 1.0, 0.0, 1.0)
>>> Color.mint()
Color(0.0, 1.0, 0.5, 1.0)
>>> Color.azure()
Color(0.0, 0.5, 1.0, 1.0)
>>> Color.violet()
Color(0.5, 0.0, 1.0, 1.0)
>>> Color.pink()
Color(1.0, 0.0, 0.5, 1.0)

.. figure:: /_images/userguide/basics.colors_color-circle.png
    :figclass: figure
    :class: figure-img img-fluid

    The RGB color circle.


Lighter and Darker Colors
=========================

The color class (:class:`compas.colors.Color`) provides methods to generate lighter and darker variations of a given color.
The methods can be used to modify the colors in-place (:meth:`compas.colors.Color.lighten` and :meth:`compas.colors.Color.darken`),
or to generate new colors (:meth:`compas.colors.Color.lightened` and :meth:`compas.colors.Color.darkened`).

>>> red = Color.red()
>>> red.lighten(50)
None
>>> red.darken(50)
None
>>> red
Color(1.0, 0.0, 0.0, 1.0)

>>> red = Color.red()
>>> red.lightened(50)
Color(1.0, 0.5, 0.5, 1.0)
>>> red.darkened(50)
Color(0.5, 0.0, 0.0, 1.0)

.. figure:: /_images/userguide/basics.colors_lightness.png
    :figclass: figure
    :class: figure-img img-fluid

    Lightness.


Saturation
==========

Similar to generating lighter and darker colors, the color class provides methods for saturating or desaturating colors
(:meth:`compas.colors.Color.saturate` and :meth:`compas.colors.Color.desaturate`, and :meth:`compas.colors.Color.saturated` and :meth:`compas.colors.Color.desaturated`).

.. figure:: /_images/userguide/basics.colors_saturation.png
    :figclass: figure
    :class: figure-img img-fluid

    Saturation.


Color Maps
==========

Using :class:`compas.colors.ColorMap`, color maps can be constructed from various color inputs.

* :meth:`compas.colors.ColorMap.from_rgb`
* :meth:`compas.colors.ColorMap.from_color`
* :meth:`compas.colors.ColorMap.from_two_colors`
* :meth:`compas.colors.ColorMap.from_three_colors`

Maps based on named scientific color palettes designed by Fabio Crameri (https://www.fabiocrameri.ch/colourmaps/)
and some of the `matplotlib` color palettes are also available.

* :meth:`compas.colors.ColorMap.from_palette`
* :meth:`compas.colors.ColorMap.from_mpl`


There is currently no predefined function for color map examples.
However, using the following template we can compare various examples.

>>> from compas.geometry import Point, Polygon
>>> from compas.utilities import linspace, pairwise
>>> from compas.datastructures import Mesh
>>> from compas.colors import Color, ColorMap
>>> from compas_view2.app import App

>>> n = 1000
>>> t = 0.3

>>> up = []
>>> down = []
>>> for i in linspace(0, 10, n):
...    point = Point(i, 0, 0)
...    up.append(point + [0, t, 0])
...    down.append(point - [0, t, 0])

>>> polygons = []
>>> for (d, c), (a, b) in zip(pairwise(up), pairwise(down)):
...    polygons.append(Polygon([a, b, c, d]))

>>> mesh = Mesh.from_polygons(polygons)

>>> cmap = ...  # define color map here
>>> facecolors = {i: cmap(i, minval=0, maxval=n - 1) for i in range(n)}

>>> viewer = App()
>>> viewer.view.show_grid = False
>>> viewer.add(mesh, facecolor=facecolors, show_lines=False)
>>> viewer.show()


From Palette
------------

>>> cmap = ColorMap.from_mpl('viridis')

.. figure:: /_images/userguide/basics.colors_maps.png
    :figclass: figure
    :class: figure-img img-fluid

    `viridis` color map from matplotlib.


From RGB
--------

>>> cmap = ColorMap.from_rgb()

.. figure:: /_images/userguide/basics.colors_maps_from-rgb.png
    :figclass: figure
    :class: figure-img img-fluid

    Color map from RGB.


From One Color
--------------

>>> cmap = ColorMap.from_color(Color.red())
>>> cmap = ColorMap.from_color(Color.red(), rangetype='light')
>>> cmap = ColorMap.from_color(Color.red(), rangetype='dark')

.. figure:: /_images/userguide/basics.colors_maps_from-one-color.png
    :figclass: figure
    :class: figure-img img-fluid

    Color maps constructed from a single color.


From Two Colors
---------------

::

    >>> cmap = ColorMap.from_two_colors(Color.from_hex('#0092D2'), Color.pink())
    >>> cmap = ColorMap.from_two_colors(Color.from_hex('#0092D2'), Color.pink(), diverging=True)

.. figure:: /_images/userguide/basics.colors_maps_from-two-colors.png
    :figclass: figure
    :class: figure-img img-fluid

    Color maps constructed from two colors.


From Three Colors
-----------------

::

    >>> cmap = ColorMap.from_three_colors(Color.red(), Color.green(), Color.blue())

.. figure:: /_images/userguide/basics.colors_maps_from-three-colors.png
    :figclass: figure
    :class: figure-img img-fluid

    Color maps constructed from three colors.
