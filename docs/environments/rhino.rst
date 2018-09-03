********************************************************************************
Working in Rhino
********************************************************************************

.. warning::

    All instructions on this page are for Rhino for Windows.
    The instructions for Rhinomac are coming soon...


*Installing* **COMPAS** for Rhino is very simple. Just open the *command prompt*
and type the following

::

    $ python -m compas_rhino.install


Optionally, you could provide a Rhino version number (``'5.0', '6.0'``).
The default is ``'5.0'``.

::

    $ python -m compas_rhino.install '6.0'



IronPython
==========

If you are using Rhino 5.0, you may also want to *replace* the version of IronPython
that comes with it, such that everything works properly.

To check your IronPython version in Rhino, go to the PythonScript Editor

::

    Tools > PythonScript > Edit


.. figure:: /_images/rhino_scripteditor.*
     :figclass: figure
     :class: figure-img img-fluid


There, run the following snippet.

.. code-block:: python

    import sys
    print sys.version_info


This will display something like

::

    sys.version_info(major=2, minor=7, micro=5, releaselevel='final', serial=0)


If the ``releaselevel`` is not ``'final'``,
install `IronPython 2.7.5 <https://github.com/IronLanguages/main/releases/tag/ipy-2.7.5>`_
and let Rhino know where it is by adding it to the Rhino Python Editor search paths.

.. note::

    Install `IronPython 2.7.5 <https://github.com/IronLanguages/main/releases/tag/ipy-2.7.5>`_,
    and not the latest version of IronPython.
    Rhino doesn't like it...


In the Rhino Python Editor, go to

::

    Tools > Options


And add

::

    C:\path\to\IronPython275
    C:\path\to\IronPython275\Lib
    C:\path\to\IronPython275\DLLs


.. note::

    Restart Rhino and check the version info as before.


Using the built-in script editor
================================


Using an external editor
========================
