
********************************************************************************
compas.artists
********************************************************************************

.. currentmodule:: compas.artists

.. rst-class:: lead


This package defines artists for visualising COMPAS objects.
Every object type is paired with a corresponding artist type that is capable of visualizing the data of the object.
The artists are implemented as pluggables, and automatically switch between plugins depending on the contexct in which they are used.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Artist
    DataArtistNotRegisteredError
    GeometryArtist
    MeshArtist
    NetworkArtist
    NoArtistContextError
    VolMeshArtist


Pluggables
==========

Pluggables are functions that don't have an actual implementation, but receive an implementation from a plugin.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    clear
    redraw
    register_artists



