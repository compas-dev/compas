********************************************************************************
Installation
********************************************************************************

The **COMPAS** framework consists of a main library and a pool of add-on packages.
Both the main library and the additional packages currently still require a bit of
manual installation since they are not yet *pip installable* and do not ship with
a setup script. The following instructions will guide you through the installation
procedure for the main library.

.. note::
    
    The instructions are just guidelines. If you know what you are doing,
    feel free to do things differently.


General instructions
====================

1. **Create a base folder**

   Create a folder on your system where you will group all **COMPAS** related things.
   For example, you could create a folder on your home drive named *compas-dev*,
   which is the name of the GitHub *company* that hosts the **COMPAS** framework.

   .. code-block:: none

        $ cd ~
        $ mkdir compas-dev
        $ cd compas-dev


2. **Download the main library**

   There are two options for downloading the main library onto your system.

   a\. *Download a release*

   Download an archive from https://github.com/compas-dev/compas/releases
   and unpack it into the installation folder.

   b\. *Clone the GitHub repository*

   From the terminal 

   .. code-block:: none

        git clone https://github.com/compas-dev/compas.git

   Using GitHub Desktop

   .. code-block:: none

        GitHub Desktop > File > Clone Repository

   * Use the *Url* option.
   * Repository Url: https://github.com/compas-dev/compas.git
   * Local Path: `path/to/compas-dev/compas`

   .. figure:: /_images/github_clonerepo.*
        :figclass: figure
        :class: figure-img img-fluid


3. **Verify the clone or download**

   After cloning or downloading, the folder structure should contain::

        compas-dev
            - compas
                - libs
                    ...
                - samples
                    ...
                - src
                    - compas
                    - compas_blender
                    - compas_maya
                    - compas_rhino
                - temp
                    ...


4. **Configure your system**

   * Verify that Python is on the system ``PATH``.
   * Add the compas framework to the ``PYTHONPATH``.

   Operating system-specific instructions for this step can be found below:

   * `Unix`_ 
   * `Windows`_


5. **Verify your installation**

   After having set the system variables test your installation.
   Start an interactive Python session (in Terminal or Command Prompt)::

        $ python


   Then try the following code.

   .. code-block:: python

        >>> import compas
        >>> compas.verify()

   This will produce something like this:

   .. code-block:: none

        ================================================================================
        Checking required packages...

        All required packages are installed.

        Checking optional packages...

        The following optional packages are not installed:
        - xxx
        - yyy
        - zzz
        ================================================================================


   If all required packages are installed, try

   .. code-block:: python

        >>> import compas
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_obj(compas.get('faces.obj'))
        >>> print(mesh)


.. _Unix:

On Unix (Linux, OSX)
====================

Open Terminal to edit your system variables in ``.bash_profile``::
    
    $ cd ~
    $ nano .bash_profile

.. note::
    
    You may be prompted for the administrator password.
    Characters will not appear while you are typing.


Add the following::

    export PATH="/path/to/anaconda/bin:$PATH"
    export PYTHONPATH="/path/to/compas-dev/compas/src:$PYTHONPATH"


.. figure:: /_images/mac_bashprofile.*
     :figclass: figure
     :class: figure-img img-fluid


After adding the paths, exit the editor with ``ctrl + o``, ``enter``, ``ctrl + x``.
Then restart your Terminal or type::

    $ source .bash_profile


.. _Windows:

On Windows
==========

On Windows, you will have to change your *Environment Variables*::

    Control Panel > System > Advanced system settings > Environment Variables


.. .. figure:: /_images/windows_controlpanel.*
..      :figclass: figure
..      :class: figure-img img-fluid


.. .. figure:: /_images/windows_advancedsystemsettings.*
..      :figclass: figure
..      :class: figure-img img-fluid


.. .. figure:: /_images/windows_environment.*
..      :figclass: figure
..      :class: figure-img img-fluid


In the section *User variables*, edit ``PATH``.

.. note::

    Create a new ``PATH`` variable if one doesn't exist.


.. figure:: /_images/windows_path.*
     :figclass: figure
     :class: figure-img img-fluid


Add the paths to your Anaconda installation.

.. figure:: /_images/windows_path-entries.*
     :figclass: figure
     :class: figure-img img-fluid


Then add ``compas`` to the ``PYTHONPATH``.

.. note::

    Create a new ``PTYTHONPATH`` variable if one doesn't exist.


.. figure:: /_images/windows_pythonpath.*
     :figclass: figure
     :class: figure-img img-fluid


.. figure:: /_images/windows_pythonpath-entries.*
     :figclass: figure
     :class: figure-img img-fluid

