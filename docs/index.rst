********************************************************************************
COMPAS Docs
********************************************************************************

.. rst-class:: lead

This is the documentation of the main library of COMPAS,
an open source framework for research and collaboration
in Architecture, Engineering, Fabrication, and Construction.

.. figure:: /_images/COMPAS.png
     :figclass: figure
     :class: figure-img img-fluid

The core package of COMPAS (:mod:`compas`) defines all functionality for geometry processing,
data structures, topology, numerical methods, robotics, the plugin mechanism, remote procedure calls ...
and can be used independently of CAD systems in any environment that supports Python programming.

The CAD packages (:mod:`compas_rhino`, :mod:`compas_ghpython`, :mod:`compas_blender`)
provide a unified framework for reading and writing CAD geometry, for visualization
of COMPAS geometry and data structures, and for basic user inter interaction
in Blender, Rhino, and Grasshopper.

The package for 2D visualisation (:mod:`compas_plotters`)
simplifies "plotting" of COMPAS geometry objects and data structures.


Getting Started
===============

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Getting Started

   installation
   configuration
   tutorial
   citing

Package Reference
=================

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Package Reference

   api/compas
   api/compas_blender
   api/compas_ghpython
   api/compas_rhino

Development
===========

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Development

   api
   devguide
   plugins
   releases
   license


.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`search`
