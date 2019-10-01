********************************************************************************
Using callbacks
********************************************************************************

COMPAS implements a *callback* mechanism that provides a consistent way to
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
Let's assume we have an interative algorithm defined in some module ``algorithm.py``.
We want to use the algorithm in a script called ``script.py``, but instead of running the
algorithm as-is, we want to print a message at the end of every 10th iteration.

.. code-block:: python

    # algorithm.py

    def algo(kmax=100, callback=None):
        if callback:
            if not callable(callback):
                raise Exception('The callback function is not callable.')

        for k in range(kmax):
            # this is where the main algorithm stuff happens
            # ...

            # at the end of every iteration the callback is called if it was provided.
            if callback:
                callback(k)

.. code-block:: python

    # script.py

    from algorithm import algo

    iterations = []

    def print_iterations(k):
        if k % 5 == 0:
            iterations.append(k)
        if k % 10 == 0:
            print("iteration", k)

    algo(callback=print_iterations)
    print(iterations)


The result of running the script is the following

.. parsed-literal::

    iteration 0
    iteration 10
    iteration 20
    iteration 30
    iteration 40
    iteration 50
    iteration 60
    iteration 70
    iteration 80
    iteration 90
    [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]


Note that in addition to modifying the behaviour of the algorithm, without actually rewriting the algorithm,
the callback has access to variables defined in the context of the calling script.
This creates all sorts of interesting possibilities.


Dynamic plotting
================

Throughout the main library, callbacks are often used in combination with the plotters
to visualise intermediate steps of an algorithm, or to visualise the progress of
an iterative algorithm. Both can be very useful mechanisms for debugging.

For example, using a callback, we can easily visualise the iterative process of a smoothing algorithm.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas.geometry import mesh_smooth_centroid
    from compas_plotters import MeshPlotter

    # make a mesh from a sample file
    mesh = Mesh.from_obj(compas.get('faces.obj'))

    # identify the vertices that should stay fixed during smoothing
    fixed = list(mesh.vertices_where({'vertex_degree': 2}))

    # make a plotter and pause for 1s to visualise the initial state before smoothing
    plotter = MeshPlotter(mesh, figsize=(10, 7))
    plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
    plotter.draw_faces()
    plotter.draw_edges()
    plotter.update(pause=1.0)

    # define the callback function that will update the plot during smoothing
    def plot_progress(mesh, k, args):
        plotter.update_vertices()
        plotter.update_faces()
        plotter.update_edges()
        plotter.update(pause=0.001)

    # run the smoothing algorithm
    mesh_smooth_centroid(mesh, kmax=50, fixed=fixed, callback=plot_progress)

    # keep the plotting window open after smoothing is done
    plotter.show()


In the above snippet, the callback function will update the vertices, faces, and edges
of the mesh at every iteration and pause briefly before continuing with the next iteration.
Note that we don't have to pass the plotter explicitly to the callback, because it has access
to the variables available in the context where it was defined.

.. code-block:: python

    def plot_progress(mesh, k, args):
        plotter.update_vertices()
        plotter.update_faces()
        plotter.update_edges()
        plotter.update(pause=0.001)


The callback is handed off to the smoothing algorithm, which will call it at every
iteration. By default, the callback receives the mesh object and the number of the
current iteration as firs and second parameter, and then any additional parameters
that were passed to the algorithm as ``callback_args``.

.. code-block:: python

    mesh_smooth_centroid(mesh, kmax=50, fixed=fixed, callback=plot_progress)


The result should be something like this.

.. figure:: /_images/tutorial_callbacks_smoothing.gif
    :figclass: figure
    :class: figure-img img-fluid


Dynamic visualisation in Rhino
==============================

.. code-block:: python
    import compas
    from compas.datastructures import Mesh
    from compas.datastructures import smooth_area
    from compas_rhino.artists import MeshArtist
    from compas_rhino.conduits import MeshConduit

    # make a mesh datastructure from a Rhino mesh object
    mesh = Mesh.from_obj(compas.get('faces.obj'))

    fixed = list(mesh.vertices_where({'vertex_degree': 2}))

    # make an artist for visualization
    conduit = MeshConduit(mesh, refreshrate=5)

    # make a callback for updating the conduit
    def callback(k, args):
       conduit.redraw(k)

    # run the smoothing algorithm with the conduit enabled
    with conduit.enabled():
        mesh_smooth_area(mesh, fixed=fixed, kmax=100, callback=callback)

    # draw the final result
    artist = MeshArtist(mesh)
    artist.draw_mesh()


Applying constraints
====================

.. code-block:: python

    import compas_rhino
    from compas.datastructures import Mesh
    from compas.geometry import smooth_area
    from compas_rhino.helpers import mesh_from_guid
    from compas_rhino.conduits import MeshConduit
    from compas_rhino.geometry import RhinoSurface
    from compas_rhino.artists import MeshArtist

    fixed = list(mesh.vertices_where({'vertex_degree': 2}))

    # make a mesh datastructure from a Rhino mesh object
    guid = compas_rhino.select_mesh()
    mesh = mesh_from_guid(Mesh, guid)

    # make a target surface from a Rhino NURBS surface
    guid = compas_rhino.select_surface()
    target = RhinoSurface(guid)

    # make a conduit for visualization
    conduit = MeshConduit(mesh, refreshrate=5)

    # make a callback for updating the conduit
    # and for pulling the free vertices back to the surface at every iteration
    def callback(k, args):
        target.pull_mesh(mesh, fixed)
        conduit.redraw(k)

    # run the smoothing algorithm with the conduit enabled
    with conduit.enabled():
        mesh_smooth_area(mesh, fixed=fixed, kmax=100, callback=callback)

    # draw the final result
    artist = MeshArtist(mesh)
    artist.draw_mesh()
