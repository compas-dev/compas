********************************************************************************
Using C/C++ code
********************************************************************************

.. split up
.. A Simple Function
.. Parameters
.. Callbacks
.. Using Eigen
.. Using libigl
.. Example: Smoothing
.. Example: Force Density Method
.. Example: Laplacian editing

Summary
=======

In this tutorial we will write a smoothing function in C++ and make it available
directly in Python. We will also use a callback to live visualise the iterations
of the algorithm and to dynamically change the boundary conditions. An
implementation of the code in this tutorial is available in the geometry package:

* :func:`compas.geometry.smooth_centroid_cpp`


Requirements
============

* a C++ compiler (for example g++, which is part of the GNU compiler collection)

Setup
=====

For this tutorial, we will use the following files and folders::

    + smoothing_cpp
        + src
            - main.cpp
        - smoothing.so
        - smoothing.py


The smoothing function
======================

First, the C++ code. The smoothing function will implement a simple barycentric
smoothing algorithm, in which at every iteration, each vertex is moved to the
barycentre of its neighbours.

By the way, I have no real experience in writing C++ code, so i am sure that this
can be done a lot more elegantly and efficiently.
I would be happy to hear about any and all suggestions (vanmelet@ethz.ch).

.. code-block:: cpp

    #include <vector>

    using namespace std;

    extern "C"
    {
        typedef void callback(int k);

        void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbours, int kmax, callback func);
    }

    void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbours, int kmax, callback func) 
    {
        int k;
        int i;
        int j, n;
        double cx, cy, cz;

        vector< vector<double> > xyz(v, vector<double>(3, 0.0));

        for (k = 0; k < kmax; k++) {

            // make a copy of the current vertex positions

            for (i = 0; i < v; i++) {
                xyz[i][0] = vertices[i][0];
                xyz[i][1] = vertices[i][1];
                xyz[i][2] = vertices[i][2];
            }

            // move each vertex to the barycentre of its neighbours

            for (i = 0; i < v; i++) {

                // skip the vertex if it is fixed
    
                if (fixed[i]) {
                    continue;
                }

                cx = 0.0;
                cy = 0.0;
                cz = 0.0;

                for (j = 0; j < nbrs[i]; j++) {
                    n = neighbours[i][j];

                    cx += xyz[n][0];
                    cy += xyz[n][1];
                    cz += xyz[n][2];
                }

                vertices[i][0] = cx / nbrs[i];
                vertices[i][1] = cy / nbrs[i];
                vertices[i][2] = cz / nbrs[i];
            }

            // call the callback

            func(k);
        }
    }


The ``ctypes`` wrapper
======================

Looking a the signature of the C++ function, the code is expecting the following
input arguments:

1. ``int v``
2. ``int *nbrs``
3. ``int *fixed``
4. ``double **vertices``
5. ``int **neighbours``
6. ``int kmax``
7. ``callback func``

Or, in other words:

1. the number of vertices, as an integer
2. the number of neighbours per vertex, as a an array of integers
3. a mask identifying the fixed vertices, as an array of integers (0/1)
4. the vertex coordinates, as a two-dimensional array of doubles
5. the vertex neighbours, as a two-dimensional array of integers
6. the maximum number of iterations, as an integer
7. the callback function, as a function of type callback

Note that the sizes of the arrays are unknown at compile time, since they depend
on the number of vertices in the system. Therefore they are passed as pointers.
My understanding of this is based on whatever google spat out and a few SO posts...

* https://stackoverflow.com/questions/8767166/passing-a-2d-array-to-a-c-function
* https://stackoverflow.com/questions/8767166/passing-a-2d-array-to-a-c-function/17569578#17569578
* http://www.cplusplus.com/doc/tutorial/arrays/

We want to be able to call the function from Python, which essentially boils down
to something like this:

.. code-block:: python

    import ctypes
    import compas
    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.interop.core.cpp.xdarray import Array1D
    from compas.interop.core.cpp.xdarray import Array2D

    # get the C++ smoothing library

    smoothing = ctypes.cdll.LoadLibrary('smoothing.so')

    # make a mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    # extract the required data for smoothing

    vertices   = mesh.get_vertices_attributes('xyz')
    adjacency  = [mesh.vertex_neighbours(key) for key in mesh.vertices()]
    fixed      = [int(mesh.vertex_degree(key) == 2) for key in mesh.vertices()]
    v          = len(vertices)
    nbrs       = [len(adjacency[i]) for i in range(v)]
    neighbours = [adjacency[i] + [0] * (10 - nbrs[i]) for i in range(v)]
    kmax       = 50

    # ==============================================================================
    # convert the python data to C-compatible types
    # ==============================================================================

    # ...

    # ==============================================================================

    # make a plotter for visualisation

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    # plot the original line geometry as a reference

    lines = []
    for a, b in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(a, 'xy'),
            'end'  : mesh.vertex_coordinates(b, 'xy'),
            'color': '#cccccc',
            'width': 0.5
        })

    plotter.draw_lines(lines)

    # plot the starting point

    plotter.draw_vertices()
    plotter.draw_edges()

    plotter.update(pause=0.5)

    # ==============================================================================
    # define the callback function
    # ==============================================================================

    def callback(k):
        print(k)

        # update the plot
        # and change the boundary conditions

        # ...

    # ==============================================================================

    # ==============================================================================
    # set the argument types for the smoothing function
    # and call it with C-compatible data
    # ==============================================================================

    smoothing.smooth_centroid.argtypes = [...]

    smoothing.smooth_centroid(...)    

    # ==============================================================================


C-compatible types and data
---------------------------

Some of these conversion are quite trivial. For example, converting an integer is simply:

.. code-block:: python

    c_v = ctypes.c_int(v)


Also the 1D arrays are not too complicated. For example:

.. code-block:: python
    
    c_fixed_type = ctypes.c_int * v
    c_fixed_data = c_fixed_type(*fixed)


The 2D arrays are already a bit trickier. For example:

.. code-block:: python
    
    c_vertex_type = ctypes.c_double * 3
    c_vertices_type = ctypes.POINTER(ctypes.c_double) * v
    c_vertices_data = c_vertices_type(*[c_vertex_type(x, y, z) for x, y, z in vertices])


Converting the callback is also quite straightforward:

.. code-block:: python

    c_callback_type = ctypes.CFUNCTYPE(None, c_int)
    c_callback = c_callback_type(callback)


To simplify the construction of C-compatible types, and C-compatible data,
there are a few helper classes in :mod:`compas.interop`:

* :class:`compas.interop.core.cpp.xdarray.Array1D`
* :class:`compas.interop.core.cpp.xdarray.Array2D`
* :class:`compas.interop.core.cpp.xdarray.Array3D`

With these helpers, the code for the conversion becomes:

.. code-block:: python

    # ==============================================================================
    # convert the python data to C-compatible types
    # ==============================================================================

    c_nbrs       = Array1D(nbrs, 'int')
    c_fixed      = Array1D(fixed, 'int')
    c_vertices   = Array2D(vertices, 'double')
    c_neighbours = Array2D(neighbours, 'int')
    c_callback   = ctypes.CFUNCTYPE(None, ctypes.c_int)

    # ==============================================================================


Then we let the smoothing function what it can expect in terms of types by setting
the argument types of the callable:

.. code-block:: python

    # ==============================================================================
    # set the argument types for the smoothing function
    # and call it with C-compatible data
    # ==============================================================================

    smoothing.smooth_centroid.argtypes = [
        c_int,
        c_nbrs.ctype,
        c_fixed.ctype,
        c_vertices.ctype,
        c_neighbours.ctype,
        c_int,
        c_callback
    ]

    smoothing.smooth_centroid(
        c_int(v),
        c_nbrs.cdata,
        c_fixed.cdata,
        c_vertices.cdata,
        c_neighbours.cdata,
        c_int(kmax),
        c_callback(wrapper)
    )    

    # ==============================================================================


The last step is to define the functionality of the callback.
The goal is to visualise the changing geometry
and to change the location of the fixed points 
during the smoothing process; in C++, but from Python.

.. code-block:: python

    # ==============================================================================
    # define the callback function
    # ==============================================================================

    def callback(k):
        print(k)

        xyz = c_vertices.cdata

        # change the boundary conditions

        if k < kmax - 1:
            xyz[18][0] = 0.1 * (k + 1)

        # update the plot

        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(pause=0.001)

        for key, attr in mesh.vertices(True):
            attr['x'] = xyz[key][0]
            attr['y'] = xyz[key][1]
            attr['z'] = xyz[key][2]

    # ==============================================================================


The result
==========

Putting it all together, we get the following script. Simply copy-paste it and run...

.. code-block:: python

    import ctypes
    from ctypes import *
    import compas
    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.interop.core.cpp.xdarray import Array1D
    from compas.interop.core.cpp.xdarray import Array2D


    # get the C++ smoothing library

    smoothing = ctypes.cdll.LoadLibrary('smoothing.so')


    # make a mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))


    # extract the required data for smoothing

    vertices   = mesh.get_vertices_attributes('xyz')
    adjacency  = [mesh.vertex_neighbours(key) for key in mesh.vertices()]
    fixed      = [int(mesh.vertex_degree(key) == 2) for key in mesh.vertices()]
    v          = len(vertices)
    nbrs       = [len(adjacency[i]) for i in range(v)]
    neighbours = [adjacency[i] + [0] * (10 - nbrs[i]) for i in range(v)]
    kmax       = 50


    # convert the python data to C-compatible types

    c_nbrs       = Array1D(nbrs, 'int')
    c_fixed      = Array1D(fixed, 'int')
    c_vertices   = Array2D(vertices, 'double')
    c_neighbours = Array2D(neighbours, 'int')
    c_callback   = CFUNCTYPE(None, c_int)


    # make a plotter for visualisation

    plotter = MeshPlotter(mesh, figsize=(10, 7))


    # plot the original line geometry as a reference

    lines = []
    for a, b in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(a, 'xy'),
            'end'  : mesh.vertex_coordinates(b, 'xy'),
            'color': '#cccccc',
            'width': 0.5
        })

    plotter.draw_lines(lines)


    # plot the starting point

    plotter.draw_vertices(facecolor={key: '#000000' for key in mesh.vertices() if mesh.vertex_degree(key) == 2})
    plotter.draw_edges()

    plotter.update(pause=0.5)


    # define the callback function

    def callback(k):
        print(k)

        xyz = c_vertices.cdata

        # change the boundary conditions

        if k < kmax - 1:
            xyz[18][0] = 0.1 * (k + 1)

        # update the plot

        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(pause=0.001)

        for key, attr in mesh.vertices(True):
            attr['x'] = xyz[key][0]
            attr['y'] = xyz[key][1]
            attr['z'] = xyz[key][2]


    # set the argument types for the smoothing function
    # and call it with C-compatible data

    smoothing.smooth_centroid.argtypes = [
        c_int,
        c_nbrs.ctype,
        c_fixed.ctype,
        c_vertices.ctype,
        c_neighbours.ctype,
        c_int,
        c_callback
    ]

    smoothing.smooth_centroid(
        c_int(v),
        c_nbrs.cdata,
        c_fixed.cdata,
        c_vertices.cdata,
        c_neighbours.cdata,
        c_int(kmax),
        c_callback(callback)
    )    


    # keep the plotting window alive

    plotter.show()


CAD environments
================

This setup can also be used in CAD environments.
Assuming that "*if it works in RhinoPython, it works everywhere*", here is a script for Rhino
that does the same as the one above, 
but uses :func:`compas.geometry.smooth_centroid_cpp` to make things a bit simpler.

.. code-block:: python

    from __future__ import print_function
    from __future__ import absolute_import
    from __future__ import division

    import compas
    import compas_rhino

    from compas.datastructures import Mesh
    from compas.geometry import smooth_centroid_cpp

    from compas_rhino.helpers import MeshArtist

    kmax = 50

    # make a mesh
    # and set the default vertex and edge attributes

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    edges = list(mesh.edges())

    # extract numerical data from the datastructure

    vertices  = mesh.get_vertices_attributes(('x', 'y', 'z'))
    adjacency = [mesh.vertex_neighbours(key) for key in mesh.vertices()]
    fixed     = [int(mesh.vertex_degree(key) == 2) for key in mesh.vertices()]

    # make an artist for dynamic visualization
    # and define a callback function
    # for drawing the intermediate configurations
    # and for changing the boundary conditions during the iterations

    slider = 30  # this is the top left corner

    artist = MeshArtist(mesh, layer='SmoothMesh')

    artist.clear_layer()


    def callback(k, xyz):
        compas_rhino.wait()

        print(k)

        if k < kmax - 1:
            xyz[slider][0] = 0.1 * (k + 1)

        artist.clear_edges()
        artist.draw_edges()
        artist.redraw()

        for key, attr in mesh.vertices(True):
            attr['x'] = xyz[key][0]
            attr['y'] = xyz[key][1]
            attr['z'] = xyz[key][2]


    xyz = smooth_centroid_cpp(vertices, adjacency, fixed, kmax=kmax, callback=callback)

    for key, attr in mesh.vertices(True):
        attr['x'] = xyz[key][0]
        attr['y'] = xyz[key][1]
        attr['z'] = xyz[key][2]

    artist.clear_edges()
    artist.draw_vertices()
    artist.draw_edges()
    artist.redraw()
