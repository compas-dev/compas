.. _gs-freecad:

*******
FreeCAD
*******

.. rst-class:: lead

Although there is no official support package for FreeCAD, working with COMPAS in FreeCAD is actually quite simple.


Install FreeCAD
===============

If FreeCAD is installed using ``conda``, the Python interpreter in FreeCAD automagically has access to all the packages installed in the same environment.

.. code-block:: bash

    conda create -n CAD python=3.8 freecad COMPAS -c conda-forge --yes


Launch FreeCAD
==============

To activate this mechanism, you have to launch FreeCAD from the environment it is installed in.

.. code-block:: bash

    conda activate CAD
    freecad


Basic Usage
===========

.. code-block:: python

    >>> import Mesh
    >>> import compas
    >>> from compas.datastructures import Mesh as cMesh

.. code-block:: python

    >>> mesh = cMesh.from_obj(compas.get('tubemesh.obj'))
    >>> mesh.quads_to_triangles()
    >>> freemesh = Mesh.Mesh(mesh.to_polygons())
    >>> Mesh.show(freemesh)
