********************************************************************************
Sublime Text
********************************************************************************

* `Sublime Text Official Documentation <https://www.sublimetext.com/docs/3/>`_
* `Sublime Text Unofficial Documentation <http://docs.sublimetext.info/en/latest/index.html>`_


Install Packages
================

.. note::

    To install packages in Sublime Text, first install `Package Control <https://packagecontrol.io/installation>`_.


**Highly recommended**

*   `Conda <https://packagecontrol.io/packages/Conda>`_

    *Plugin that allows users to work with conda directly within Sublime Text*

*   `SideBarEnhancements <https://packagecontrol.io/packages/SideBarEnhancements>`_

    *Provides enhancements to the operations on Sidebar of Files and Folders for Sublime Text*

*   `SublimeLinter <https://packagecontrol.io/packages/SublimeLinter>`_

    *The code linting framework for Sublime Text 3. No linters included: get them via Package Control*

*   `SublimeLinter flake8 <https://packagecontrol.io/packages/SublimeLinter-flake8>`_

    *This linter plugin for SublimeLinter provides an interface to flake8*


**Optional**

*   `GitGutter <https://packagecontrol.io/packages/GitGutter>`_

    *Plug-in to show information about files in a git repository*

*   `MarkdownPreview <https://packagecontrol.io/packages/MarkdownPreview>`_

    *Markdown preview and build plugin for Sublime Text*

*   `Terminal <https://packagecontrol.io/packages/Terminal>`_

    *Launch terminals from the current file or the root project folder*


**Even more optional**

*   `One Dark Color Scheme <https://packagecontrol.io/packages/One%20Dark%20Color%20Scheme>`_

    *A port of the One Dark color scheme from Github's Atom editor*


To install the above packages open the Command Palette,
and type ``Package Control`` to see all possible commands related to that.
Select ``Package Control: Install Package`` and hit enter.

.. code-block:: none

    Tools > Command Palette


.. figure:: /_images/sublimetext_packagecontrol.png
     :figclass: figure
     :class: figure-img img-fluid


A list with available packages will appear.
Type one of the names listed above, select the corresponding package and hit enter again.
The package will be installed automatically.
There is no need to restart Sublime Text.

.. note::

    Sublime Text is keyboard-oriented editor.
    Therefore, it is worth getting familiar with some of the keyboard shortcuts.
    One of the most import shortcuts is the one that launches the Command Palette.

    On Windows: ``Shift + Ctrl + P``. On Mac: ``Shift + Command + P``.


Run scripts
===========

To run scripts from within Sublime Text, you need to select a build system.
Please use ``Conda``:

.. code-block:: none

    Tools > Build System > Conda

To run the current script, use ``Ctrl + B`` (Windows) or ``Command + B`` (Mac).


Virtual environments
====================

If you are using ``conda`` to manage your virtual environments, and you installed
the Conda package as described above, you can do all environment management dirtectly
from Sublime Text. Simply launch the Command Palette and type ``Conda`` to see all
available options.

.. figure:: /_images/sublimetext_conda.png
     :figclass: figure
     :class: figure-img img-fluid


Choose ``Conda: Activate Environment`` and the select the environment you want to activate.
Then select ``Conda`` as the build system to use the Python installation of the
activated environment.
