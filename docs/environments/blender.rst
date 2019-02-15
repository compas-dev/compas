********************************************************************************
Working in Blender
********************************************************************************

Blender ships with its own embedded version of Python but it is relatively
simple to replace it with the one you have COMPAS installed on.

.. note::

    The following instructions are for Blender 2.79 which ships with
    **Pyhton 3.5.3**, for other versions, update the python version accordingly.

.. warning::

    We currently do not yet support Blender 2.8 with any of the released versions
    of COMPAS. There is, however, a feature branch with some support for Blender
    2.8 available directly from the Github repo.


Replace Python
==============

It is recommended to create a new ``conda`` environment to make sure the python
version matches exactly what Blender expects.


**On Windows**

Open the command prompt and type the following to install a new python
environment with COMPAS:

.. code-block:: bash

    $ conda config --add channels conda-forge
    $ conda create -n blender-279 python=3.5.3 COMPAS
    $ activate blender-279


Now configure Blender to use the newly installed environment:

.. code-block:: bash

    $ cd %PROGRAMFILES%\Blender Foundation\Blender\2.79
    $ ren python original_python
    $ mklink /j python %CONDA_PREFIX%


**On Mac**

Open the Terminal and type the following to install a new python
environment with COMPAS:

.. code-block:: bash

    $ conda config --add channels conda-forge
    $ conda create -n blender-279 python=3.5.3 COMPAS
    $ source activate blender-279


Now configure Blender to use the newly installed environment:

.. code-block:: bash

    $ cd /Applications/blender.app/Contents/Resources/2.79
    $ mv python original_python
    $ ln -s $CONDA_PREFIX python


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

**On Windows**

.. code-block:: bash

    $ activate blender-279
    $ conda install ...


**On Mac**

.. code-block:: bash

    $ source activate blender-279
    $ conda install ...


Miscellaneous
=============

For whatever reason, on Mac, the info bar that usually displays text output and
and error and info messages, will not produce any output of scripts.
To see the output of scripts, you have to start Blender from the Terminal such that
the output can be directed there...

To avoid having to navigate to the Blender executable evey time you want to do this,
you could add the path to the executable to your system ``PATH`` variable.
In your ``~/.bash_profile`` add the following.


.. code-block:: bash

    export PATH="/Applications/blender.app/Contents/MacOS:$PATH"


After that starting Blender from the command line is much simpler.


.. code-block:: bash

    $ blender


And all output from the scripts you run will appear in the Terminal window...
