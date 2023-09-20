:html_theme.sidebar_secondary.remove:

********************************************************************************
COMPAS Documentation
********************************************************************************

.. rst-class:: lead

This is the documentation of the core infratructure of COMPAS,
an open source framework for computational research and collaboration
in Architecture, Engineering, Fabrication, and Construction.

.. .. figure:: /_images/COMPAS.png
..      :figclass: figure
..      :class: figure-img img-fluid

.. The main package of COMPAS (:mod:`compas`) defines all functionality for geometry processing,
.. data structures, topology, numerical methods, robotics, the plugin mechanism, remote procedure calls ...
.. and can be used independently of CAD systems in any environment that supports Python programming.

.. The CAD packages (:mod:`compas_rhino`, :mod:`compas_ghpython`, :mod:`compas_blender`)
.. provide a unified framework for reading and writing CAD geometry, for visualization
.. of COMPAS geometry and data structures, and for basic user inter interaction
.. in Blender, Rhino, and Grasshopper.

.. The package for 2D visualisation (:mod:`compas_plotters`)
.. simplifies "plotting" of COMPAS geometry objects and data structures.

.. Sections
.. ========

.. The documentation is divided into the following sections.

.. grid:: 1 1 2 2
   :gutter: 4

   .. grid-item-card::

      User Guide
      ^^^^^^^^^^

      If you want to use COMPAS for your research or in one of your projects,
      this is the place to start.

      .. toctree::
         :maxdepth: 2
         :titlesonly:

         userguide/index


   .. grid-item-card::

      Package Reference
      ^^^^^^^^^^^^^^^^^

      The reference documentation of the core package and the CAD packages.

      .. toctree::
         :maxdepth: 2
         :titlesonly:

         reference/index


   .. grid-item-card::

      Developer Guide
      ^^^^^^^^^^^^^^^

      If you want to contribute to COMPAS, this is the place to start.

      .. toctree::
         :maxdepth: 2
         :titlesonly:

         devguide/index


   .. grid-item-card::

      Extensions
      ^^^^^^^^^^

      The core extensions to COMPAS and the AEC toolboxes manages by the compas-dev team are listed here.

      .. toctree::
         :maxdepth: 2
         :titlesonly:

         extensions/index

