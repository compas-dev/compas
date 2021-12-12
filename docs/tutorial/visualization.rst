*************
Visualization
*************

This tutorial is about visualization of COMPAS objects in Rhino, Grasshopper, and Blender.
For information about standalone 2D visualizations (i.e. "plotting"), please visit the tutorial about :ref:`tutorial_plotters`.
For information about standalone 3D visualizations, please visit the documentation of :py:mod:`compas_view2`: <https://compas.dev/compas_view2>.

Object - Artist Pairs
=====================

Visualization of COMPAS objects is handled by artists.
Each object type is paired with a corresponding artist type through a naming convention.
The artists are implemented for Rhino, Blender, and Grasshopper with a similar but not identical API,
and have to be imported accordingly depending on the execution context.

.. raw:: html

    <div class="card">
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item">
                    <a class="nav-link active" data-toggle="tab" href="#object-artist-rhino">Rhino</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#object-artist-grasshopper">Grasshopper</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#object-artist-blender">Blender</a>
                </li>
            </ul>
        </div>
        <div class="card-body">
            <div class="tab-content">

.. raw:: html

    <div class="tab-pane active" id="object-artist-rhino">

.. code-block:: python

    from compas.geometry import Frame, Box
    from compas_rhino.artists import BoxArtist

    box = Box(Frame.worldXY(), 1, 1, 1)

    artist = BoxArtist(box)
    artist.draw()

.. raw:: html

    </div>
    <div class="tab-pane" id="object-artist-grasshopper">

.. code-block:: python

    from compas.geometry import Frame, Box
    from compas_ghpython.artists import BoxArtist

    box = Box(Frame.worldXY(), 1, 1, 1)

    artist = BoxArtist(box)
    a = artist.draw()

.. raw:: html

    </div>
    <div class="tab-pane" id="object-artist-blender">

.. code-block:: python

    from compas.geometry import Frame, Box
    from compas_blender.artists import BoxArtist

    box = Box(Frame.worldXY(), 1, 1, 1)

    artist = BoxArtist(box)
    artist.draw()

.. raw:: html

    </div>
    </div>
    </div>
    </div>


Base Artist
===========

The base artist class for all artists is :py:class:`compas.artists.Artist`.
Conveniently, this base class can also be used to create the correct artist type for any of the COMPAS object types.
The implementation of this artist depends on the context in which the code is executed: Rhino, GH, or Blender.

.. code-block:: python

    from compas.artists import Artist
    from compas.geometry import Frame, Box

    box = Box(Frame.worldXY(), 1, 1, 1)

    artist = Artist(box)
    artist.draw()


This code snippet can be executed in Rhino, Grasshopper and Blender.
The base artist will create an instance of the type of artist paired with the (data) object type.


.. code-block:: python

    print(type(artist))


Running this code snippet in Rhino (using ``RunPythonScript``) will print the following result for the artist types.

.. code-block:: none

    <class 'compas_rhino.artists.boxartist.BoxArtist'>
    <class 'compas_rhino.artists.meshartist.MeshArtist'>    


The base artist detected that the current execution context is Rhino,
that the objects passed to the constructor were a :py:class:`compas.geometry.Box`
and a :py:class:`compas.datastructures.Mesh`,
and paired the corresponding artist types with them.

Conversely, running the snippet in Blender will procude the following artist types.

.. code-block:: none

    <class 'compas_blender.artists.boxartist.BoxArtist'>
    <class 'compas_blender.artists.meshartist.MeshArtist'>    


In Grasshopper, the snippet can be executed from within a GH User Component, with a few small modifications.
For example, if the component has an output parameter named ``a``.

.. code-block:: python

    from compas.artists import Artist
    from compas.geometry import Box, Frame, Translation
    from compas.datastructures import Mesh

    a = []

    box = Box(Frame.worldXY(), 1, 1, 1)
    mesh = Mesh.from_shape(box)

    mesh.transform(Translation.from_vector([2, 0, 0]))

    artist = Artist(box)
    a += artist.draw()

    print(type(artist))

    artist = Artist(mesh)
    a += artist.draw()

    print(type(artist))


The resulting artist types are similar as before.

.. code-block:: none

    <class 'compas_ghpython.artists.boxartist.BoxArtist'>
    <class 'compas_ghpython.artists.meshartist.MeshArtist'>    


Colors
======

.. code-block:: python

    from compas.geometry import Box
    from 


Redraw
======


Datastructures
==============


Custom Artists
==============

