*************
Visualization
*************

This tutorial is about visualization of COMPAS objects in Rhino, Grasshopper, and Blender.
For information about standalone 2D visualizations (i.e. "plotting"), please visit the tutorial about :ref:`tutorial_plotters`.
For information about standalone 3D visualizations, please visit the documentation of :py:mod:`compas_view2`: https://compas.dev/compas_view2.


Object - Artist Pairs
=====================

COMPAS introduces the concept of **artists** for visualization.
An artist is a class whose primary goal is to perform the necessary conversions to visualize a COMPAS object in the viewport.
Each object type is paired with a corresponding artist type through a naming convention:
``Box`` - ``BoxArtist``, ``Mesh`` - ``MeshArtist``, ``RobotModel`` - ``RobotModelArtist``.
The individual artists are implemented for Rhino, Blender, and Grasshopper with a similar but not identical API,
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
This base class can be used to create the correct artist type for any of the COMPAS object types.
The type of artist that is created depends on the combination of the object type and the context in which the code is executed: Rhino, GH, or Blender.
This eliminates the need for more specific artist imports and allows for creating general scripts that can be run in Rhino, GH, and Blender without further modifications.

.. code-block:: python

    from compas.artists import Artist
    from compas.geometry import Frame, Box

    box = Box(Frame.worldXY(), 1, 1, 1)

    artist = Artist(box)
    artist.draw()


When running this code snippet in Rhino (using ``RunPythonScript``) the created artist will be of type :class:`compas_rhino.artists.BoxArtist`.

.. code-block:: python

    print(type(artist))
    # <class 'compas_rhino.artists.boxartist.BoxArtist'>


The base artist detected that the current execution context is Rhino,
and that the object passed to the constructor is a :py:class:`compas.geometry.Box`.

In Blender, we will get a :class:`compas_blender.artists.BoxArtist`.

.. code-block:: python

    print(type(artist))
    # <class 'compas_blender.artists.boxartist.BoxArtist'>


In Grasshopper, the snippet can be executed from within a GH User Component, with a small modification.
The output of the draw function has to be assigned to the output variable of the component (e.g. output variable ``a``).

.. code-block:: python

    from compas.artists import Artist
    from compas.geometry import Frame, Box
 
    box = Box(Frame.worldXY(), 1, 1, 1)

    artist = Artist(box)
    a = artist.draw()


.. code-block:: python

    print(type(artist))
    # <class 'compas_ghpython.artists.boxartist.BoxArtist'>


Colors
======

Colors are in the form of RGB tuples.
In Rhino and Grasshopper the components have to be specified in integer format with values between 0 and 255.
In Blender, colors have RGB components in float format with values between 0 and 1.
Values beyond 1 will cause the object to emit light with an intensity related to the provided number.
Therefore, the same colors can be used in Rhino, Grasshopper, and Blender, if they are in 0-255 integer format.

.. code-block:: python

    from compas.geometry import Frame, Box
    from compas.artists import Artist

    box = Box(Frame.worldXY(), 1, 1, 1)

    Artist(box).draw(color=(0, 255, 0))


Primitives and shapes only have one color attribute: ``compas.artists.PrimitiveArtist.color`` and ``compas.artists.ShapeArtist.color``.
This attribute can be set when the artist is constructed by providing a value for the parameter ``color``,
or by assigning a value to the attribute afterwards.

.. code-block:: python

    artist = Artist(box, color=(255, 0, 0))

    artist.color = (0, 0, 255)

    artist.draw()


The color value stored in the ``color`` attribute can be temporarily overwritten
using the ``color`` parameter of the ``draw`` function.
Note that the value of this parameter is not stored in the ``color`` attribute
and therefore only has an effect on the specific ``draw`` call.

.. code-block:: python

    artist.draw(color=(0, 255, 0))


Data structure artists a few mor color settings in addition to ``color``.
A detailed overview of the visualization options for data structures is provided in the section about datastructures: `Datastructures`_.


Shape Resolution
================

Shapes are visualized using a polygonal representation of their geometry.
All shapes, except for :class:`compas.geometry.Box` have to be discretised with a specific resolution
to create this representation.
The default resolution is ``u=16`` and ``v=16``.

.. code-block:: python

    from compas.artists import Artist
    from compas.geometry import Sphere

    sphere = Sphere([0, 0, 0], 1)

    Artist(sphere, u=32, v=32).draw()


The mechanism for changing resolution settings is the same as for colors.

.. code-block:: python

    artist = Artist(sphere, u=32, v=32)
    artist.u = 64
    artist.draw(v=64)


Datastructures
==============

Data structure artists provide the same base functionality as the artists for primitives and shapes,
and additional functionality related to the individual components.

.. code-block:: python

    from compas.artists import Artist
    from compas.geometry import Frame, Box
    from compas.datastructures import Mesh

    box = Box(Frame.worldXY(), 1, 1, 1)
    mesh = Mesh.from_shape(box)

    Artist(mesh).draw()


The above will draw the vertices, edges, and faces of the mesh as individual objects,
using a combination of the following methods

* :meth:`compas.artists.MeshArtist.draw_vertices`
* :meth:`compas.artists.MeshArtist.draw_edges`
* :meth:`compas.artists.MeshArtist.draw_faces`

The selection of elements to include in the drawing, and their colors,
can be modified with the parameters of :meth:`compas.artists.MeshArtist.draw`.

.. code-block:: python

    vertices = mesh.vertex_sample(size=4)
    edges = mesh.edge_sample(size=4)
    faces = mesh.face_sample(size=2)

    Artist(mesh).draw(vertices=vertices, edges=edges, faces=faces)


Colors can be modified globally per element type,

.. code-block:: python

    from compas.artists import Artist
    from compas.geometry import Frame, Box
    from compas.datastructures import Mesh

    vertices = mesh.vertex_sample(size=4)
    edges = mesh.edge_sample(size=4)
    faces = mesh.face_sample(size=2)

    Artist(mesh).draw(vertices=vertices, edges=edges, faces=faces, vertexcolor=(255, 0, 0), edgecolor=(0, 255, 0), facecolor=(0, 0, 255))


or individually per element.

.. code-block:: python

    import random
    from compas.artists import Artist
    from compas.geometry import Frame, Box
    from compas.datastructures import Mesh
    from compas.utilities import i_to_rgb

    vertices = mesh.vertex_sample(size=4)
    edges = mesh.edge_sample(size=4)
    faces = mesh.face_sample(size=2)

    vertex_color = {vertex: i_to_rgb(random.random()) for vertex in vertices}
    edge_color = {edge: i_to_rgb(random.random()) for edge in edges}
    face_color = {face: i_to_rgb(random.random()) for face in faces}

    Artist(mesh).draw(vertices=vertices, edges=edges, faces=faces, vertexcolor=vertex_color, edgecolor=edge_color, facecolor=face_color)


Redraw
======

In Rhino, automatic redrawing of the view has been turned off
such that the view is not continuously updated with every object that is added to the scene.

In most cases, a redraw of the view is called automatically called at the end of the execution of a script.
The only exception to that is when a script is executed using the built-in script editor on Mac.
In that context, an explicit call to ``Artist.redraw()`` is needed to prevent the view from freezing up.

.. code-block:: python

    from compas.geometry import Frame, Box
    from compas.artists import Artist

    box = Box(Frame.worldXY(), 1, 1, 1)

    Artist(box).draw()

    Artist.redraw_scene()


The ``redraw`` method can also be used for interactive scripts or dynamic visualizations,
where the view has to be redrawn at potentially multiple stages before the end of the script execution.

.. code-block:: python

    import time
    from compas.geometry import Frame, Box, Translation
    from compas.artists import Artist

    box = Box(Frame.worldXY(), 1, 1, 1)

    artist = Artist(box)
    artist.draw(redraw_scene=True)

    T = Translation.from_vector([1, 0, 0])

    for i in range(10):
        time.sleep(1)
        box.transform(T)
        artist.draw(redraw_scene=True)


Clear
=====

Sometimes the entire scene has to be cleaned before drawing any new objects.
This can be the case, for example, when running a script multiple times in a row to test different versions of a WIP algorithm or procedure.

.. code-block:: python

    Artist.clear_scene()


To clear only the objects previously drawn by a specific artist, use the ``clear`` method of the artist instance.

.. code-block:: python

    artist.clear()


Layers
======

The use of layers only applies to Rhino.

Under construction...


Collections
===========

The use of object collections only applies to Blender.

Under construction...


Custom Artists
==============

The procedure for making a custom artist in an extension package consists of the following steps.

1. Define the custom artist class for the relevant contexts.
2. Register the object with the artist for each context.

Consider, for example, an extension :mod:`compas_x`,
with a subpackage for custom datastructures (:mod:`compas_x.datastructures`)
and one for all Rhino related functionality (:mod:`compas_x.rhino`).

.. code-block:: python

    # compas_x.datastructures.xmesh.py

    from compas.datastructures import Mesh

    class XMesh(Mesh):

        # add custom methods


.. code-block:: python

    # compas_x.rhino.xmeshartist.py

    from compas_rhino.artists import MeshArtist

    class XMeshArtist(MeshArtist):

        # add custom visualisation methods


Note that registration of the object-artist pair is only necessary to facilitate automatic artist construction
using the base artist (:class:`compas.artists.Artist`).

.. code-block:: python

    # compas_x.rhino.__init__.py

    from compas.artists import Artist
    from compas.plugins import plugin
    from compas_x.datastructures import XMesh
    from .xmeshartist import XMeshArtist

    @plugin(category='factories', requires=['Rhino'])
    def register_artists():
        Artist.register(XMesh, XMeshArtist, context='Rhino')
