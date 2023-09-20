********************************************************************************
compas.artists
********************************************************************************

.. currentmodule:: compas.artists

.. rst-class:: lead

For visualization of geometry objects and data structures, COMPAS provides "artists".
Every object type is paired with a corresponding artist type that is capable of visualizing the data of the object.
This package provides base artist classes with pluggable methods
that receive an implementation from plugins defined by various visualization contexts.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Artist
    GeometryArtist
    MeshArtist
    NetworkArtist
    VolMeshArtist


Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DataArtistNotRegistered
    NoArtistContextError
