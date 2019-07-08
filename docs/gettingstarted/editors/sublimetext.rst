********************************************************************************
Sublime Text
********************************************************************************

Install Package Control
=======================

To install packages in Sublime Text, first install Package Control (https://packagecontrol.io/installation).


Install Packages
================

Packages are installed using Package Control.
Open the Command Palette and type "Package Control" to see all related commands.
Select ``Package Control: Install Package``.

To open the Command Palette, hit key combination ``SHIFT + CTRL + P`` (on Windows) or ``SHIFT + COMMAND + P`` (on Mac).

.. figure:: /_images/sublimetext_packagecontrol.png
     :figclass: figure
     :class: figure-img img-fluid


A list with available packages will appear.
Select a package and it will be installed automatically.
There is no need to restart Sublime Text.

*   **Conda** Work with conda environments directly in Sublime Text. (https://packagecontrol.io/packages/Conda)
*   **SideBarEnhancements** Provides enhancements for the sidebar and operations on files and folders. (https://packagecontrol.io/packages/SideBarEnhancements)
*   **SublimeLinter** Code linting framework for Sublime Text 3. No linters included: get them via Package Control. (https://packagecontrol.io/packages/SublimeLinter)
*   **SublimeLinter flake8** Plugin for SublimeLinter that provides interface to flake8. (https://packagecontrol.io/packages/SublimeLinter-flake8)


Run scripts
===========

To run scripts from within Sublime Text, you need to select a build system.
Please use ``Conda``:

::

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

