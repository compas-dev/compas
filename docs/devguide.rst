===============
Developer Guide
===============

This guide is intended for people who want to contribute to the code and documentation
of the core COMPAS packages:

* :mod:`compas`
* :mod:`compas_blender`
* :mod:`compas_ghpython`
* :mod:`compas_plotters`
* :mod:`compas_rhino`

Note, however, that the general procedure is applicable to all COMPAS package development.

Setup/Installation
==================

To set up a developer environment

1. Fork `the repository <https://github.com/compas-dev/compas>`_ and clone the fork.
2. Create a virtual environment using your tool of choice (e.g. `virtualenv`, `conda`, etc).

.. code-block:: bash

    conda create -n compas-dev python=3.7
    conda activate compas-dev

3. Install development dependencies:

.. code-block:: bash

    cd path/to/compas
    pip install -r requirements-dev.txt

4. Make sure all tests pass:

.. code-block:: bash

    invoke test

5. Create a branch for your contributions.

.. code-block::

    git branch title-proposed-changes
    git checkout title-proposed-changes

6. Start making changes!


Submitting a PR
===============

Once you are done making changes, you have to submit your contribution through a pull request (PR).
The procedure for submitting a PR is the following.

1. Make sure all tests still pass:

.. code-block:: bash

    invoke test

2. Add yourself to ``AUTHORS.md``.
3. Commit your changes and push your branch to GitHub.
4. Create a `pull request <https://help.github.com/articles/about-pull-requests/>`_ through the GitHub website.

During development, use `pyinvoke <http://docs.pyinvoke.org/>`_ tasks on the
command line to ease recurring operations:

* ``invoke clean``: Clean all generated artifacts.
* ``invoke check``: Run various code and documentation style checks.
* ``invoke docs``: Generate documentation.
* ``invoke test``: Run all tests and checks in one swift command.


Style guide
===========

* PEP 8
* flake8
* naming conventions
* consistency
* foolish consistency
* principle of least astonishment


Documentation
=============

* sphinx
* RestructuredText
* docs structure
* api docs
  * napoleon
  * Numpy-style
* examples
* references
* see also

Code structure
==============

Each of the core packages is divided into subpackages that group functionality into logical components.
For example, :mod:`compas` is divided into:

* :mod:`compas.datastructures`
* :mod:`compas.files`
* :mod:`compas.geometry`

The API of each subpackage is documented in the docstring of its ``__init__.py`` file using basic RestructuredText.
From outside of these packages, functionality should be imported directly from the subpackage level,
regardless of the code structure underneath.

For example, in some ``script.py``:

.. code-block:: python

    from compas.geometry import add_vectors
    from compas.geometry import oriented_bounding_box_numpy
    from compas.geometry import Polygon
    from compas.geometry import Transformation

    from compas.numerical

To allow the public API of the modules and packages contained in a subpackage to reach the subpackage level,
each module should declare the classes, functions and variables of its public API in the module's ``__all__`` variable.
Per package, the APIs of the contained module are collected in ``__all__`` variable of the package (in the ``__init__.py``).

.. code-block:: python

    __all__ = [_ for _ in dir() if not _.startswith('_')]


.. _plugins:

Plugins
=======

COMPAS has an extensible architecture based on plugins that allows to
customize and extend the functionality of the core framework.

For a plugin to work, there needs to exist a counterpart to be connected to.
This means there are two components involved:

* :meth:`compas.plugins.pluggable` interface: the *extension point* that COMPAS defines
  as the counterpart for plugins to connect to.
* :meth:`compas.plugins.plugin` implementation: a *concrete implementation* of the
  ``pluggable`` interface.

Both of these components are declared using decorators:

.. code-block:: python

    @pluggable
    def do_hard_stuff(input):
        pass

    @plugin(pluggable_name='do_hard_stuff')
    def do_hard_stuff_numpy(input):
        # NOTE: Here use the power of numpy to do hard stuff very fast
        # ..

Once these parts are implemented, the program could simply
call the function ``do_hard_stuff`` and the appropriate plugin
implementation using ``numpy`` would be called automatically.

Why are plugins important?
--------------------------

The example above is just a single code block, but the power of plugins comes
from the ability to split those two parts -the :meth:`compas.plugins.pluggable`
and the :meth:`compas.plugins.plugin`- into completely different files, folders
or even entire projects and still work the same way.

Additionally, COMPAS is able to pick the most suitable plugin implementation
for its current execution context. For instance, one could have two implementations
of the same :meth:`compas.plugins.pluggable` definition, one using ``numpy`` and
another one using *Rhino SDK* and have the correct one automatically selected
based on where your script is executing.

How to make plugins discoverable?
---------------------------------

COMPAS plugin discovery is based on naming conventions. This is mainly due to
the need to support IronPython inside Rhino, which lacks ``setuptools``
infrastructure. For more details, check
`these python guidelines <https://packaging.python.org/guides/creating-and-discovering-plugins/#using-naming-convention>`_.

A COMPAS plugin needs to fulfill two conditions:

* **Name**: The package name should be prefixed with ``compas``, eg. ``compas_cgal``.
* **Metadata**: The package should define a bit of metadata listing the modules that contain plugins.
  This is done declaring a variable called ``__all_plugins__``,
  eg. ``__all_plugins__ = ['compas_cgal.booleans']``.

COMPAS automatically discovers plugins searching over all available packages in the system,
and picks up those prefixed with the ``compas`` word.
All packages are included in the search: packages installed with ``pip``, packages made
available through the ``PYTHONPATH`` / ``IRONPYTHONPATH``, local packages, etc.

Once a package is found, the metadata in ``__all_plugins__`` is read and all modules
listed are analyzed to look for functions decorated with the :meth:`compas.plugins.plugin`
decorator.

Two kinds of extension points
-----------------------------

An extension point, or *pluggable* interface can be declared as being one of two types
based on how they select which implementation to pick if there are multiple available.

* ``selector='first_match'``: this type of extension point will pick the first plugin
  implementation that satisfies the requirements.
* ``selector='collect_all'``: extension points defined with this selector will instead
  collect all plugin implementations and execute them all, collecting the return
  values into a list. An example of this is the Rhino install extension
  point: :meth:`compas_rhino.install.installable_rhino_packages`.

A complete example
------------------

Let's explore a complete example to gain a better understanding.

Extension point
^^^^^^^^^^^^^^^

For the sake of example, we are going to assume that ``compas`` core defines
the following :meth:`compas.plugins.pluggable` interface in

**compas/geometry/booleans/__init__.py**

.. code-block:: python

    @pluggable(category='booleans')
    def boolean_union_mesh_mesh(A, B):
        pass

Plugin
^^^^^^

Now let's write a plugin that implements this interface:

**compas_plugin_sample/__init__.py**

.. code-block:: python

    __all_plugins__ = ['compas_plugin_sample.boolean_trimesh']


**compas_plugin_sample/boolean_trimesh.py**

.. code-block:: python

    import trimesh

    @plugin(category='booleans', requires=['trimesh'])
    def boolean_union_mesh_mesh(A, B):
        va, fa = A
        at = trimesh.Trimesh(vertices=va, faces=fa)

        vb, fb = B
        bt = trimesh.Trimesh(vertices=vb, faces=fb)

        r = at.union(bt, engine='scad')

        return r.vertices, r.faces

Voilà! We have a trimesh-based boolean union plugin!

Advanced options
----------------

There are a few additional options that plugins can use:

* ``requires``: List of required python modules. COMPAS will filter out plugins if their
  requirements list is not satisfied at runtime. This allows to have multiple implementations
  of the same operation and have them selected based on which packages are installed.
  on the system. Eg. `requires=['scipy']`.
* ``tryfirst`` and ``trylast``: Plugins cannot control the exact priority they will have
  but they can indicate whether to try to prioritize them or demote them as fallback using
  these two boolean parameters.
* ``pluggable_name``: Usually, the name of the decorated plugin method matches that of the
  pluggable interface. When that is not the case, the pluggable name can be specified via
  this parameter.
* ``domain``: extension points are unambiguously identified by a URL that combines domain,
  category and pluggable name. All COMPAS core plugins use the same domain, but other
  packages could potentially decide to use a different domain to ensure collision-free
  naming of pluggable extension points.

While developing plugins, it is also possible to enable print output to understand what
how plugin selection works behind the scenes. To enable that, set ``DEBUG`` flag
accordingly:

.. code-block:: python

    from compas.plugins import plugin_manager
    plugin_manager.DEBUG = True

Multiple implementations
========================


Testing
=======

