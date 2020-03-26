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
        Validated list of keys referencing :attr:`compas.files.GLTFScene.context.nodes`.
    extras : object
    extensions : object
    context : GLTFContent
        GLTF context in which the scene exists.
    key : int
        Key of the scene within :attr:`compas.files.GLTFContent.scenes`.
    nodes : dict
        Dictionary of nodes in the given scene, without a specified root.
    positions_and_edges : tuple
        Tuple containing a dictionary of positions and a list of tuples representing edges.

    Methods
    -------
    add_child(str node_name, object node_extras)
        Creates a :class:`compas.files.GLTFNode` with name `node_name` (default `None`)
        and extras `node_extras` (default `None`), and adds this node to the children of `scene`.
    to_dict(dict node_index_by_key)
        Returns a JSONable dictionary object in accordance with glTF specifications.
    from_dict(dict scene, GLTFContent context)
        Creates a :class:`compas.files.GLTFScene` from a glTF scene dictionary
        and inserts it in the provided context.
    """
    def __init__(self, context, children=None, name=None, extras=None, extensions=None):
        self.name = name
        self._children = GLTFChildren(context, children or [])
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

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = GLTFChildren(self.context, value or [])

    @property
    def nodes(self):
        return self.context.get_nodes_from_scene(self)

    @property
    def positions_and_edges(self):
        return self.context.get_scene_positions_and_edges(self)

    def add_child(self, node_name=None, node_extras=None):
        return self.context.add_node_to_scene(self, node_name, node_extras)

    def to_dict(self, node_index_by_key):
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

    @classmethod
    def from_dict(cls, scene, context):
        if scene is None:
            return None
        return cls(
            context=context,
            children=scene.get('nodes'),
            name=scene.get('name'),
            extras=scene.get('extras'),
            extensions=scene.get('extensions'),
        )
