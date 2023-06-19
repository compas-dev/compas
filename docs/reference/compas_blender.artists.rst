********************************************************************************
compas_blender.artists
********************************************************************************

.. currentmodule:: compas_blender.artists

.. rst-class:: lead

Artists for visualizing (painting) COMPAS geometry, robots, and data structures in Blender.
The artists in this package provide plugins for the pluggable methods of the base artists defined in :mod:`compas.artists`.
They can be used directly from here (:mod:`compas_blender.artists`), or through the base artist :class:`~compas.artists.Artist`.


Primitive Artists
=================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CircleArtist
    FrameArtist
    LineArtist
    PointArtist
    PolygonArtist
    PolylineArtist
    VectorArtist


Shape Artists
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BoxArtist
    CapsuleArtist
    ConeArtist
    CylinderArtist
    PolyhedronArtist
    SphereArtist


Curve and Surface Artists
=========================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CurveArtist
    SurfaceArtist


Datastructure Artists
=====================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist
    NetworkArtist


Robot Artist
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RobotModelArtist


Base Classes
============

.. autosummary::
    :toctree: generated/

    BlenderArtist

