********************************************************************************
Working in Blender
********************************************************************************

Blender ships with its own embedded version of Python but it is relatively
simple to replace it with the one you have **COMPAS** installed on.

It is recommended to create a new ``conda`` environment to make sure the python
version matches exactly what Blender expects.

The following instructions are for Blender 2.79 which ships with
**Pyhton 3.5.3**, for other versions, update the python version accordingly.

Open the command prompt and type the following to install a new python
environment with **COMPAS**:

::

    $ conda create -n blender-279 python=3.5.3
    $ activate blender-279
    $ conda config --add channels conda-forge
    $ conda install COMPAS


On Windows
==========

Now configure Blender to use the newly installed environment:

::

    $ cd %PROGRAMFILES%\Blender Foundation\Blender\2.79
    $ ren python original_python
    $ mklink /j python %CONDA_PREFIX%


On Mac
======

.. warning::

    Under construction...
