********************************************************************************
Requirements
********************************************************************************

.. _Anaconda: https://www.continuum.io/
.. _EPD: https://www.enthought.com/products/epd/


To get the most out of **COMPAS**, we recommend installing a scientific Python
distribution such as `Anaconda`_ or `EPD`_. This will take care of most of the
(optional) dependencies listed below. However, if you prefer, most of these packages
can also be added individually to a basic Python installation using *pip*.

If you are working on Windows, many installers for packages that are not *pip installable*
can be found on Christof Gholke's page
`Unofficial Windows Binaries for Python Extension Packages <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_.
On mac, you can use a package manager like `macports <https://www.macports.org/>`_
or `homebrew <http://brew.sh/>`_.

* `Numpy <http://www.numpy.org/>`_: For all numerical calculations and algorithms.
* `Scipy <https://www.scipy.org/>`_: For all numerical calculations and algorithms.
* `Matplotlib <http://matplotlib.org/>`_: For two-dimensional visualisations.
* `PyOpenGL <http://pyopengl.sourceforge.net/>`_: For three-dimensional visualisations.
* `PySide <https://wiki.qt.io/PySide>`_: For some of the standalone tools.
* `NetworkX <https://networkx.github.io/>`_: For spring layouts of networks.
* `Planarity <https://github.com/hagberg/planarity>`_: For planarity testing.
* `Numba <http://numba.pydata.org/>`_: For just-in-time compilation.
* `PyCuda <https://mathema.tician.de/software/pycuda/>`_: For parallel computation through Nvidia's CUDA.
* `PyOpenCL <https://mathema.tician.de/software/pyopencl/>`_: For parallel computation though OpenCL.
* `Imageio <https://imageio.github.io/>`_: For reading and writing of image data.


.. rst-class:: table table-responsive table-bordered

====================== ======================== ================================
package                dependencies             exceptions
====================== ======================== ================================
compas.com             --                       matlab (``MatlabEngine``, ``MatlabSession``), paramiko (``ssh.py``)
compas.datastructures  --
compas.files           --
compas.geometry        --                       NumPy, SciPy (functions with the ``_numpy`` suffix)
compas.hpc             Numba, PyCuda, PyOpenCL
compas.interop         --
compas.numerical       NumPy, SciPy
compas.plotters        Matplotlib
compas.topology        --                       NumPy, SciPy (functions with the ``_numpy`` suffix), planarity (``network_is_planar``), NetworkX (``network_embed_in_plane``)
compas.utilities       --                       imageio (``gif_from_images``)
compas.viewers         PyOpenGL, PySide
====================== ======================== ================================
