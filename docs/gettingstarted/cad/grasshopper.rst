********************************************************************************
Grasshopper
********************************************************************************

To get COMPAS working in Grasshopper, you first have to follow the steps from
`Working in Rhino <rhino.html>`_.

In Grasshopper, COMPAS is imported from within a GhPython component. Rhino for
Mac and Rhino WIP+6 all come with their own GhPython interpreter, but if you use
Rhino 5 in Windows, please download and install GhPython `here <https://www.food4rhino.com/app/ghpython>`_.

Verify setup
============

To verify that everything is working properly, simply create a GhPython
component on your Grasshopper canvas, paste the following script and hit `OK`.

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

If you change a Python library during a running Rhino application, which is
imported in a GhPython component (e.g. via :code:`import my_custom_library`),
it is necessary to reload the library so that the GhPython interpreter
recognizes the changes. To avoid restarting Rhino, you can use the function
:code:`unload_modules`. The following example reloads the library
:code:`my_custom_library`.

.. code-block:: python

    from compas_ghpython import unload_modules

    unload_modules('my_custom_library')


Working with global sticky variables
====================================

.. TODO
    Working with global sticky variables
    https://developer.rhino3d.com/guides/rhinopython/ghpython-global-sticky/

    Passing dictionaries to another component
    my_dict = {'apples': 5, 'bananas': 7, 'pears': 3}
    my_outlet = [my_dict]


Freezing Grasshopper and workarounds
====================================

