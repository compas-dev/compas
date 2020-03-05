********************************************************************************
Visual Studio Code
********************************************************************************

`Visual Studio Code <https://code.visualstudio.com/>`_ is a free and open source text
editor with very good support for Python programming.
We recommend installing the following VS Code extensions:

* `Python <https://marketplace.visualstudio.com/items?itemName=ms-python.python>`_

  *Official extension to add support for Python programming, including debugging, auto-complete, formatting, etc.*

* `EditorConfig <https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig>`_

  *Add support for ``.editorconfig`` files to VS Code.*

To install the above extensions, open the ``Extensions`` view  by clicking on the
``Extensions`` icon in the **Activity Bar** on the left side of VS Code and search
the extension name in the search box. Once found, select it and click ``Install``.

By default, VS Code will use ``PyLint`` to verify your code. To select a different
linter: open the ``Command Palette`` (``Ctrl+Shift+P``) and select the
``Python: Select Linter`` command.


Run scripts
===========

To run Python scripts from within VS Code, you have several options:

* Right-click on the file, and select ``Run Python File in Terminal``.
* Open the file and press ``F5`` to start the script with the debugger attached, which means you can add breakpoints (clicking on the gutter, next to the line numbers), inspect variables and step into your code for debugging, or...
* Open the file and press ``Ctrl+F5`` to start the script without debugger.

.. note::

    On Windows, VS Code uses PowerShell as default terminal shell, which causes problems when used with Anaconda.
    To switch to the standard Windows shell, press ``Ctrl+Shift+P``, type ``Select Default Shell``, and choose ``Command Prompt`` instead.


Virtual environments
====================

If you are using ``conda`` to manage your virtual environments, VS Code has built-in
support for them. When a ``.py`` file is open on VS Code, the bottom left side of the
**Status bar** will show the Python interpreter used to run scripts.
Click on it and a list of all available interpreters including all environments
will be shown. Select one, and the next time you run a script, the newly selected
interpreter will be used.


More features
=============

VS Code provides a large set of features to make it easier to program in Python.
`Check out the documentation for more details <https://code.visualstudio.com/docs/languages/python>`_.
