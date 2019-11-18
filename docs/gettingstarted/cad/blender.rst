********************************************************************************
Blender
********************************************************************************

Blender ships with its own embedded version of Python but it is relatively
simple to replace it with the one you have COMPAS installed on.

.. note::

    The latest releases of COMPAS only support Blender 2.8. This version of Blender
    requires Python `3.7.x`.


Replace Python
==============

It is recommended to create a new ``conda`` environment to make sure the python
version matches exactly what Blender expects.

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

In Blender, you should now be able to use COMPAS packages without any problems.
Simply create and run the following script to verify everything is working properly.

.. code-block:: python

    import compas

    from compas.datastructures import Mesh
    from compas_blender.artists import MeshArtist

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    artist = MeshArtist(mesh)

    artist.draw_vertices()
    artist.draw_edges()
    artist.draw_faces()


.. figure:: /_images/blender_verify.png
     :figclass: figure
     :class: figure-img img-fluid


Install Python packages
=======================

After replacing the embedded version of Python with the one in the virutual
environment, as instructed above, it is not necessary to activate the environment
before using Blender. However, when you want to update the installed packages,
or add more packages, make sure you do it for the Python in the virtual environment.
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
