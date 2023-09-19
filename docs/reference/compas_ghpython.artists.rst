********************************************************************************
compas_ghpython.artists
********************************************************************************

.. currentmodule:: compas_ghpython.artists

.. rst-class:: lead

Artists for visualizing (painting) COMPAS geometry and data structures in Grasshopper using the GH Python component.
The artists in this package provide plugins for the pluggable methods of the base artists in :mod:`compas.artists`.
Therefore, they can be used directly, from here, or through the base artists :class:`~compas.artists.Artist`.


Geometry Artists
================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BoxArtist
    BrepArtist
    CapsuleArtist
    CircleArtist
    ConeArtist
    CurveArtist
    CylinderArtist
    FrameArtist
    LineArtist
    PlaneArtist
    PointArtist
    PolygonArtist
    PolyhedronArtist
    PolylineArtist
    VectorArtist
    SphereArtist
    SurfaceArtist
    TorusArtist


Datastructure Artists
=====================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist
    NetworkArtist
    VolMeshArtist


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    GHArtist
