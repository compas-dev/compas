********************************************************************************
COMPAS Docs
********************************************************************************

.. rst-class:: lead

The main library of the COMPAS framework consists of a core package (:mod:`compas`)
and several additional packages for integration of the core into CAD software
(:mod:`compas_rhino`, :mod:`compas_ghpython`, :mod:`compas_blender`).
The core package defines all *real* functionality.
The CAD packages simply provide a unified framework for processing,
visualising and interacting with datastructures and geometrical objects, and for
building user interfaces in different CAD software.


Core functionality
==================

To deal with the different academic backgrounds, programming skills, and computational
experience of its users, COMPAS is implemented primarily in Python and designed
to be entirely independent of the functionality of CAD software. As a result, it
can be used on different platforms and in combination with external software and
libraries, and at the same time take advantage of the various scientific and non-scientific
libraries available in the Python ecosystem itself. Furthermore, and perhaps more
importantly, it ensures that research based on COMPAS is not tied to a specific
CAD-based ecosystem.


CAD integration
===============

In the context of this framework CAD tools are obviously indispensible
tools to construct and manipulate geometry, apply constraints interactively, make
user interfaces, or even just to use as viewer for running scripts. The CAD helper
packages (:mod:`compas_rhino`, :mod:`compas_ghpython`, :mod:`compas_blender`) provide
a unified and consistent interface to CAD tools and their ecosystems.


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
   devguide
   roadmap
   changelog
   license
   citing
