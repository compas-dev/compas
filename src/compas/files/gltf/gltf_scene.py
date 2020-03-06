from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


class GLTFScene(object):
    """Object representing the base of a scene.

    Attributes
    ----------
    name : str
        Name of the scene.
    nodes : list
        List of keys referencing :attr:`compas.files.GLTFScene.context`.
    extras : object
    context : GLTFContent
    """
    def __init__(self, context, name=None, extras=None):
        self.name = name
        self.nodes = []
        self.extras = extras

        self.key = None
        self.context = context

    def add_node(self, node_name=None, node_extras=None):
        return self.context.add_node_to_scene(self, node_name, node_extras)
