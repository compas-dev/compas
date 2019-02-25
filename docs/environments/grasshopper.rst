********************************************************************************
Working in Grasshopper
********************************************************************************

To get COMPAS working in Grasshopper, you first have to follow the steps from
`Working in Rhino <rhino.html>`_. 

In Grasshopper, COMPAS is imported from within a GhPython component. Rhino for 
Mac and Rhino WIP+6 all come with their own GhPython interpreter, but if you use
Rhino 5 in Windows, please download and install GhPython from `here <https://www.food4rhino.com/app/ghpython>`_.

Verify setup
============

To verify that everything is working properly, simply create a GhPython 
component on your Grasshopper canvas and paste following script:

.. code-block:: python

    import compas

    from compas.datastructures import Mesh
    from compas_ghpython.artists import MeshArtist

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    artist = MeshArtist(mesh)

    a = artist.draw()


.. figure:: /_images/gh_verify.jpg
     :figclass: figure
     :class: figure-img img-fluid


Reloading changed libraries
===========================

To refresh a changed python library, run the following code from any GhPython
component on your canvas:

.. code-block:: python
    from compas_ghpython import unload_modules

    unload_modules('compas')


Differences to working in the Rhino PythonScript Editor
=======================================================


Freezing Grasshopper and workarounds
====================================
