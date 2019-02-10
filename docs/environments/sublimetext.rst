********************************************************************************
Working in Sublime Text
********************************************************************************

* `Sublime Text Official Documentation <https://www.sublimetext.com/docs/3/>`_
* `Sublime Text Unofficial Documentation <http://docs.sublimetext.info/en/latest/index.html>`_


Install Packages
================

.. note::

    To install packages in Sublime Text, first install `Package Control <https://packagecontrol.io/installation>`_.


**Highly recommended**

* Conda
* SideBarEnhancements
* SublimeLinter
* SublimeLinter-flake8

**Optional**

* GitGutter
* MarkdownPreview
* One Dark Color Scheme
* requirementstxt
* Terminal


To install the above packages go to

.. code-block:: none

    Tools > Command Palette


.. note::

    Sublime Text is keyboard-oriented editor.
    It is really worth getting familiar with some of the keyboard shortcuts.
    One of the most import shortcuts is the one that launches the Command Palette.

    On Windows: ``Shift + Control + P``

    On Mac: ``Shift + Command + P``


and then type ``install``.
One of the first entries in the dropdown will be ``Package Control: Install Package``.
Select it and hit enter.

A list with available packages will appear.
Type one of the names listed above, select the corresponding package and hit enter.


Run scripts
===========

To run Python scripts from within Sublime Text, you need to (define and) select
a build system. There should be a default Python builder available. This default
builder will use whatever system-wide Python it can find.

To define a build system with a Python version of your choosing, do

.. code-block:: none

    Tools > Build System > New Build System

This will open a new ``untitled.sublime-build`` file with the following snippet

.. code-block:: javascript

    {
        "shell_cmd" : "make"
    }

Change this to

.. code-block:: javascript

    {
        "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
        "selector": "source.python",
        "shell_cmd": "\"python\" -u \"$file\""
    }

Specify whatever Python you want to use.
You can use a system-wide Python excutable, or specify the absolute path to a specific one.

Save the file and use as filename whatever name you want to give the builder.

For example,

.. code-block:: none

    Anaconda.sublime-build


Virtual environments
====================

If you are using ``conda`` to manage your virtual environments, and you installed
the Conda package as described above, you can do all environment management dirtectly
from Sublime Text. Simply launch the Command Palette and type ``Conda`` to see all
available options.

Choose ``Conda: Activate Environment`` and the select the environment you want to activate.
Then select ``Conda`` as the build system to use the Python installation of the
activated environment.
