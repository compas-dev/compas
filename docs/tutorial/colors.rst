*********************
Colors and Color Maps
*********************

.. highlight:: python

.. rst-class:: lead

In COMPAS colors are defined in RGB color space, with components in the range of 0-1.


The RGB Color Circle
====================

The color class (:class:`compas.colors.Color`) provides constructor methods
for the primary, secondary, and tertiary colors of the RGB color wheel or color circle.

**Primary**

::

    >>> Color.red()
    Color(1.0, 0.0, 0.0, 1.0)
    >>> Color.green()
    Color(0.0, 1.0, 0.0, 1.0)
    >>> Color.blue()
    Color(0.0, 0.0, 1.0, 1.0)

**Secondary**

::

    >>> Color.yellow()
    Color(1.0, 1.0, 0.0, 1.0)
    >>> Color.cyan()
    Color(0.0, 1.0, 1.0, 1.0)
    >>> Color.magenta()
    Color(1.0, 0.0, 1.0, 1.0)

**Tertiary**

::

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

.. plot::
    :caption: Colors of the RGB color circle.

    from compas_plotters.plotter import Plotter
    from compas.geometry import Point, Circle
    from compas.colors import Color

    plotter = Plotter(figsize=(13, 1))

    plotter.add(Circle(([0, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.red())
    plotter.add(Circle(([1, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.orange())
    plotter.add(Circle(([2, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.yellow())
    plotter.add(Circle(([3, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.lime())
    plotter.add(Circle(([4, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.green())
    plotter.add(Circle(([5, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.mint())
    plotter.add(Circle(([6, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.cyan())
    plotter.add(Circle(([7, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.azure())
    plotter.add(Circle(([8, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.blue())
    plotter.add(Circle(([9, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.violet())
    plotter.add(Circle(([10, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.magenta())
    plotter.add(Circle(([11, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.pink())
    plotter.add(Circle(([12, 0, 0], [0, 0, 1]), 0.4), facecolor=Color.red())

    plotter.zoom_extents()
    plotter.show()


Lighter and Darker Colors
=========================

The color class (:class:`compas.colors.Color`) provides methods to generate lighter and darker variations of a given color.
The methods can be used to modify the colors in-place (:meth:`compas.colors.Color.lighten` and :meth:`compas.colors.Color.darken`),
or to generate new colors (:meth:`compas.colors.Color.lightened` and :meth:`compas.colors.Color.darkened`).

::

    >>> red = Color.red()
    >>> red.lighten(50)
    None
    >>> red.darken(50)
    None
    >>> red
    Color(1.0, 0.0, 0.0, 1.0)

::

    >>> red = Color.red()
    >>> red.lightened(50)
    Color(1.0, 0.5, 0.5, 1.0)
    >>> red.darkened(50)
    Color(0.5, 0.0, 0.0, 1.0)

.. plot::
    :caption: Lighter and darker colors of the color wheel.

    from compas_plotters.plotter import Plotter
    from compas.geometry import Point, Circle
    from compas.colors import Color

    plotter = Plotter(figsize=(13, 9))

    red = Color.red()
    orange = Color.orange()
    yellow = Color.yellow()
    lime = Color.lime()
    green = Color.green()
    mint = Color.mint()
    cyan = Color.cyan()
    azure = Color.azure()
    blue = Color.blue()
    violet = Color.violet()
    magenta = Color.magenta()
    pink = Color.pink()

    plotter.add(Circle(([0, 0, 0], [0, 0, 1]), 0.4), facecolor=red)
    plotter.add(Circle(([1, 0, 0], [0, 0, 1]), 0.4), facecolor=orange)
    plotter.add(Circle(([2, 0, 0], [0, 0, 1]), 0.4), facecolor=yellow)
    plotter.add(Circle(([3, 0, 0], [0, 0, 1]), 0.4), facecolor=lime)
    plotter.add(Circle(([4, 0, 0], [0, 0, 1]), 0.4), facecolor=green)
    plotter.add(Circle(([5, 0, 0], [0, 0, 1]), 0.4), facecolor=mint)
    plotter.add(Circle(([6, 0, 0], [0, 0, 1]), 0.4), facecolor=cyan)
    plotter.add(Circle(([7, 0, 0], [0, 0, 1]), 0.4), facecolor=azure)
    plotter.add(Circle(([8, 0, 0], [0, 0, 1]), 0.4), facecolor=blue)
    plotter.add(Circle(([9, 0, 0], [0, 0, 1]), 0.4), facecolor=violet)
    plotter.add(Circle(([10, 0, 0], [0, 0, 1]), 0.4), facecolor=magenta)
    plotter.add(Circle(([11, 0, 0], [0, 0, 1]), 0.4), facecolor=pink)
    plotter.add(Circle(([12, 0, 0], [0, 0, 1]), 0.4), facecolor=red)

    plotter.add(Circle(([0, 1, 0], [0, 0, 1]), 0.4), facecolor=red.darkened(25))
    plotter.add(Circle(([1, 1, 0], [0, 0, 1]), 0.4), facecolor=orange.darkened(25))
    plotter.add(Circle(([2, 1, 0], [0, 0, 1]), 0.4), facecolor=yellow.darkened(25))
    plotter.add(Circle(([3, 1, 0], [0, 0, 1]), 0.4), facecolor=lime.darkened(25))
    plotter.add(Circle(([4, 1, 0], [0, 0, 1]), 0.4), facecolor=green.darkened(25))
    plotter.add(Circle(([5, 1, 0], [0, 0, 1]), 0.4), facecolor=mint.darkened(25))
    plotter.add(Circle(([6, 1, 0], [0, 0, 1]), 0.4), facecolor=cyan.darkened(25))
    plotter.add(Circle(([7, 1, 0], [0, 0, 1]), 0.4), facecolor=azure.darkened(25))
    plotter.add(Circle(([8, 1, 0], [0, 0, 1]), 0.4), facecolor=blue.darkened(25))
    plotter.add(Circle(([9, 1, 0], [0, 0, 1]), 0.4), facecolor=violet.darkened(25))
    plotter.add(Circle(([10, 1, 0], [0, 0, 1]), 0.4), facecolor=magenta.darkened(25))
    plotter.add(Circle(([11, 1, 0], [0, 0, 1]), 0.4), facecolor=pink.darkened(25))
    plotter.add(Circle(([12, 1, 0], [0, 0, 1]), 0.4), facecolor=red.darkened(25))

    plotter.add(Circle(([0, 2, 0], [0, 0, 1]), 0.4), facecolor=red.darkened(50))
    plotter.add(Circle(([1, 2, 0], [0, 0, 1]), 0.4), facecolor=orange.darkened(50))
    plotter.add(Circle(([2, 2, 0], [0, 0, 1]), 0.4), facecolor=yellow.darkened(50))
    plotter.add(Circle(([3, 2, 0], [0, 0, 1]), 0.4), facecolor=lime.darkened(50))
    plotter.add(Circle(([4, 2, 0], [0, 0, 1]), 0.4), facecolor=green.darkened(50))
    plotter.add(Circle(([5, 2, 0], [0, 0, 1]), 0.4), facecolor=mint.darkened(50))
    plotter.add(Circle(([6, 2, 0], [0, 0, 1]), 0.4), facecolor=cyan.darkened(50))
    plotter.add(Circle(([7, 2, 0], [0, 0, 1]), 0.4), facecolor=azure.darkened(50))
    plotter.add(Circle(([8, 2, 0], [0, 0, 1]), 0.4), facecolor=blue.darkened(50))
    plotter.add(Circle(([9, 2, 0], [0, 0, 1]), 0.4), facecolor=violet.darkened(50))
    plotter.add(Circle(([10, 2, 0], [0, 0, 1]), 0.4), facecolor=magenta.darkened(50))
    plotter.add(Circle(([11, 2, 0], [0, 0, 1]), 0.4), facecolor=pink.darkened(50))
    plotter.add(Circle(([12, 2, 0], [0, 0, 1]), 0.4), facecolor=red.darkened(50))

    plotter.add(Circle(([0, 3, 0], [0, 0, 1]), 0.4), facecolor=red.darkened(75))
    plotter.add(Circle(([1, 3, 0], [0, 0, 1]), 0.4), facecolor=orange.darkened(75))
    plotter.add(Circle(([2, 3, 0], [0, 0, 1]), 0.4), facecolor=yellow.darkened(75))
    plotter.add(Circle(([3, 3, 0], [0, 0, 1]), 0.4), facecolor=lime.darkened(75))
    plotter.add(Circle(([4, 3, 0], [0, 0, 1]), 0.4), facecolor=green.darkened(75))
    plotter.add(Circle(([5, 3, 0], [0, 0, 1]), 0.4), facecolor=mint.darkened(75))
    plotter.add(Circle(([6, 3, 0], [0, 0, 1]), 0.4), facecolor=cyan.darkened(75))
    plotter.add(Circle(([7, 3, 0], [0, 0, 1]), 0.4), facecolor=azure.darkened(75))
    plotter.add(Circle(([8, 3, 0], [0, 0, 1]), 0.4), facecolor=blue.darkened(75))
    plotter.add(Circle(([9, 3, 0], [0, 0, 1]), 0.4), facecolor=violet.darkened(75))
    plotter.add(Circle(([10, 3, 0], [0, 0, 1]), 0.4), facecolor=magenta.darkened(75))
    plotter.add(Circle(([11, 3, 0], [0, 0, 1]), 0.4), facecolor=pink.darkened(75))
    plotter.add(Circle(([12, 3, 0], [0, 0, 1]), 0.4), facecolor=red.darkened(75))

    plotter.add(Circle(([0, 4, 0], [0, 0, 1]), 0.4), facecolor=red.darkened(100))
    plotter.add(Circle(([1, 4, 0], [0, 0, 1]), 0.4), facecolor=orange.darkened(100))
    plotter.add(Circle(([2, 4, 0], [0, 0, 1]), 0.4), facecolor=yellow.darkened(100))
    plotter.add(Circle(([3, 4, 0], [0, 0, 1]), 0.4), facecolor=lime.darkened(100))
    plotter.add(Circle(([4, 4, 0], [0, 0, 1]), 0.4), facecolor=green.darkened(100))
    plotter.add(Circle(([5, 4, 0], [0, 0, 1]), 0.4), facecolor=mint.darkened(100))
    plotter.add(Circle(([6, 4, 0], [0, 0, 1]), 0.4), facecolor=cyan.darkened(100))
    plotter.add(Circle(([7, 4, 0], [0, 0, 1]), 0.4), facecolor=azure.darkened(100))
    plotter.add(Circle(([8, 4, 0], [0, 0, 1]), 0.4), facecolor=blue.darkened(100))
    plotter.add(Circle(([9, 4, 0], [0, 0, 1]), 0.4), facecolor=violet.darkened(100))
    plotter.add(Circle(([10, 4, 0], [0, 0, 1]), 0.4), facecolor=magenta.darkened(100))
    plotter.add(Circle(([11, 4, 0], [0, 0, 1]), 0.4), facecolor=pink.darkened(100))
    plotter.add(Circle(([12, 4, 0], [0, 0, 1]), 0.4), facecolor=red.darkened(100))

    plotter.add(Circle(([0, -1, 0], [0, 0, 1]), 0.4), facecolor=red.lightened(25))
    plotter.add(Circle(([1, -1, 0], [0, 0, 1]), 0.4), facecolor=orange.lightened(25))
    plotter.add(Circle(([2, -1, 0], [0, 0, 1]), 0.4), facecolor=yellow.lightened(25))
    plotter.add(Circle(([3, -1, 0], [0, 0, 1]), 0.4), facecolor=lime.lightened(25))
    plotter.add(Circle(([4, -1, 0], [0, 0, 1]), 0.4), facecolor=green.lightened(25))
    plotter.add(Circle(([5, -1, 0], [0, 0, 1]), 0.4), facecolor=mint.lightened(25))
    plotter.add(Circle(([6, -1, 0], [0, 0, 1]), 0.4), facecolor=cyan.lightened(25))
    plotter.add(Circle(([7, -1, 0], [0, 0, 1]), 0.4), facecolor=azure.lightened(25))
    plotter.add(Circle(([8, -1, 0], [0, 0, 1]), 0.4), facecolor=blue.lightened(25))
    plotter.add(Circle(([9, -1, 0], [0, 0, 1]), 0.4), facecolor=violet.lightened(25))
    plotter.add(Circle(([10, -1, 0], [0, 0, 1]), 0.4), facecolor=magenta.lightened(25))
    plotter.add(Circle(([11, -1, 0], [0, 0, 1]), 0.4), facecolor=pink.lightened(25))
    plotter.add(Circle(([12, -1, 0], [0, 0, 1]), 0.4), facecolor=red.lightened(25))

    plotter.add(Circle(([0, -2, 0], [0, 0, 1]), 0.4), facecolor=red.lightened(50))
    plotter.add(Circle(([1, -2, 0], [0, 0, 1]), 0.4), facecolor=orange.lightened(50))
    plotter.add(Circle(([2, -2, 0], [0, 0, 1]), 0.4), facecolor=yellow.lightened(50))
    plotter.add(Circle(([3, -2, 0], [0, 0, 1]), 0.4), facecolor=lime.lightened(50))
    plotter.add(Circle(([4, -2, 0], [0, 0, 1]), 0.4), facecolor=green.lightened(50))
    plotter.add(Circle(([5, -2, 0], [0, 0, 1]), 0.4), facecolor=mint.lightened(50))
    plotter.add(Circle(([6, -2, 0], [0, 0, 1]), 0.4), facecolor=cyan.lightened(50))
    plotter.add(Circle(([7, -2, 0], [0, 0, 1]), 0.4), facecolor=azure.lightened(50))
    plotter.add(Circle(([8, -2, 0], [0, 0, 1]), 0.4), facecolor=blue.lightened(50))
    plotter.add(Circle(([9, -2, 0], [0, 0, 1]), 0.4), facecolor=violet.lightened(50))
    plotter.add(Circle(([10, -2, 0], [0, 0, 1]), 0.4), facecolor=magenta.lightened(50))
    plotter.add(Circle(([11, -2, 0], [0, 0, 1]), 0.4), facecolor=pink.lightened(50))
    plotter.add(Circle(([12, -2, 0], [0, 0, 1]), 0.4), facecolor=red.lightened(50))

    plotter.add(Circle(([0, -3, 0], [0, 0, 1]), 0.4), facecolor=red.lightened(75))
    plotter.add(Circle(([1, -3, 0], [0, 0, 1]), 0.4), facecolor=orange.lightened(75))
    plotter.add(Circle(([2, -3, 0], [0, 0, 1]), 0.4), facecolor=yellow.lightened(75))
    plotter.add(Circle(([3, -3, 0], [0, 0, 1]), 0.4), facecolor=lime.lightened(75))
    plotter.add(Circle(([4, -3, 0], [0, 0, 1]), 0.4), facecolor=green.lightened(75))
    plotter.add(Circle(([5, -3, 0], [0, 0, 1]), 0.4), facecolor=mint.lightened(75))
    plotter.add(Circle(([6, -3, 0], [0, 0, 1]), 0.4), facecolor=cyan.lightened(75))
    plotter.add(Circle(([7, -3, 0], [0, 0, 1]), 0.4), facecolor=azure.lightened(75))
    plotter.add(Circle(([8, -3, 0], [0, 0, 1]), 0.4), facecolor=blue.lightened(75))
    plotter.add(Circle(([9, -3, 0], [0, 0, 1]), 0.4), facecolor=violet.lightened(75))
    plotter.add(Circle(([10, -3, 0], [0, 0, 1]), 0.4), facecolor=magenta.lightened(75))
    plotter.add(Circle(([11, -3, 0], [0, 0, 1]), 0.4), facecolor=pink.lightened(75))
    plotter.add(Circle(([12, -3, 0], [0, 0, 1]), 0.4), facecolor=red.lightened(75))

    plotter.add(Circle(([0, -4, 0], [0, 0, 1]), 0.4), facecolor=red.lightened(100))
    plotter.add(Circle(([1, -4, 0], [0, 0, 1]), 0.4), facecolor=orange.lightened(100))
    plotter.add(Circle(([2, -4, 0], [0, 0, 1]), 0.4), facecolor=yellow.lightened(100))
    plotter.add(Circle(([3, -4, 0], [0, 0, 1]), 0.4), facecolor=lime.lightened(100))
    plotter.add(Circle(([4, -4, 0], [0, 0, 1]), 0.4), facecolor=green.lightened(100))
    plotter.add(Circle(([5, -4, 0], [0, 0, 1]), 0.4), facecolor=mint.lightened(100))
    plotter.add(Circle(([6, -4, 0], [0, 0, 1]), 0.4), facecolor=cyan.lightened(100))
    plotter.add(Circle(([7, -4, 0], [0, 0, 1]), 0.4), facecolor=azure.lightened(100))
    plotter.add(Circle(([8, -4, 0], [0, 0, 1]), 0.4), facecolor=blue.lightened(100))
    plotter.add(Circle(([9, -4, 0], [0, 0, 1]), 0.4), facecolor=violet.lightened(100))
    plotter.add(Circle(([10, -4, 0], [0, 0, 1]), 0.4), facecolor=magenta.lightened(100))
    plotter.add(Circle(([11, -4, 0], [0, 0, 1]), 0.4), facecolor=pink.lightened(100))
    plotter.add(Circle(([12, -4, 0], [0, 0, 1]), 0.4), facecolor=red.lightened(100))

    plotter.zoom_extents()
    plotter.show()


Saturation
==========

Similar to generating lighter and darker colors, the color class provides methods for saturating or desaturating colors
(:meth:`compas.colors.Color.saturate` and :meth:`compas.colors.Color.desaturate`, and :meth:`compas.colors.Color.saturated` and :meth:`compas.colors.Color.desaturated`).

.. plot::
    :caption: Lighter and darker colors of the color wheel.

    from compas_plotters.plotter import Plotter
    from compas.geometry import Point, Circle
    from compas.colors import Color

    plotter = Plotter(figsize=(13, 5))

    red = Color.red()
    orange = Color.orange()
    yellow = Color.yellow()
    lime = Color.lime()
    green = Color.green()
    mint = Color.mint()
    cyan = Color.cyan()
    azure = Color.azure()
    blue = Color.blue()
    violet = Color.violet()
    magenta = Color.magenta()
    pink = Color.pink()

    plotter.add(Circle(([0, 0, 0], [0, 0, 1]), 0.4), facecolor=red)
    plotter.add(Circle(([1, 0, 0], [0, 0, 1]), 0.4), facecolor=orange)
    plotter.add(Circle(([2, 0, 0], [0, 0, 1]), 0.4), facecolor=yellow)
    plotter.add(Circle(([3, 0, 0], [0, 0, 1]), 0.4), facecolor=lime)
    plotter.add(Circle(([4, 0, 0], [0, 0, 1]), 0.4), facecolor=green)
    plotter.add(Circle(([5, 0, 0], [0, 0, 1]), 0.4), facecolor=mint)
    plotter.add(Circle(([6, 0, 0], [0, 0, 1]), 0.4), facecolor=cyan)
    plotter.add(Circle(([7, 0, 0], [0, 0, 1]), 0.4), facecolor=azure)
    plotter.add(Circle(([8, 0, 0], [0, 0, 1]), 0.4), facecolor=blue)
    plotter.add(Circle(([9, 0, 0], [0, 0, 1]), 0.4), facecolor=violet)
    plotter.add(Circle(([10, 0, 0], [0, 0, 1]), 0.4), facecolor=magenta)
    plotter.add(Circle(([11, 0, 0], [0, 0, 1]), 0.4), facecolor=pink)
    plotter.add(Circle(([12, 0, 0], [0, 0, 1]), 0.4), facecolor=red)

    plotter.add(Circle(([0, 1, 0], [0, 0, 1]), 0.4), facecolor=red.desaturated(25))
    plotter.add(Circle(([1, 1, 0], [0, 0, 1]), 0.4), facecolor=orange.desaturated(25))
    plotter.add(Circle(([2, 1, 0], [0, 0, 1]), 0.4), facecolor=yellow.desaturated(25))
    plotter.add(Circle(([3, 1, 0], [0, 0, 1]), 0.4), facecolor=lime.desaturated(25))
    plotter.add(Circle(([4, 1, 0], [0, 0, 1]), 0.4), facecolor=green.desaturated(25))
    plotter.add(Circle(([5, 1, 0], [0, 0, 1]), 0.4), facecolor=mint.desaturated(25))
    plotter.add(Circle(([6, 1, 0], [0, 0, 1]), 0.4), facecolor=cyan.desaturated(25))
    plotter.add(Circle(([7, 1, 0], [0, 0, 1]), 0.4), facecolor=azure.desaturated(25))
    plotter.add(Circle(([8, 1, 0], [0, 0, 1]), 0.4), facecolor=blue.desaturated(25))
    plotter.add(Circle(([9, 1, 0], [0, 0, 1]), 0.4), facecolor=violet.desaturated(25))
    plotter.add(Circle(([10, 1, 0], [0, 0, 1]), 0.4), facecolor=magenta.desaturated(25))
    plotter.add(Circle(([11, 1, 0], [0, 0, 1]), 0.4), facecolor=pink.desaturated(25))
    plotter.add(Circle(([12, 1, 0], [0, 0, 1]), 0.4), facecolor=red.desaturated(25))

    plotter.add(Circle(([0, 2, 0], [0, 0, 1]), 0.4), facecolor=red.desaturated(50))
    plotter.add(Circle(([1, 2, 0], [0, 0, 1]), 0.4), facecolor=orange.desaturated(50))
    plotter.add(Circle(([2, 2, 0], [0, 0, 1]), 0.4), facecolor=yellow.desaturated(50))
    plotter.add(Circle(([3, 2, 0], [0, 0, 1]), 0.4), facecolor=lime.desaturated(50))
    plotter.add(Circle(([4, 2, 0], [0, 0, 1]), 0.4), facecolor=green.desaturated(50))
    plotter.add(Circle(([5, 2, 0], [0, 0, 1]), 0.4), facecolor=mint.desaturated(50))
    plotter.add(Circle(([6, 2, 0], [0, 0, 1]), 0.4), facecolor=cyan.desaturated(50))
    plotter.add(Circle(([7, 2, 0], [0, 0, 1]), 0.4), facecolor=azure.desaturated(50))
    plotter.add(Circle(([8, 2, 0], [0, 0, 1]), 0.4), facecolor=blue.desaturated(50))
    plotter.add(Circle(([9, 2, 0], [0, 0, 1]), 0.4), facecolor=violet.desaturated(50))
    plotter.add(Circle(([10, 2, 0], [0, 0, 1]), 0.4), facecolor=magenta.desaturated(50))
    plotter.add(Circle(([11, 2, 0], [0, 0, 1]), 0.4), facecolor=pink.desaturated(50))
    plotter.add(Circle(([12, 2, 0], [0, 0, 1]), 0.4), facecolor=red.desaturated(50))

    plotter.add(Circle(([0, 3, 0], [0, 0, 1]), 0.4), facecolor=red.desaturated(75))
    plotter.add(Circle(([1, 3, 0], [0, 0, 1]), 0.4), facecolor=orange.desaturated(75))
    plotter.add(Circle(([2, 3, 0], [0, 0, 1]), 0.4), facecolor=yellow.desaturated(75))
    plotter.add(Circle(([3, 3, 0], [0, 0, 1]), 0.4), facecolor=lime.desaturated(75))
    plotter.add(Circle(([4, 3, 0], [0, 0, 1]), 0.4), facecolor=green.desaturated(75))
    plotter.add(Circle(([5, 3, 0], [0, 0, 1]), 0.4), facecolor=mint.desaturated(75))
    plotter.add(Circle(([6, 3, 0], [0, 0, 1]), 0.4), facecolor=cyan.desaturated(75))
    plotter.add(Circle(([7, 3, 0], [0, 0, 1]), 0.4), facecolor=azure.desaturated(75))
    plotter.add(Circle(([8, 3, 0], [0, 0, 1]), 0.4), facecolor=blue.desaturated(75))
    plotter.add(Circle(([9, 3, 0], [0, 0, 1]), 0.4), facecolor=violet.desaturated(75))
    plotter.add(Circle(([10, 3, 0], [0, 0, 1]), 0.4), facecolor=magenta.desaturated(75))
    plotter.add(Circle(([11, 3, 0], [0, 0, 1]), 0.4), facecolor=pink.desaturated(75))
    plotter.add(Circle(([12, 3, 0], [0, 0, 1]), 0.4), facecolor=red.desaturated(75))

    plotter.add(Circle(([0, 4, 0], [0, 0, 1]), 0.4), facecolor=red.desaturated(100))
    plotter.add(Circle(([1, 4, 0], [0, 0, 1]), 0.4), facecolor=orange.desaturated(100))
    plotter.add(Circle(([2, 4, 0], [0, 0, 1]), 0.4), facecolor=yellow.desaturated(100))
    plotter.add(Circle(([3, 4, 0], [0, 0, 1]), 0.4), facecolor=lime.desaturated(100))
    plotter.add(Circle(([4, 4, 0], [0, 0, 1]), 0.4), facecolor=green.desaturated(100))
    plotter.add(Circle(([5, 4, 0], [0, 0, 1]), 0.4), facecolor=mint.desaturated(100))
    plotter.add(Circle(([6, 4, 0], [0, 0, 1]), 0.4), facecolor=cyan.desaturated(100))
    plotter.add(Circle(([7, 4, 0], [0, 0, 1]), 0.4), facecolor=azure.desaturated(100))
    plotter.add(Circle(([8, 4, 0], [0, 0, 1]), 0.4), facecolor=blue.desaturated(100))
    plotter.add(Circle(([9, 4, 0], [0, 0, 1]), 0.4), facecolor=violet.desaturated(100))
    plotter.add(Circle(([10, 4, 0], [0, 0, 1]), 0.4), facecolor=magenta.desaturated(100))
    plotter.add(Circle(([11, 4, 0], [0, 0, 1]), 0.4), facecolor=pink.desaturated(100))
    plotter.add(Circle(([12, 4, 0], [0, 0, 1]), 0.4), facecolor=red.desaturated(100))

    plotter.zoom_extents()
    plotter.show()


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

To quickly plot a color palette for visual inspection use plot method of the color map class :meth:`compas.colors.ColorMap.plot`.
For example, the "viridis" map from `matplotlib`.

.. plot::

    from compas.colors import ColorMap

    map = ColorMap.from_mpl('viridis')
    map.plot()


Examples
--------

Using the following template we can compare various color maps.

::

    >>> from compas.colors import Color, ColorMap
    >>> from compas.geometry import Point, Bezier
    >>> from compas_plotters.plotter import Plotter

::

    >>> points = [Point(0, 0, 0), Point(3, 6, 0), Point(6, -6, 6), Point(9, 0, 0)]
    >>> curve = Bezier(points)

::

    >>> cmap = ...

::

    >>> plotter = Plotter(figsize=(16, 9))
    >>> n = 500
    >>> for i, point in enumerate(curve.locus(n)):
    ...     color = cmap(i, 0, n - 1)
    ...     plotter.add(point, facecolor=color, edgecolor=color, edgewidth=0.5, size=10)
    ...
    >>> plotter.zoom_extents()
    >>> plotter.show()


From RGB
~~~~~~~~

::

    >>> cmap = ColorMap.from_rgb()

.. plot::

    from compas.colors import Color, ColorMap
    from compas.geometry import Point, Bezier
    from compas_plotters.plotter import Plotter
    points = [Point(0, 0, 0), Point(3, 6, 0), Point(6, -6, 6), Point(9, 0, 0)]
    curve = Bezier(points)

    cmap = ColorMap.from_rgb()

    plotter = Plotter(figsize=(16, 9))
    n = 500
    for i, point in enumerate(curve.locus(n)):
        color = cmap(i, 0, n - 1)
        plotter.add(point, facecolor=color, edgecolor=color, edgewidth=0.5, size=10)
    plotter.zoom_extents()
    plotter.show()


From One Color
~~~~~~~~~~~~~~

::

    >>> cmap = ColorMap.from_color(Color.red())
    >>> cmap = ColorMap.from_color(Color.red(), rangetype='light')
    >>> cmap = ColorMap.from_color(Color.red(), rangetype='dark')

.. plot::

    from compas.colors import Color, ColorMap
    from compas.geometry import Point, Bezier, Translation
    from compas_plotters.plotter import Plotter
    points = [Point(0, 0, 0), Point(3, 6, 0), Point(6, -6, 6), Point(9, 0, 0)]
    curve = Bezier(points)

    plotter = Plotter(figsize=(16, 9))
    n = 500

    cmap = ColorMap.from_color(Color.red())
    for i, point in enumerate(curve.transformed(Translation.from_vector([0, 0, 0])).locus(n)):
        color = cmap(i, 0, n - 1)
        plotter.add(point, facecolor=color, edgecolor=color, edgewidth=0.5, size=10)

    cmap = ColorMap.from_color(Color.red(), rangetype='light')
    for i, point in enumerate(curve.transformed(Translation.from_vector([0, -1, 0])).locus(n)):
        color = cmap(i, 0, n - 1)
        plotter.add(point, facecolor=color, edgecolor=color, edgewidth=0.5, size=10)

    cmap = ColorMap.from_color(Color.red(), rangetype='dark')
    for i, point in enumerate(curve.transformed(Translation.from_vector([0, -2, 0])).locus(n)):
        color = cmap(i, 0, n - 1)
        plotter.add(point, facecolor=color, edgecolor=color, edgewidth=0.5, size=10)

    plotter.zoom_extents()
    plotter.show()


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
