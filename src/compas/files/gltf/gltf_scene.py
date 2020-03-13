from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from compas.files.gltf.gltf_children import GLTFChildren


class GLTFScene(object):
    """Object representing the COMPAS consumable part of a glTF scene.

    Attributes
    ----------
    name : str
        Name of the scene.
    children : GLTFChildren
        List of keys referencing :attr:`compas.files.GLTFScene.context.nodes`.
    extras : object
    extensions : object
    context : :class:`compas.files.GLTFContent`
        GLTF context in which the GLTFScene exists.
    """
    def __init__(self, context, name=None, extras=None, extensions=None):
        self.name = name
        self._children = GLTFChildren(context, [])
        self.extras = extras
        self.extensions = extensions

        self._key = None
        self.context = context
        self._set_key()

    def _set_key(self):
        key = len(self.context.scenes)
        while key in self.context.scenes:
            key += 1
        self.context.scenes[key] = self
        self._key = key

    @property
    def key(self):
        return self._key

    def get_dict(self, node_index_by_key):
        scene_dict = {}
        if self.children:
            scene_dict['nodes'] = [node_index_by_key[key] for key in self.children]
        if self.name:
            scene_dict['name'] = self.name
        if self.extras:
            scene_dict['extras'] = self.extras
        if self.extensions:
            scene_dict['extensions'] = self.extensions
        return scene_dict

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = GLTFChildren(self.context, value or [])

    @property
    def nodes(self):
        """Returns dictionary of nodes in the given scene, without a specified root."""
        return self.context.get_nodes_from_scene(self)

    @property
    def positions_and_edges(self):
        """Returns a tuple containing a dictionary of positions and a list of tuples representing edges."""
        return self.context.get_scene_positions_and_edges(self)

    def add_child(self, node_name=None, node_extras=None):
        return self.context.add_node_to_scene(self, node_name, node_extras)
