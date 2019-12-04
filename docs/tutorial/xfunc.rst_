********************************************************************************
Writing XFuncs
********************************************************************************

.. note::

    In most use cases, :class:`compas.utilities.XFunc` has been superseded by
    :mod:`compas.rpc`.


Python Implementations
======================

Python (the programming language) has several implementations.
The default and most widespread implementation is CPython.

CPython is implemented in C.
The CPython interpreter compiles your Python source code into bytecodes, and then
executes the bytecodes to run your program.
It is therfore, very easy to write C-extensions for CPython code, because in the end
it is executed by a C interpreter.

Other implementations are, for example, Jython and IronPython.
Jython is implemented in Java; the Jython intepreter compiles Python code to Java
bytecode and runs it on the Java Virtual Machine.
IronPython is written in C# and runs on the .NET DLR (Dynamic Language Runtime).

The advantage of imlementations such as Jython or IronPython is that they can use Python
libraries but also provide access to the capabilities of their respective ecosystems;
In Jython you can import and use any Java classes from within your Jython code.
IronPython can use the .NET framework.


.. code-block:: python

    # Jython

    import sys
    import os

    from java.util import Random
    from java.awt import Color

    from jarray import zeros

    from javax.swing import JLabel
    from javax.vecmath import Point2f

    # ...


.. code-block:: python

    # IronPython

    import sys
    import os

    from System.Windows.Forms import PictureBox
    from System.Windows.Forms import PictureBoxSizeMode
    from System.Windows.Forms import DockStyle

    from System.Drawing import Image

    from System.Net import WebClient

    from System.IO import MemoryStream

    # ...


The downside is that many of the Python packages that are interesting for Computational
Science and Engineering are only available for CPython.


RhinoPython
===========

In Rhino, Python scripts are executed by an IronPython interpreter.
This means that from your Python scripts, in addition to RhinoCommon, you have
direct access to the .NET, but you can't use Numpy, Scipy, Pandas, Shapely, Cython,
Plnarity, Matplotlib, NetworkX, and many other interesting packages.

.. code-block:: python

    # yes

    import os
    import sys

    import rhinoscriptsyntax as rs
    import sciptcontext as sc

    from Rhino.Geometry import Point3d
    from Rhino.UI import MouseCallback

    from System.Windows.Forms import Form
    from System.Drawing import Color

.. code-block:: python

    # no

    from numpy import array
    from scipy.linalg import solve
    from shapely.geometry import Polygon

    import matplotlib.pyplot as plt


As a result, none of the COMPAS algorithms relying on these packages can be used
directly in Rhino.

.. code-block:: python

    # yes

    import compas

    from compas.datastructures import Mesh
    from compas.datastructures import mesh_transform

    from compas.numerical import dr
    from compas.geometry import bounding_box


.. code-block:: python

    # no

    import compas

    from compas.datastructures import Mesh
    from compas.datastructures import mesh_transform_numpy

    from compas.numerical import dr_numpy
    from compas.geometry import bounding_box_numpy


External Functions
==================

To overcome this limitation, COMPAS provides a mechanism for calling Python functions
through a separately launched subprocess.


.. code-block:: python

    from compas.utilities import XFunc

    dr_numpy = XFunc('compas.numerical.dr_numpy')


.. note::

    On Rhino for Mac, the version of subprocess shipped with IronPython is broken.
    Therefore, you have to use :class:`compas_rhino.utilities.XFunc` instead.
    This version obviously also works in Rhino for Windows.


Limitations
-----------

The input and output of XFuncs have to be native Python objects.
If the wrapped function returns Numpy arrays, these will be converted automatically
to lists.

.. code-block:: python

    # yes

    from compas.utilities import XFunc

    bounding_box_numpy = XFunc('compas.geometry.bounding_box_numpy')


.. code-block:: python

    # no

    from compas.utilities import XFunc

    mesh_transform_numpy = XFunc('compas.datastructures.mesh_transform_numpy')


The latter example will not work because the function :func:`compas.datastructures.mesh_transform_numpy`
expects a :class:`compas.datastructures.Mesh` as its first argument, which is not
a native Python object.

Using callbacks with XFuncs will currently also not work.


Error handling
--------------

Any errors thrown by the wrapped functions will be caught by the Xfunc and re-raised
together with a traceback to allow for proper debugging.


Code profiles
-------------

The execution of the wrapped function in the subprocess is automatically profiled
and a printout of the profile is available as an attribute of the XFunc.

.. code-block:: python

    from compas.utilities import XFunc

    dr_numpy = XFunc('compas.numerical.dr_numpy')

    # some preprocessing

    result = dr_numpy(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius)

    print dr_numpy.profile


Examples
========

Basic usage
-----------


Usage with data structures
--------------------------

