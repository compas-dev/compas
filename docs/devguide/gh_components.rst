**********************
Grasshopper Components
**********************

Grasshopper user objects need to be built using `COMPAS Github Action componentizer <https://github.com/compas-dev/compas-actions.ghpython_components>`_.

1. Apply your changes to the component source code (``src/compas_ghpython/components``).
2. Rebuild them:

   .. code-block:: bash

        invoke build-ghuser-components

3. Install them on Rhino/Grasshopper as usual:

   .. code-block:: bash

        python -m compas_rhino.install

The install step does not copy them, but creates a symlink to the location in which they are built,
so after the first installation, it is usually not required to reinstall them, only rebuild them (unless a new component is added).

.. note::

    This step requires IronPython version 2.7 to be available on the system.  The default behavior is to run the command
    ``ipy``.  If this command is not available or is the wrong version, the optional ``ironpython`` argument will replace it, eg
    ``invoke build-ghuser-components --ironpython="mono path/to/ipy.exe"``.

.. _plugins:
