********************************************************************************
CPython in Rhino
********************************************************************************

.. make part of series *Working in Rhino* (part of the series *Working in ...*)
.. add to series: Configuration
.. add to series: Writing scripts
.. add to series: Working with datastructures (or, with the main library)
.. add to series: Making tools
.. add to series: Using CPython
.. add to series: RhinoMac (separate, but short)
.. add to series: Grasshopper (separate, but short)

.. * advantages of ironpython
.. * limitations of ironpython
.. * xfuncs
.. * specify the interpreter
.. * other options
.. * dynamic visualisation
.. * live interaction
.. * examples

In Rhino, Python scripts can be used to

(from the docs `what is python <http://developer.rhino3d.com/guides/rhinopython/what-is-rhinopython/#what-is-python>`_)

* Automate a repetitive task in Rhino much faster than you could do manually.
* Perform tasks in Rhino or Grasshopper that you don’t have access to in the standard set of Rhino commands or Grasshopper components.
* Generate geometry using algorithms.
* Many, many other things. It is a programming language after all.

Or, create

(also from the docs `where can you use python in rhino <http://developer.rhino3d.com/guides/rhinopython/what-is-rhinopython/#where-can-you-use-python-in-rhino>`_)

* Interactive scripts.
* New custom commands.
* Create new plug-ins.
* Read and Write customized file formats.
* Interact with cloud applications.
* Create realtime links to other applications
* Create customer Grasshopper components
* Store and display project specific information beyond what basic Rhino can store.

Rhino runs Python scripts using IronPython 2.7.
This is great because it provides access to the .NET framework.
However, this also means that many (C)Python libraries are not available.
For example Numpy, Scipy, Matplotlib, SimPy, Numba, NetworkX, CVXPY, Shapely, PyOpenGL, PySide, ...

With `compas.utilities.XFunc` this limitation can be partly removed.
Below is an example from the API reference.

.. code-block:: python

    import compas
    import compas_rhino

    from compas.datastructures import Mesh
    from compas.utilities import XFunc
    from compas_rhino.artists import MeshArtist

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    vertices = mesh.get_vertices_attributes('xyz')
    edges    = list(mesh.edges())
    fixed    = list(mesh.vertices_where({'vertex_degree': 2}))
    q        = mesh.get_edges_attribute('q', 1.0)
    loads    = mesh.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))

    xyz, q, f, l, r = XFunc('compas.numerical.fd_numpy')(vertices, edges, fixed, q, loads)

    for key, attr in mesh.vertices(True):
        attr['x'] = xyz[key][0]
        attr['y'] = xyz[key][1]
        attr['z'] = xyz[key][2]

    artist = MeshArtist(mesh)

    artist.clear()

    artist.draw_vertices()
    artist.draw_edges()

    artist.redraw()

