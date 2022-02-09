********************************************************************************
API Reference
********************************************************************************

Packages
========

.. toctree::
    :maxdepth: 1
    :titlesonly:

    api/compas
    api/compas_blender
    api/compas_ghpython
    api/compas_plotters
    api/compas_rhino


Package Structure
=================

All core packages have their public API defined and documented at the first subpackage level.

For example, although the mesh data structure is internally defined in `compas.datastructures.mesh.mesh.py`,
the mesh class should be imported from :mod:`compas.datastructures`.

.. code-block:: python

    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh()


This type of import is often referred to as "2nd-level import",
and was introduced to allow packages to be restructured without unnecessarily affecting the publicly available API.


Naming Conventions
==================

Class names are written in "CamelCase".

* :class:`compas.datastructures.Mesh`,
* :class:`compas.datastructures.VolMesh`,
* :class:`compas.geometry.Point`,
* :class:`compas_rhino.artists.BoxArtist`,
* :class:`compas_blender.artists.LineArtist`,
* ...

All other names use the "snake_case" naming convention.

* :func:`compas.geometry.cross_vectors`,
* :func:`compas.geometry.intersection_line_line`,
* :meth:`compas.datastructures.Mesh.vertex_attributes`,
* :attr:`compas.geometry.Line.start`
* ...

Module-level variables and constants are written in ALLCAPS.

* :data:`compas.PRECISION`,
* :data:`compas.IPY`,
* :data:`compas.BLENDER`,
* :data:`compas.APPDATA`,
* ...

Some functions or methods (especially in :mod:`compas.geometry`) have 2D variants,
marked with a ``_xy`` suffix,
meaning that they ignore the Z-coordinate of 3D inputs, and also accept inputs without Z-coordinates.
It is important to note that regardless of the dimensionality of the input,
these 2D function variants always return 3D output with Z-coordinate equal to 0 (zero).

* :func:`compas.geometry.bounding_box_xy`
* :func:`compas.geometry.intersection_line_line_xy`
* :func:`compas.geometry.is_polygon_convex_xy`
* ...


Type Information
================

To maintain compatibility with IronPython 2.7 used in Rhino and Grasshopper,
we currently don't use type hints in object definitions directly (in the future these type hints will be included in separate stub files).
Instead, we try to be as precise as possible with type information in the object docstrings.

For docstring formatting we follow the guidelines of `numpydoc`, as described here
https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard,
with some small exceptions, additions, and modifications, for the sake of improved precision and legibility.

Instead of ``list of float`` or ``list of list of int`` etc.,
we use a notation that is based on what the corresponding type hint would be:
``list[float]`` or ``list[list[int]]``.

In cases where both tuples and lists, or other types of "positionally ordered collections of items", are acceptable as input parameters
we use ``Sequence[float]``. A sequence containing a known set of multiple types is denoted with ``Sequence[float | int]``.

If a function requires as input a tuple or a list with a specific structure,
we simply write ``[float, float, float]``, for example for XYZ coordinates,
without "tuple" or "list" in front of the brackets.
To specify a nested lists of such objects, we use ``list[[float, float, float]]``,
which would indicate that the required input is a list of, for example, multiple XYZ coordinates,
without requiring any of the individual items to be specifically a tuple or a list.

For geometric inputs, the type information can quickly become quite long ad verbose.
Therefore, in addition to the above conventions, we define the following type aliases.

.. rst-class:: table table-bordered

.. list-table:: Basic Type Aliases
    :widths: auto
    :header-rows: 1

    * - Alias
      - Full Type Information
    * - ``point``
      - ``[float, float, float]`` | :class:`compas.geometry.Point`
    * - ``vector``
      - ``[float, float, float]`` | :class:`compas.geometry.Vector`
    * - ``quaternion``
      - ``[float, float, float, float]`` | :class:`compas.geometry.Quaternion`

Note the use of ``a | b`` instead of ``Union[a, b]``.
Type aliases can also be nested to further improve legibility of more complex types.

.. rst-class:: table table-bordered

.. list-table:: Nested Type Aliases
    :widths: auto
    :header-rows: 1

    * - Alias
      - Full Type Information
    * - ``line``
      - ``[point, point]`` | :class:`compas.geometry.Line`
    * - ``plane``
      - ``[point, vector]`` | :class:`compas.geometry.Plane`
    * - ``frame``
      - ``[point, vector, vector]`` | :class:`compas.geometry.Frame`
    * - ``circle``
      - ``[plane, float]``| :class:`compas.geometry.Circle`
    * - ``ellipse``
      - ``[plane, float, float]`` | :class:`compas.geometry.Ellipse`
    * - ``polyline``
      - ``Sequence[point]`` | :class:`compas.geometry.Polyline`
    * - ``polygon``
      - ``Sequence[point]`` | :class:`compas.geometry.Polygon`
