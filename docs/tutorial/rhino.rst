.. _working-in-rhino:

****************
Working in Rhino
****************

Using COMPAS in Rhino is not "all or nothing".


COMPAS objects to Rhino objects
===============================

COMPAS objects are converted to Rhino objects (or "exported" from COMPAS to Rhino)
by placing them in the Rhino model space.

This is accomplished by drawing the object with an "artist".
All COMPAS objects have (or should have) a corresponding artist.

.. code-block:: python

    from compas.geometry import Point
    from compas_rhino.artists import PointArtist

    point = Point(0, 0, 0)
    artist = PointArtist(point, color=(255, 0, 0))
    artist.draw()


Every artist keeps track of the GUIDs of the objects it places in the Rhino model space.

.. code-block:: python

