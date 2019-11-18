********************************************************************************
Blender
********************************************************************************

Blender ships with its own embedded version of Python. Therefore, the simplest
(and recommended) way to install COMPAS for Blender is to replace the embedded
Python by the Python of a `conda` environment that already has COMPAS installed.

It is important that the version of Python installed in the `conda` environment matches
the version of Python that was originally shipped with Blender. For Blender 2.8x
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
            </ul>
        </div>
        <div class="card-body">
            <div class="tab-content">

.. raw:: html

    <div class="tab-pane active" id="replace_python_windows">

Open the command prompt and type the following to install a new python
environment with COMPAS:

.. code-block:: bash

    conda config --add channels conda-forge
    conda create -n blender python=3.7 COMPAS
    conda activate blender

Now configure Blender to use the newly installed environment:

.. code-block:: bash

    python -m compas_blender.install "%PROGRAMFILES%\Blender Foundation\Blender\2.80"

.. raw:: html

    </div>
    <div class="tab-pane" id="replace_python_osx">

Open the Terminal and type the following to install a new python
environment with COMPAS:

.. code-block:: bash

    conda config --add channels conda-forge
    conda create -n blender python=3.7 COMPAS
    conda activate blender

Now configure Blender to use the newly installed environment:

.. code-block:: bash

    python -m compas_blender.install /Applications/blender.app/Contents/Resources/2.80

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


Start Blender
=============

Both on Windows and Mac (for different reasons) Blender should be started from the command line.
By adding the Blender executable to the `PATH` variable this is really simple.

.. raw:: html

    <div class="card">
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item">
                    <a class="nav-link active" data-toggle="tab" href="#blender_start_windows">Windows</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#blender_start_osx">OSX</a>
                </li>
            </ul>
        </div>
        <div class="card-body">
            <div class="tab-content">

.. raw:: html

    <div class="tab-pane active" id="blender_start_windows">

Add the path to the Blender executable to your PATH in Environment Variables.

.. code-block::

    %PROGRAMFILES%\Blender Foundation\Blender

.. raw:: html

    </div>
    <div class="tab-pane" id="blender_start_osx">

Add the following to your .bash_profile

.. code-block:: bash

    export PATH="/Applications/blender.app/Contents/MacOS:$PATH"

.. raw:: html

    </div>

.. raw:: html

    </div>
    </div>
    </div>

After that starting Blender from the command line is much simpler.

.. code-block:: bash

    blender
