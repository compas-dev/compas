.. _gs-blender:

*******************************************************************************
Blender
*******************************************************************************

Blender ships with its own embedded version of Python. Therefore, the simplest
(and recommended) way to install COMPAS for Blender is to replace the embedded
Python by the Python of a ``conda`` environment that already has COMPAS installed.

It is important that the version of Python installed in the ``conda`` environment matches
the version of Python that was originally shipped with Blender. For Blender 2.83 LTS
the version of the bundled Python is 3.7, and for 2.93 LTS it is 3.9.

.. note::

    On windows, the standard installation procedure recently stopped working.
    For an alternative procedure see `Installation on Windows`_.


Installation
============

These instructions are for the latest Blender 2.93 LTS which ships with Python 3.9
If you don't have an environment yet with Python 3.9 and COMPAS you can create one with ``conda``.

.. code-block:: bash

    conda create -n blender -c conda-forge python=3.9 compas --yes

Configuring Blender to use the newly installed environment is slightly different per OS.

.. tabs::

    .. tab-item:: Windows
        :active:

        .. code-block:: bash

            conda activate blender
            python -m compas_blender.install -v 2.93

        Note that the path ``%PROGRAMFILES%\\Blender Foundation\\Blender 2.93\\2.93`` might be different on your system.
        Check your Blender installation and change the path accordingly.

    .. tab-item:: OSX

        .. code-block:: bash

            conda activate blender
            python -m compas_blender.install /Applications/blender.app/Contents/Resources/2.93

        Note that the path ``/Applications/blender.app/Contents/Resources/2.93`` might be different on your system.
        Check your Blender installation and change the path accordingly.

    .. tab-item:: Linux

        .. code-block:: bash

            conda activate blender
            python -m compas_blender.install ~/Blender/2.93

        Note that the path ``~/Blender/2.93`` might be different on your system.
        Check your Blender installation and change the path accordingly.


On Windows and OSX, if Blender is installed in the default location, you can simply provide the version number.

.. code-block:: bash

    conda activate blender
    python -m compas_blender.install -v 2.93


Verify setup
============

In Blender, at the interactive Python prompt (>>>) import the following packages

.. code-block:: python

    >>> import compas
    >>> import compas_blender
    >>> import numpy
    >>> import scipy


Install Python packages
=======================

After replacing the embedded version of Python with the one in the virutual
environment, as instructed above, it is not necessary to activate the environment
before using Blender. However, when you want to update the installed packages,
or add more packages, make sure to activate the Blender environment first.
Otherwise, the changes will not have any effect.

.. code-block:: bash

    conda activate blender
    conda install ...

.. note::

    If you want to use blender with a different environment,
    you simply have to activate that environment and follow the same procedure described above.


Add-ons
=======

For some Blender add-ons, not only the version of Python has to match, but also the version of Numpy.
For example, `Sverchok <http://nortikin.github.io/sverchok/>`_, a Grasshopper-type visual programming tool for Blender,
will not work with the version of Numpy included in the latest COMPAS releases, even though Blender will.

In those cases, you can simply revert to an earlier version of Numpy that is still compatible with COMPAS
in the environment you use with Blender. For Sverchok, this would be version ``1.17.5``,
which is the one shipped with Blender originally. To revert simply do

.. code-block:: bash

    conda activate blender
    conda install numpy=1.17.5


Start Blender
=============

Blender uses the command window of your system to display error messages and other text output.
On Windows, the output window can be brought to the front directly from the "Window" menu.
On Mac or Linux, you should start Blender from the command line.

By adding the Blender executable to the ``PATH`` variable this is really simple.
Just add the following to your ``.bash_profile`` or ``.bashrc``.

.. tabs::

    .. tab-item:: OSX
        :active:

        .. code-block:: bash

            export PATH="/Applications/blender.app/Contents/MacOS:$PATH"

    .. tab-item:: Linux

        .. code-block:: bash

            export PATH="~/Blender/2.83:$PATH"

            Note that this path might be different on your system.


After that starting Blender from the command line is much simpler.

.. code-block:: bash

    blender


Known Issues
============

On Windows, Blender sometimes has issues with finding NumPy libraries.
If this is the case, the problem can usually be solved by reinstalling NumPy in your environment using ``pip``.
However, to avoid issues with other packages that were already installed and depend on a specific version of NumPy,
you should install the same version as the one installed originally by ``conda``.

.. code-block:: bash

    python -c "import numpy; print(numpy.__version__)"

If the above is, for example, ``1.20.3``

.. code-block:: bash

    pip install --force-reinstall numpy==1.20.3

Alternatively, you can create a new environment and simply install entire COMPAS using ``pip``.

.. code-block:: bash

    conda create -n blender python=3.9 cython planarity --yes
    conda activate blender
    pip install compas
    python -m compas_blender.install


Installation on Windows
=======================

On Windows, the procedure described above no longer works.
However, an alternative procedure is still possible.
Note that since this procedure is based on installing COMPAS directly using the `python` and `pip` executables shipped with Blender,
it is limited to packages that can be installed from the Python Package Index (PyPI).

The basic command will install `compas` and `compas_blender` (and `compas_rhino` and `compas_ghpython`) for the default version of Blender (2.93),
if that version can be found in the default installation location.

.. code-block:: bash

    python -m compas_blender.install_windows

Install for a different version.

.. code-block:: bash

    python -m compas_blender.install_windows -v 3.1

Install additional packages.

.. code-block:: bash

    python -m compas_blender.install_windows -p compas_cloud

Install with `pip` configuration options.

.. code-block:: bash

    python -m compas_blender.install_windows --force-reinstall --no-deps
