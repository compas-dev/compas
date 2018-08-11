# -*- coding: utf-8 -*-

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'


# -- General configuration ------------------------------------------------

project          = 'COMPAS'
copyright        = '2017, Block Research Group - ETH Zurich'
author           = 'Tom Van Mele'
release          = '0.2.7'
version          = '.'.join(release.split('.')[0:2])

master_doc       = 'index'
source_suffix    = ['.rst', ]
templates_path   = ['_templates', ]
exclude_patterns = ['_build', ]

pygments_style   = 'sphinx'
show_authors     = True
add_module_names = True
language         = None


# -- Extension configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'matplotlib.sphinxext.plot_directive',
]

# autodoc options

autodoc_default_flags = [
    'undoc-members',
    'private-members',
    'special-members',
    'show-inheritance',
]

autodoc_member_order = 'alphabetical'

# autosummary options

autosummary_generate = True

# napoleon options

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False

# plot options

# plot_include_source
# plot_pre_code
# plot_basedir
# plot_formats
# plot_rcparams
# plot_apply_rcparams
# plot_working_directory
# plot_template

plot_html_show_source_link = False
plot_html_show_formats = False

# intersphinx options

intersphinx_mapping = {'python': ('https://docs.python.org/', None)}


# -- Options for HTML output ----------------------------------------------

html_theme = 'compas'
html_theme_path = ['../temp/sphinx_compas_theme']
html_theme_options = {
    'navbar_active' : 'main',
}
html_context = {}
html_static_path = []
html_extra_path = ['.nojekyll']
html_last_updated_fmt = ''
html_copy_source = False
html_show_sourcelink = False
html_add_permalinks = ''
html_experimental_html5_writer = True
html_compact_lists = True
