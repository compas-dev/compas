********************************************************************************
CPython in Rhino
********************************************************************************

Rhino runs Python scripts using IronPython 2.7.
This is great because it provides access to the .NET framework.
However, this also means that many (C)Python libraries are not available.
For example Numpy, Scipy, Matplotlib, SimPy, Numba, NetworkX, CVXPY, Shapely, PyOpenGL, PySide, ...

.. code-block:: python

    # IronPython provides access to the .NET framework

    import System

    import clr
    clr.AddReference("System.Windows.Forms.DataVisualization")

    from System.Windows.Forms.DataVisualization import Charting
    from System.Windows.Forms import WebBrowser
    from System.Windows.Forms import TextBox

    from System.Drawing import Size
    from System.Drawing import Point
    from System.Drawing import Color
    from System.Drawing import Image

    from System.Net import WebClient
    from System.IO import MemoryStream

    # ...


With `compas.utilities.XFunc` this limitation can be partly removed.
Below is an example from the API reference.

.. code-block:: python

    import compas
    import compas_rhino

    from compas.datastructures import Mesh
    from compas.utilities import XFunc
    from compas_rhino.artists import MeshArtist


    # importing fd_numpy directly does not work
    # because Numpy & Scipy are not available for IronPython
    # however we can construct an *XFunc* to replace the original function

    fd = XFunc('compas.numerical.fd.fd_numpy.fd_numpy')


    mesh = Mesh.from_obj(compas.get('faces.obj'))

    vertices = mesh.get_vertices_attributes('xyz')
    edges    = list(mesh.edges())
    fixed    = list(mesh.vertices_where({'vertex_degree': 2}))
    q        = mesh.get_edges_attribute('q', 1.0)
    loads    = mesh.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))


    # the *XFunc* can be called in the same way as the original

    xyz, q, f, l, r = fd(vertices, edges, fixed, q, loads)


    # update the mesh
    # and display the result

    for key, attr in mesh.vertices(True):
        attr['x'] = xyz[key][0]
        attr['y'] = xyz[key][1]
        attr['z'] = xyz[key][2]

    artist = MeshArtist(mesh)

    artist.clear()

    artist.draw_vertices()
    artist.draw_edges()

    artist.redraw()

