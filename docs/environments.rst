********************************************************************************
Environments
********************************************************************************

.. warning::

    Under construction...


The core functionality of **COMPAS** is completely independent of CAD tools and
can be used from the terminal, in standalone scripts, apps, or with the plotters 
and viewers that are shipped with the main library.

In addition, **COMPAS** can be easily used in CAD software using the corresponding
CAD packages. Currently, Rhino, Blender, and Grasshopper are supported.
The Blender Python API is based on CPython. **COMPAS** is thus (almost) natively
supported. Rhino and Grasshopper, on the other hand, are based on DotNet and IronPython.
Therefore, even though most of **COMPAS** is compatible with IronPython,
a few more configuration steps are required to get started there.


.. probably we will end up having the same instructions for all CAD environments
.. because they all ship with their own version of Python
.. and need to be made aware of the locally installed site packages
.. and thus of Python
.. Rhino requires the additional explanation of XFuncs
.. Grasshopper of its typical quirks


Working in Rhino
================

IronPython
----------

Unfortunately, Rhino 5 ships with a beta version of IronPython, which results in
a few errors here and there. We recommend that you install your own version of
IronPython such that everything works properly.

To check your IronPython version in Rhino, go to the PythonScript Editor::

    Tools > PythonScript > Edit


.. figure:: /_images/rhino_scripteditor.*
     :figclass: figure
     :class: figure-img img-fluid


There, run the following snippet.

.. code-block:: python

    import sys
    print sys.version_info


This will display something like::

    sys.version_info(major=2, minor=7, micro=5, releaselevel='final', serial=0)


If the ``releaselevel`` is not ``'final'``,
install `IronPython 2.7.5 <https://github.com/IronLanguages/main/releases/tag/ipy-2.7.5>`_
and let Rhino know where it is by adding it to the Rhino Python Editor search paths.

.. note::

    Install `IronPython 2.7.5 <https://github.com/IronLanguages/main/releases/tag/ipy-2.7.5>`_,
    and not the latest version of IronPython.
    Rhino doesn't like it...


In the Rhino Python Editor, go to::

    Tools > Options


And add::

    C:\path\to\IronPython275
    C:\path\to\IronPython275\Lib
    C:\path\to\IronPython275\DLLs


.. note::

    Restart Rhino and check the version info as before.


COMPAS
------

Rhino has its own environment settings.
Therefore, you will have to tell Rhino where to find ``compas`` as well.
In the Rhino Python Editor, go to::

    Tools > Options


and add the path to ``compas``.

.. figure:: /_images/rhino_compaspath.*
     :figclass: figure
     :class: figure-img img-fluid


Restart Rhino and un the following script in the PythonScript editor to see if everything works.
There should obviously not be any errors, and the script should generate a mesh
the shape of a droplet.

.. code-block:: python

    import compas
    import compas_rhino

    from compas.datastructures import Mesh
    from compas.topology import mesh_subdivide
    from compas_rhino.artists import MeshArtist

    mesh = Mesh.from_polyhedron(6)
    subd = mesh_subdivide(mesh, scheme='catmullclark', k=3, fixed=[mesh.get_any_vertex()])

    artist = MeshArtist(subd)

    artist.draw_faces(join_faces=True)


Working in Blender
==================

*under construction*



