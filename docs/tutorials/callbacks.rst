********************************************************************************
Using callbacks
********************************************************************************

**COMPAS** implements a *callback* mechanism that provides a consistent way to
customise algorithms, apply constraints, visualise progress of iterative algorithms, ...

.. note::

    A *callback* is a function that is passed to another function as a parameter
    such that the latter function can call the former at any time during its own
    execution. Perhaps the name *callback* is based on the fact that through the
    *callback* the second function can "call back" into the scope where the first
    function was defined. Or perhaps not :), but it is a convenient way to think
    about it because at time of execution, the callback has access to the variables
    of the scope in which it was defined.


In principle, the mechanism can be summarised with the following snippets.

.. code-block:: python

    # algorithm.py

    def algo(..., callback=None):

        if callback:
            if not callable(callback):
                raise Exception('The callback function is not callable.')

        # stuff

        for k in range(kmax):
            # stuffs

            if callback:
                callback(k)

        # more stuffs

.. code-block:: python

    # somescript.py

    from algorithm import algo

    text = 'iteration number:'

    def callback(k):
        print(text, k)

    algo(..., callback=callback)


In this case, the result would be a bit boring, because the callback would simply
print the number of the current iteration of the algorithm. Note, however, that
the callback has access to the variable ``text``, even though that ariable was defined
in a different context that the one in which the callback is called.


Dynamic plotting
================

Throughout the main library, callbacks are often used in combination with the plotters
to visualise intermediate steps of an algorithm, or to visualise the progress of
an iterative algorithm. Both can be very useful mechanisms for debugging.

For example, from :mod:`compas.geometry`, an code snippet visualising the progress
of an iterative smoothing algorithm (:func:`compas.geometry.mesh_smooth_centroid`).

.. code-block:: python

    import compas

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.geometry import mesh_smooth_centroid

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start' : mesh.vertex_coordinates(u, 'xy'),
            'end'   : mesh.vertex_coordinates(v, 'xy'),
            'color' : '#cccccc',
            'width' : 0.5
        })
    plotter.draw_lines(lines)

    plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.update(pause=1.0)

    def callback(mesh, k, args):
        print(k)
        plotter.update_vertices()
        plotter.update_faces()
        plotter.update_edges()
        plotter.update(pause=0.001)

    mesh_smooth_centroid(mesh, kmax=50, fixed=fixed, callback=callback)

    plotter.show()


We use a mesh plotter as visualisation tool.

.. code-block:: python

    plotter = MeshPlotter(mesh, figsize=(10, 7))


First, as a reference, we plot a set of lines corresponding to the original
configuration of the mesh.

.. code-block:: python

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start' : mesh.vertex_coordinates(u, 'xy'),
            'end'   : mesh.vertex_coordinates(v, 'xy'),
            'color' : '#cccccc',
            'width' : 0.5
        })
    plotter.draw_lines(lines)


Then we initialise the vertices, edges and faces that will be updated at every
iteration to visualise the process. We also tell the plotter to pause for a second,
to be able to digest the orginal configuration before the smoothing starts.

.. code-block:: python

    plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
    plotter.draw_faces()
    plotter.draw_edges()

    plotter.update(pause=1.0)


The next step is to define the callback function that will update the plotter.
The plotter has dedicated functions for this. They update the geometry of the
collections of vertices, edges and faces while keeping the style attributes as they
were set by the original calls to the draw functions. With a call to the general
update function we update the drawing.

The callback is handed off to the smoothing algorithm, which will call it at every
iteration. By default, the callback receives the mesh object and the number of the
current iteration as firs and second parameter, and then any additional parameters
that were passed to the algorithm.

.. code-block:: python

    def callback(mesh, k, args):
        print(k)
        plotter.update_vertices()
        plotter.update_faces()
        plotter.update_edges()
        plotter.update(pause=0.001)

    mesh_smooth_centroid(mesh, kmax=50, fixed=fixed, callback=callback)


Finally, we make sure that the plotting window remains active and visible.

.. code-block:: python

    plotter.show()


The result shpould be something like this.

.. figure:: /_images/tutorial_callbacks_smoothing.gif
    :figclass: figure
    :class: figure-img img-fluid


Dynamic visualisation in Rhino with conduits
============================================


Applying constraints
====================


Live interaction
================

