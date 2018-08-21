********************************************************************************
Documentation
********************************************************************************


The documentation of **COMPAS** is generated with `Sphinx <http://www.sphinx-doc.org/en/stable/>`_.
Sphinx uses `reStructuredText <http://www.sphinx-doc.org/en/stable/rest.html>`_
(reST) as its markup language, which is parsed and translated to different output formats, 
such as HTML, using `Docutils <http://docutils.sourceforge.net/>`_. The default
templating language in Sphinx is `Jinja <http://www.sphinx-doc.org/en/stable/templating.html>`_.

Sphinx adds various new directives to standard reST. An overview is
available `here <http://www.sphinx-doc.org/en/stable/markup/index.html>`_.

Documentation can be generated from hand-written `*.rst` files and from the
*docstrings* in your code using the `autodoc <http://www.sphinx-doc.org/en/stable/ext/autodoc.html>`_
and `autosummary <http://www.sphinx-doc.org/en/stable/ext/autosummary.html>`_ extensions.
For an overview of builtin extensions, see `builtins <http://www.sphinx-doc.org/en/stable/ext/builtins.html>`_.

In addition to `autosummary` and `autodoc`, the **COMPAS** docs also use

* `sphinx.ext.intersphinx <http://www.sphinx-doc.org/en/stable/ext/intersphinx.html>`_,
* `sphinx.ext.mathjax <http://www.sphinx-doc.org/en/stable/ext/math.html#module-sphinx.ext.mathjax>`_,
* `sphinx.ext.napoleon <http://www.sphinx-doc.org/en/stable/ext/napoleon.html>`_,
* `sphinx.ext.viewcode <http://www.sphinx-doc.org/en/stable/ext/viewcode.html>`_,
* `matplotlib.sphinxext.plot_directive <https://matplotlib.org/sampledoc/extensions.html>`_.


Project structure
=================

.. code-block:: none

    + path/to/doc
        + _build
            # optional output directory for the built documentation
        + _source
            + _images
                # add here images that are referenced from rst files or from the docstrings
            + _static
                # add here content that is not referenced from the rst files or docstrings
                # for example, css files, js files, favicons.ico, ...
                #
                # note: the name of this folder can be specified in conf.py
            + _templates
                # add here any html templates
                # note: the name of this folder can be specified in conf.py
                #
                # the base templates are found in
                # path/to/site-packages/sphinx/theme/basic
                # - layout.html
                # - ...
                + autosummary
                    # add here rst templates used by autosummary
                    # the base templates can be found in
                    # path/to/site-packages/sphinx/ext/autosummary/templates/autosummary
                    # - base.rst
                    # - class.rst
                    # - method.rst
                    # - module.rst
            - conf.py
                # the configuration file
            - index.rst
                # the master document


Configuration: `conf.py`
========================

* general options

  .. code-block:: python

        #

* `autosummary` and `autodoc` options

  .. code-block:: python

        # include undocumented members
        # include special members (e.g. magic methods)
        # include the bases of a class
        autodoc_default_flags - [
            'undoc-members',
            'special-members',
            'show-inheritance',
        ]

        # alphabetic ordering of class methods and attributes
        autodoc_member_order - 'alphabetical'

        # 
        autosummary_generate - True

* `napoleon` options

  .. code-block:: python

        napoleon_google_docstring - False
        napoleon_numpy_docstring - True
        napoleon_include_init_with_doc - False
        napoleon_include_private_with_doc - True
        napoleon_include_special_with_doc - True
        napoleon_use_admonition_for_examples - False
        napoleon_use_admonition_for_notes - False
        napoleon_use_admonition_for_references - False
        napoleon_use_ivar - False
        napoleon_use_param - False
        napoleon_use_rtype - False

* `plot_directive` options

  .. code-block:: python

        # plot_include_source
        # plot_pre_code
        # plot_basedir
        # plot_formats
        # plot_rcparams
        # plot_apply_rcparams
        # plot_working_directory
        # plot_template

        plot_html_show_source_link - False
        plot_html_show_formats - False

* HTML options

  .. code-block:: python

        html_theme - 'compas'
        html_theme_path - ['../../sphinx_compas_theme']
        html_theme_options - {}
        html_context - {}
        html_static_path - ['_static']
        html_last_updated_fmt - ''
        html_copy_source - False
        html_show_sourcelink - False
        html_add_permalinks - ''
        html_experimental_html5_writer - True
        html_compact_lists - True


sphinx_compas_theme
-------------------

The COMPAS framework uses its own Sphinx theme, which is available at https://github.com/compas-dev/sphinx_compas_theme.git.
The theme is based on the `Bootstrap front-end framework <https://getbootstrap.com/>`_.

To use the theme, clone the repository and modify the configuration file as explained above.


reST files
----------

* Including code

  http://www.sphinx-doc.org/en/stable/markup/code.html

  .. code-block:: reST

      .. code-block:: python

          import compas

  .. code-block:: reST

      .. literalinclude:: conf.py


* Including images

  .. code-block:: reST

      .. image:: /_images/compas_intro.jpg

  .. code-block:: reST

      .. figure:: /_images/compas_intro.jpg
           :figclass: figure
           :class: figure-img img-fluid

* Including plots
* Including raw html


API docs
--------

* `__init__`
* docstrings
* autosummary

