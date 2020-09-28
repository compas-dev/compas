***********
Grasshopper
***********

To get COMPAS working in Grasshopper, you first have to install COMPAS for Rhino.
In Grasshopper, COMPAS is imported from within a GhPython component. Rhino for
Mac and Rhino 6+ all come with their own GhPython interpreter, but if you use
Rhino 5 on Windows, please download and install GhPython `here <https://www.food4rhino.com/app/ghpython>`_.

Verify setup
============

To verify that everything is working properly, simply create a GhPython
component on your Grasshopper canvas, paste the following script and hit `OK`.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_ghpython.artists import MeshArtist

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    a = MeshArtist(mesh).draw()


.. figure:: /_images/gh_verify.jpg
     :figclass: figure
     :class: figure-img img-fluid


Reloading changed libraries
===========================

If you change a Python library during a running Rhino application, which is
imported in a GhPython component (e.g. via ``import compas_fab``),
it is necessary to reload the library so that the GhPython interpreter
recognizes the changes. To avoid restarting Rhino, you can use the function
``unload_modules``. The following example reloads the library ``compas_fab``.

.. code-block:: python

    from compas_ghpython import unload_modules

    unload_modules('compas_fab')

