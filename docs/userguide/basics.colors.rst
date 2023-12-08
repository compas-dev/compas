*********************
Colors and Color Maps
*********************

.. rst-class:: lead

In COMPAS colors are defined in RGB color space, with components in the range of 0-1.


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

.. figure:: /_images/userguide/basics.colors_maps.png
    :figclass: figure
    :class: figure-img img-fluid

    `viridis` color map from matplotlib.


Examples
--------

Using the following template we can compare various color maps.

>>> from compas.colors import Color, ColorMap
>>> from compas.geometry import Bezier, Circle, Frame
>>> from compas_view2.app import App

>>> points = [Point(0, 0, 0), Point(3, 6, 0), Point(6, -6, 6), Point(9, 0, 0)]
>>> curve = Bezier(points)

>>> cmap = ...

>>> viewer = App()
>>> n = 500
>>> for i, point in enumerate(curve.to_points(n)):
...     color = cmap(i, minval=0, maxval=n - 1)
...     plotter.add(point, pointcolor=color, pointsize=30)
...
>>> viewer.show()


From RGB
~~~~~~~~

>>> cmap = ColorMap.from_rgb()

.. figure:: /_images/userguide/basics.colors_maps_from-rgb.png
    :figclass: figure
    :class: figure-img img-fluid

    Color map from RGB.


From One Color
~~~~~~~~~~~~~~

>>> cmap = ColorMap.from_color(Color.red())
>>> cmap = ColorMap.from_color(Color.red(), rangetype='light')
>>> cmap = ColorMap.from_color(Color.red(), rangetype='dark')

.. figure:: /_images/userguide/basics.colors_maps_from-rgb.png
    :figclass: figure
    :class: figure-img img-fluid

    Color maps constructed from a single color.


From Two Colors
~~~~~~~~~~~~~~~

::

    >>> cmap = ColorMap.from_two_colors(Color.from_hex('#0092D2'), Color.pink())
    >>> cmap = ColorMap.from_two_colors(Color.from_hex('#0092D2'), Color.pink(), diverging=True)

.. plot::

    from compas.colors import Color, ColorMap
    from compas.geometry import Point, Bezier, Translation
    from compas_plotters.plotter import Plotter
    points = [Point(0, 0, 0), Point(3, 6, 0), Point(6, -6, 6), Point(9, 0, 0)]
    curve = Bezier(points)

    plotter = Plotter(figsize=(16, 9))
    n = 500

    cmap = ColorMap.from_two_colors(Color.from_hex('#0092D2'), Color.pink())
    for i, point in enumerate(curve.transformed(Translation.from_vector([0, 0, 0])).locus(n)):
        color = cmap(i, 0, n - 1)
        plotter.add(point, facecolor=color, edgecolor=color, edgewidth=0.5, size=10)

    cmap = ColorMap.from_two_colors(Color.from_hex('#0092D2'), Color.pink(), diverging=True)
    for i, point in enumerate(curve.transformed(Translation.from_vector([0, -1, 0])).locus(n)):
        color = cmap(i, 0, n - 1)
        plotter.add(point, facecolor=color, edgecolor=color, edgewidth=0.5, size=10)

    plotter.zoom_extents()
    plotter.show()


From Three Colors
~~~~~~~~~~~~~~~~~

::

    >>> cmap = ColorMap.from_three_colors(Color.red(), Color.green(), Color.blue())

.. plot::

    from compas.colors import Color, ColorMap
    from compas.geometry import Point, Bezier, Translation
    from compas_plotters.plotter import Plotter
    points = [Point(0, 0, 0), Point(3, 6, 0), Point(6, -6, 6), Point(9, 0, 0)]
    curve = Bezier(points)

    plotter = Plotter(figsize=(16, 9))
    n = 500

    cmap = ColorMap.from_three_colors(Color.red(), Color.green(), Color.blue())

    for i, point in enumerate(curve.transformed(Translation.from_vector([0, 0, 0])).locus(n)):
        color = cmap(i, 0, n - 1)
        plotter.add(point, facecolor=color, edgecolor=color, edgewidth=0.5, size=10)

    plotter.zoom_extents()
    plotter.show()
