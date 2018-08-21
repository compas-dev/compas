********************************************************************************
Environments
********************************************************************************

Working in Rhino
================

.. note::

    We are working on an automated version of the steps described in this section.
    Should be available soon...


IronPython
----------

Rhino uses IronPython to interpret your Python scripts.
It ships with its own version of IronPython, and in Rhino 5 this bundled version is a beta version.
You should install your own version of IronPython such that everything works properly.

.. note::

    Install `IronPython 2.7.5 <https://github.com/IronLanguages/main/releases/tag/ipy-2.7.5>`_,
    and not the latest version of IronPython.
    Rhino doesn't like it...


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



