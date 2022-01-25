from typing import List
from uuid import uuid4

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.docutils import SphinxDirective
from sphinx.util.logging import getLogger

LOGGER = getLogger(__name__)


def setup(app: Sphinx) -> None:
    app.add_directive("tabs", TabSetDirective)
    app.add_directive("tab-item", TabItemDirective)
    app.add_post_transform(TabSetHtmlTransform)
    app.add_node(compas_tab_input, html=(visit_tab_input, depart_tab_input))
    app.add_node(compas_tab_label, html=(visit_tab_label, depart_tab_label))
    app.add_node(nodes.container, override=True, html=(visit_container, depart_container))


def visit_container(self, node: nodes.Node):
    classes = "docutils container"
    attrs = {}
    if node.get("is_div", False):
        classes = "docutils"
    self.body.append(self.starttag(node, "div", CLASS=classes, **attrs))


def depart_container(self, node: nodes.Node):
    self.body.append("</div>\n")


class TabSetDirective(SphinxDirective):
    """A container for a set of tab items."""

    has_content = True

    def run(self) -> List[nodes.Node]:
        """Run the directive."""
        self.assert_has_content()
        tabs = nodes.container("", is_div=True, component="tabs", classes=["compas-tabs"])
        self.set_source_info(tabs)
        self.state.nested_parse(self.content, self.content_offset, tabs)
        return [tabs]


class TabItemDirective(SphinxDirective):

    required_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        "active": directives.flag,
        "name": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        """Run the directive."""
        self.assert_has_content()
        tab_item = nodes.container("", component="tab-item", is_div=True, classes=["compas-tab-item"], active=("active" in self.options))

        # add tab label
        textnodes, _ = self.state.inline_text(self.arguments[0], self.lineno)
        tab_label = nodes.rubric(self.arguments[0], *textnodes, classes=["compas-tab-item-label"])
        self.add_name(tab_label)
        tab_item += tab_label

        # add tab content
        tab_content = nodes.container("", component="tab-content", is_div=True, classes=["compas-tab-item-content"])
        self.state.nested_parse(self.content, self.content_offset, tab_content)
        tab_item += tab_content

        return [tab_item]


class compas_tab_input(nodes.Element, nodes.General):
    pass


class compas_tab_label(nodes.TextElement, nodes.General):
    pass


def visit_tab_input(self, node):
    attributes = {"ids": [node["id"]], "type": node["type"], "name": node["set_id"]}
    if node["checked"]:
        attributes["checked"] = "checked"
    self.body.append(self.starttag(node, "input", **attributes))


def depart_tab_input(self, node):
    self.body.append("</input>")


def visit_tab_label(self, node):
    attributes = {"for": node["input_id"]}
    if "sync_id" in node:
        attributes["data-sync-id"] = node["sync_id"]
    self.body.append(self.starttag(node, "label", **attributes))


def depart_tab_label(self, node):
    self.body.append("</label>")


def is_component(node: nodes.Node, name: str):
    """Check if a node is a certain design component."""
    try:
        return node.get("component") == name
    except AttributeError:
        return False


class TabSetHtmlTransform(SphinxPostTransform):
    """Transform tabs to HTML specific AST structure."""

    default_priority = 200
    formats = ("html",)

    def get_unique_key(self):
        return str(uuid4())

    def run(self) -> None:
        """Run the transform."""
        for tabs in self.document.traverse(lambda node: is_component(node, "tabs")):
            tabs_identity = self.get_unique_key()
            children = []

            # get the first selected node
            active_index = None
            for index, tab_item in enumerate(tabs.children):
                if tab_item.get("active", False):
                    if active_index is None:
                        active_index = index
            active_index = 0 if active_index is None else active_index

            for index, tab_item in enumerate(tabs.children):
                try:
                    tab_label, tab_content = tab_item.children
                except ValueError:
                    print(tab_item)
                    raise
                tab_item_identity = self.get_unique_key()

                # create: <input checked="checked" id="id" type="radio">
                input_node = compas_tab_input("", id=tab_item_identity, set_id=tabs_identity, type="radio", checked=(index == active_index))
                input_node.source, input_node.line = tab_item.source, tab_item.line
                children.append(input_node)

                # create: <label for="id">...</label>
                label_node = compas_tab_label("", *tab_label.children, input_id=tab_item_identity, classes=tab_label["classes"])
                label_node.source, label_node.line = tab_item.source, tab_item.line
                children.append(label_node)

                # add content
                children.append(tab_content)

            print(tabs['classes'])
            tabs['classes'] = [value for value in tabs['classes'] if value != 'container']
            tabs.children = children
