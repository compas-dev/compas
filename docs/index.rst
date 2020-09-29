********************************************************************************
COMPAS Docs
********************************************************************************

.. rst-class:: lead

This is the documentation of the main library of the COMPAS framework.
It contains a core package, a package for 2D visualization,
and three packages for the integration in CAD software.

.. .. figure:: /_images/gh_verify.jpg
..      :figclass: figure
..      :class: figure-img img-fluid

The core package (:mod:`compas`) defines all functionality for geometry processing,
data structures, topology, numerical methods, robotics, the plugin mechanism, remote procedure calls ...
and can be used independently of CAD systems in any environment that supports Python.

The CAD packages (:mod:`compas_rhino`, :mod:`compas_ghpython`, :mod:`compas_blender`)
provide a unified framework for reading and writing CAD geometry, for visualization
of COMPAS geometry and data structures, and for basic user inter interaction
in Blender, Rhino, and Grasshopper.

The package for 2D visualisation (:mod:`compas_plotters`)
simplifies "plotting" of COMPAS geometry objects and data structures.


Table of Contents
=================

.. toctree::
   :maxdepth: 3
   :titlesonly:

   Introduction <self>
   installation
   gettingstarted
   tutorial
   api
   plugins
   devguide
   changelog
   license
   citing
