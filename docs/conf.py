# flake8: noqa
# -*- coding: utf-8 -*-

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = "1.0"

import inspect
import importlib
import re
import sphinx_compas_theme

# -- General configuration ------------------------------------------------

project = "COMPAS"
copyright = "COMPAS Association"
author = "Tom Van Mele"


def get_latest_version():
    with open("../CHANGELOG.md", "r") as file:
        content = file.read()
        pattern = re.compile(r"## (Unreleased|\[\d+\.\d+\.\d+\])")
        versions = pattern.findall(content)
        latest_version = versions[0] if versions else None
        if latest_version and latest_version.startswith("[") and latest_version.endswith("]"):
            latest_version = latest_version[1:-1]
        return latest_version


latest_version = get_latest_version()
if latest_version == "Unreleased":
    release = "Unreleased"
    version = "latest"
else:
    release = latest_version
    version = ".".join(release.split(".")[0:2])

master_doc = "index"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
templates_path = sphinx_compas_theme.get_autosummary_templates_path() + ["_templates"]
exclude_patterns = ["_build", "**.ipynb_checkpoints", "_notebooks", "**/__temp"]

# pygments_style = "sphinx"
# pygments_dark_style = "monokai"
# show_authors = True
add_module_names = True
language = "en"


# -- Extension configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    # "sphinx.ext.linkcode",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.coverage",
    # "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.autodoc.typehints",
    "sphinx_design",
    "sphinx_inline_tabs",
    "sphinx_togglebutton",
    "sphinx_remove_toctrees",
    "sphinx_copybutton",
    # "sphinxcontrib.bibtex",
    "numpydoc",
]

# remove_from_toctrees = ["api/generated/*"]

numpydoc_show_class_members = False
numpydoc_class_members_toctree = False
numpydoc_attributes_as_param_list = True

# bibtex options

# bibtex_bibfiles = ['refs.bib']

# autodoc options

autodoc_type_aliases = {}

# this does not work properly yet
# autodoc_typehints = "none"
# autodoc_typehints_format = "short"
autodoc_typehints_description_target = "documented"

autodoc_mock_imports = [
    "System",
    "clr",
    "Eto",
    "Rhino",
    "Grasshopper",
    "scriptcontext",
    "rhinoscriptsyntax",
    "bpy",
    "bmesh",
    "mathutils",
]

autodoc_default_options = {
    "undoc-members": True,
    "show-inheritance": True,
}

autodoc_member_order = "groupwise"

autoclass_content = "class"


def skip(app, what, name, obj, would_skip, options):
    if name.startswith("_"):
        return True
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


# autosummary options

autosummary_generate = True
autosummary_mock_imports = [
    "System",
    "clr",
    "Eto",
    "Rhino",
    "Grasshopper",
    "scriptcontext",
    "rhinoscriptsyntax",
    "bpy",
    "bmesh",
    "mathutils",
]

# graph options

# inheritance_graph_attrs = dict(rankdir="LR", resolution=150)
# inheritance_node_attrs = dict(fontsize=8)

# plot options

plot_include_source = False
plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = ["png"]

# intersphinx options

intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "compas": ("https://compas.dev/compas/latest/", None),
}

# linkcode


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    if not info["module"]:
        return None
    if not info["fullname"]:
        return None

    package = info["module"].split(".")[0]
    if not package.startswith("compas"):
        return None

    module = importlib.import_module(info["module"])
    parts = info["fullname"].split(".")

    if len(parts) == 1:
        obj = getattr(module, info["fullname"])
        mod = inspect.getmodule(obj)
        if not mod:
            return None
        filename = mod.__name__.replace(".", "/")
        lineno = inspect.getsourcelines(obj)[1]
    elif len(parts) == 2:
        obj_name, attr_name = parts
        obj = getattr(module, obj_name)
        attr = getattr(obj, attr_name)
        if inspect.isfunction(attr):
            mod = inspect.getmodule(attr)
            if not mod:
                return None
            filename = mod.__name__.replace(".", "/")
            lineno = inspect.getsourcelines(attr)[1]
        else:
            return None
    else:
        return None

    return f"https://github.com/compas-dev/compas/blob/main/src/{filename}.py#L{lineno}"


# extlinks


extlinks = {
    "rhino": ("https://developer.rhino3d.com/api/RhinoCommon/html/T_%s.htm", "%s"),
    "blender": ("https://docs.blender.org/api/2.93/%s.html", "%s"),
}

# from pytorch

from sphinx.writers import html, html5

# def visit_reference(self, node: Element) -> None:
#     atts = {'class': 'reference'}
#     if node.get('internal') or 'refuri' not in node:
#         atts['class'] += ' internal'
#     else:
#         atts['class'] += ' external'
#     if 'refuri' in node:
#         atts['href'] = node['refuri'] or '#'
#         if self.settings.cloak_email_addresses and atts['href'].startswith('mailto:'):
#             atts['href'] = self.cloak_mailto(atts['href'])
#             self.in_mailto = True
#     else:
#         assert 'refid' in node, \
#                 'References must have "refuri" or "refid" attribute.'
#         atts['href'] = '#' + node['refid']
#     if not isinstance(node.parent, nodes.TextElement):
#         assert len(node) == 1 and isinstance(node[0], nodes.image)  # NoQA: PT018
#         atts['class'] += ' image-reference'
#     if 'reftitle' in node:
#         atts['title'] = node['reftitle']
#     if 'target' in node:
#         atts['target'] = node['target']
#     self.body.append(self.starttag(node, 'a', '', **atts))

#     if node.get('secnumber'):
#         self.body.append(('%s' + self.secnumber_suffix) %
#                             '.'.join(map(str, node['secnumber'])))


def replace(Klass):
    old_call = Klass.visit_reference

    def visit_reference(self, node):
        if "refuri" in node:
            refuri = node.get("refuri")
            if "generated" in refuri:
                href_anchor = refuri.split("#")
                if len(href_anchor) > 1:
                    href = href_anchor[0]
                    anchor = href_anchor[1]
                    page = href.split("/")[-1]
                    parts = page.split(".")
                    if parts[-1] == "html":
                        pagename = ".".join(parts[:-1])
                        if anchor == pagename:
                            node["refuri"] = href
        return old_call(self, node)

    Klass.visit_reference = visit_reference


replace(html.HTMLTranslator)
replace(html5.HTML5Translator)

# -- Options for HTML output ----------------------------------------------

html_theme = "pydata_sphinx_theme"
html_logo = "_static/images/compas_icon_white.png"  # relative to parent of conf.py
html_title = "COMPAS docs"
html_favicon = "_static/images/compas.ico"

html_theme_options = {
    # theme structure and layout
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": [
        "version-switcher",
        # "theme-switcher",
        "navbar-icon-links",
    ],
    "navbar_persistent": ["search-button"],
    "navbar_align": "content",
    "article_header_start": [
        # "breadcrumbs"
    ],
    "article_header_end": [],
    "primary_sidebar_end": [
        # "sidebar-ethical-ads"
    ],
    "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
    "article_footer_items": ["prev-next.html"],
    "show_prev_next": True,
    # "content_footer_items": [],
    "footer_start": ["copyright", "sphinx-version"],
    "footer_end": ["theme-version"],
    # navigation and links
    "external_links": [
        # {"name": "Changelog", "url": "https://github.com/compas-dev/compas/releases"},
        {"name": "COMPAS Framework", "url": "https://compas.dev"},
        # {"name": "COMPAS Association", "url": "https://compas.dev/association"},
    ],
    "header_links_before_dropdown": 5,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/compas-dev/compas",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
        {
            "name": "Discourse",
            "url": "http://forum.compas-framework.org/",
            "icon": "fa-brands fa-discourse",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/COMPAS/",
            "icon": "fa-brands fa-python",
            "type": "fontawesome",
        },
    ],
    # "icon_links_label": "Quick Links",
    "use_edit_page_button": True,
    # user interface
    "announcement": "This is the WIP documentation for the pre-release of COMPAS 2.0. The documentation of COMPAS 1.17.5 is available <a href='https://compas.dev/compas/1.17.5/'>here</a>.",
    "switcher": {
        "json_url": "https://raw.githubusercontent.com/compas-dev/compas/gh-pages/versions.json",
        "version_match": version,
    },
    "check_switcher": False,
    # content and features
    # theming and style
    "logo": {
        "image_light": "_static/images/compas_icon_white.png",  # relative to parent of conf.py
        "image_dark": "_static/images/compas_icon_white.png",  # relative to parent of conf.py
        "text": "COMPAS docs",
    },
    "favicons": [
        {
            "rel": "icon",
            "href": "images/compas.ico",  # relative to the static path
        }
    ],
    "navigation_depth": 3,
    "show_nav_level": 1,
    "show_toc_level": 2,
    "pygment_light_style": "default",
    "pygment_dark_style": "monokai",
}

html_sidebars = {
    "**": [
        "sidebar-nav-bs",
        # "sidebar-ethical-ads",
    ],
}

html_context = {
    "github_url": "https://github.com",
    "github_user": "compas-dev",
    "github_repo": "compas",
    "github_version": "main",
    "doc_path": "docs",
}

html_static_path = ["_static"]
html_css_files = ["compas.css"]
html_extra_path = []
html_last_updated_fmt = ""
html_copy_source = False
html_show_sourcelink = True
html_permalinks = False
html_permalinks_icon = ""
html_compact_lists = True
