.. _gs-blender:

*******************************************************************************
Blender
*******************************************************************************

Blender ships with its own embedded version of Python. Therefore, the simplest
(and recommended) way to install COMPAS for Blender is to replace the embedded
Python by the Python of a `conda` environment that already has COMPAS installed.

It is important that the version of Python installed in the `conda` environment matches
the version of Python that was originally shipped with Blender. For Blender 2.9x
this is Python 3.7x.

Installation
============

.. raw:: html

    <div class="card">
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item">
                    <a class="nav-link active" data-toggle="tab" href="#replace_python_windows">Windows</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#replace_python_osx">OSX</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#replace_python_linux">Linux</a>
                </li>
            </ul>
        </div>
        <div class="card-body">
            <div class="tab-content">

.. raw:: html

    <div class="tab-pane active" id="replace_python_windows">

If you wish to install a new python environment with COMPAS, open the command prompt and type the following:

.. code-block:: bash

    conda config --add channels conda-forge
    conda create -n blender python=3.7 COMPAS

Now configure Blender to use the newly installed environment or any environment in which you have COMPAS:

.. code-block:: bash

    conda activate blender
    python -m compas_blender.install "%PROGRAMFILES%\\Blender Foundation\\Blender 2.91\\2.91"

Note that the path ``%PROGRAMFILES%\\Blender Foundation\\Blender 2.91\\2.91`` might be different
if you have another version of Blender intalled.
Check your version of Blender and change the path accordingly.

.. raw:: html

    </div>
    <div class="tab-pane" id="replace_python_osx">

If you wish to install a new python environment with COMPAS, open the Terminal and type the following:

.. code-block:: bash

    conda config --add channels conda-forge
    conda create -n blender python=3.7 COMPAS

Now configure Blender to use the newly installed environment or any environment in which you have COMPAS:

.. code-block:: bash

    conda activate blender
    python -m compas_blender.install /Applications/blender.app/Contents/Resources/2.91

Note that the path ``/Applications/blender.app/Contents/Resources/2.91`` might be different
if you have another version of Blender intalled.
Check your version of Blender and change the path accordingly.

.. raw:: html

    </div>
    <div class="tab-pane" id="replace_python_linux">

If you wish to install a new python environment with COMPAS, open the Terminal and type the following:

.. code-block:: bash

    conda config --add channels conda-forge
    conda create -n blender python=3.7 COMPAS

Now configure Blender to use the newly installed environment or any environment in which you have COMPAS.

First, backup the original python:

.. code-block:: bash

    conda activate blender
    python -m compas_blender.install ~/Blender/2.91

Note that the path ``~/Blender/2.91`` might be different for your setup.
Check your version of Blender and change the path accordingly.

.. raw:: html

    </div>

.. raw:: html

    </div>
    </div>
    </div>


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
    if you want to use blender with a different environment, you simply have to activate that environment and floow the same procedure described above.

Start Blender
=============

Blender uses the command window of your system to display error messages and other text output.
On Windows, the output window can be brought to the front directly from the "Window" menu.
On Mac, you should start Blender from the command line.

By adding the Blender executable to the ``PATH`` variable this is really simple.
Just add the following to your ``.bash_profile``

.. code-block:: bash

    export PATH="/Applications/blender.app/Contents/MacOS:$PATH"

After that starting Blender from the command line is much simpler.

.. code-block:: bash

    blender
