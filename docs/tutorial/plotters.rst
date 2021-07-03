**************
Plotters
**************

The COMPAS plotters (:mod:`compas_plotters`) provide an easy-to-use inteface for basic 2D visualisation
of COMPAS objects based on matplotlib.

The package contains four types of plotters: :class:`compas_plotters.GeometryPlotter`, :class:`compas_plotters.NetworkPlotter`, :class:`compas_plotters.MeshPlotter`, and ... :class:`compas_plotters.Plotter`.
The first three are deprecated in favour of :class:`compas_plotters.Plotter`, which is therefore the only one that will be described in this tutorial.


Example
=======

.. figure:: /_images/tutorial/plotters_example.png
    :figclass: figure
    :class: figure-img img-fluid

.. code-block:: python

    import random
    import compas
    from compas.geometry import Circle, Polyline
    from compas.datastructures import Network
    from compas_plotters import Plotter

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    start, end = random.sample(network.leaves(), 2)
    path = network.shortest_path(start, end)
    points = network.nodes_attributes('xy', keys=path)

    polyline = Polyline(points)
    circles = [Circle([point, [0, 0, 1]], 0.1 * index) for index, point in enumerate(points)]

    plotter = Plotter()

    plotter.add(network)
    plotter.add(polyline, linewidth=3)
    plotter.add_from_list(circles, facecolor=(0, 1, 1))

    plotter.zoom_extents()
    plotter.show()


Basic Usage
===========

Using :class:`compas_plotters.Plotter` is very simple.

1. Create a plotter instance.
2. Add Objects.
3. Optionally zoom the extents of all objects that were added.
4. Show the plot.

.. code-block:: python

    plotter = Plotter()

    # add objects

    plotter.zoom_extents()
    plotter.show()

COMPAS geometry objects and data structures can be added using :meth:`compas_plotters.Plotter.add`.
By adding an object, a corresponding "artist" is created automatically in the background,
and the plotter will use the artist to visualize the object.

The artists provide many configuration options to modify the display styles of the objects.
The :meth:`compas_plotters.Plotter.add` method accepts additional keyword arguments corresponding to those configuration options.
See the API reference of the individual artists for the available options per object type.

.. code-block:: python

    point = Point(0, 0, 0)

    plotter.add(point, size=10, facecolor=(1.0, 0.7, 0.7), edgecolor=(1.0, 0, 0))

Alternatively, multiple objects of the same type can also be added using :meth:`compas_plotters.Plotter.add_from_list`.
In this case all configurations options will be applied uniformly to all objects in the list.

.. code-block:: python

    cloud = Pointcloud.from_bounds(10, 10, 0, 100)

    plotter.add_from_list(cloud.points, size=1, facecolor=(1.0, 0.7, 0.7), edgecolor=(1.0, 0, 0))


Geometry Objects
================

Most of the geometry primitives are supported
and can be added to a plotter instance as described above:

* :class:`compas.geometry.Point`
* :class:`compas.geometry.Vector`
* :class:`compas.geometry.Line`
* :class:`compas.geometry.Circle`
* :class:`compas.geometry.Ellipse`
* :class:`compas.geometry.Polyline`
* :class:`compas.geometry.Polygon`

Bezier curves and pointclouds are currently not available yet, but will be added as well.
Note that in all cases, the ``z`` coordinates of the objects are simply ignored, and only a 2D representation is depicted.

.. code-block:: python

    plotter.add(point)
    plotter.add(vector)
    plotter.add(line)
    plotter.add(circle)
    plotter.add(ellipse)
    plotter.add(polyline)
    plotter.add(polygon)


Data Structures
===============

Of the three types of data structures, only network and mesh are supported.
Also in this case, the ``z`` coordinates of the geometry is ignored, and only a 2D representation is depicted.

.. code-block:: python

    plotter.add(point)
    plotter.add(vector)


Dynamic Plots
=============


Exports
=======
