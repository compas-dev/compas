.. _acadia2017_day1_datastructures:

********************************************************************************
Datastructures
********************************************************************************


Why data structures?
====================

Consider set of points and faces.
How would you answer basic questions about the connectivity of these objects?
For example:

* Which vertices are connected to a particular vertex?
* Which faces are connected to a particular vertex?
* Which vertices make up a particular face?
* Which faces are connected to a particular face?
* ...

.. code-block:: python

    # geometrical solution to some of these questions


By structuring the data, these questions can be answered topologically rather than
geometrically, which is much more efficient.

Applications ...


Network, Mesh, VolMesh
----------------------

The *compas* framework contains three types of data structures and related operations and algorithms:

* ``compas.datastructures.network``
* ``compas.datastructures.mesh``
* ``compas.datastructures.volmesh``


Visualization
=============

.. plot::
    :include-source:
    
    import compas

    from compas.datastructures import Mesh
    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)

    plotter.draw_vertices()
    plotter.draw_faces()
    plotter.draw_edges()
    plotter.show()


Builders and constructors
=========================


Accessing the data
==================


Accessing the data attributes
=============================


Topology
========


Geometry
========


Operations
==========


Algorithms
==========


Customization
=============


Numerical computation
=====================


CAD integration
===============
