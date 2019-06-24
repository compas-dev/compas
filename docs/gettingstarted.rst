********************************************************************************
Getting started
********************************************************************************

.. highlight:: bash


Installation
============

The recommended way to install COMPAS is with `conda <https://conda.io/docs/>`_.
COMPAS is available via the ``conda-forge`` channel.

::

    $ conda config --add channels conda-forge


To install COMPAS in the current environment

::

    $ conda install COMPAS


To install a specific version of COMPAS

::

    $ conda install COMPAS=0.7.0


To install COMPAS in a separate environment

::

    $ conda create -n compas-dev COMPAS


To install COMPAS in a separate environment with a specific version of Python

::

    $ conda create -n compas-dev python=3.7 COMPAS


.. note::

    If you install COMPAS in a separate environment (recommended),
    don't forget to activate the environment when you want to use the installed functionality.

    ::

        $ conda activate compas-dev


Examples
========

Using an interactive Python interpreter:

.. code-block:: bash

    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_obj(compas.get('faces.obj'))
    >>> mesh.summary()


Using your favourite code editor or IDE:

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh)
    plotter.draw_mesh()
    plotter.show()


Using the PythonScriptEditor in Rhino:

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_rhino import MeshArtist

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    artist = MeshArtist(mesh)
    artist.draw_mesh()


Using the script editor in Blender:

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_blender import MeshArtist

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    artist = MeshArtist(mesh)
    artist.draw_mesh()


Next Steps
==========

* https://compas-dev.github.io/main/examples.html
* https://compas-dev.github.io/main/tutorial.html
* https://compas-dev.github.io/main/api.html


Get Help
========

* https://compas-dev.github.io/main/knownissues.html
* https://github.com/compas-dev/compas/issues
* https://forum.compas-framework.org/
