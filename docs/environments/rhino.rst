********************************************************************************
Working in Rhino
********************************************************************************

.. highlight:: bash


*Installing* COMPAS for Rhino is very simple.
Just type the following on the command line

::

    $ python -m compas_rhino.install


Optionally, you could provide a Rhino version number (``5.0, 6.0``).
The default is ``6.0``.

::

    $ python -m compas_rhino.install -v 6.0


.. note::

    On Windows, use the "Anaconda Prompt" instead of the "Command Prompt", and make
    sure to run it as administrator.

    On Mac, use the Terminal.

If you installed COMPAS using ``conda``, which is highly recommended, make sure
that the environment in which you installed COMPAS is active when you issue the
above commands.


IronPython
==========

If you are using Rhino 5.0, you may also want to *replace* the version of IronPython
that comes with it, such that everything works properly.

To check your IronPython version in Rhino, go to the PythonScript Editor

.. code-block:: none

    Tools > PythonScript > Edit


.. figure:: /_images/rhino_scripteditor.*
     :figclass: figure
     :class: figure-img img-fluid


There, run the following snippet.

.. code-block:: python

    import sys
    print sys.version_info


This will display something like

.. code-block:: none

    sys.version_info(major=2, minor=7, micro=5, releaselevel='final', serial=0)


If the ``releaselevel`` is not ``'final'``,
install `IronPython 2.7.5 <https://github.com/IronLanguages/main/releases/tag/ipy-2.7.5>`_
and let Rhino know where it is by adding it to the Rhino Python Editor search paths.

.. note::

    Install `IronPython 2.7.5 <https://github.com/IronLanguages/main/releases/tag/ipy-2.7.5>`_,
    and not the latest version of IronPython.
    Rhino doesn't like it...


In the Rhino Python Editor, go to

.. code-block:: none

    Tools > Options


And add

.. code-block:: none

    C:\path\to\IronPython275
    C:\path\to\IronPython275\Lib
    C:\path\to\IronPython275\DLLs


.. note::

    Restart Rhino and check the version info as before.


Install COMPAS packages
=======================

The procedure for installing a COMPAS package in Rhino is similar to installing
COMPAS itself.

.. code-block:: bash




Working with virtual environments
=================================


Installing plugins
==================


XFunc and RPC
=============

