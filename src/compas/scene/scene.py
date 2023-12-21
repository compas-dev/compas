from compas.data import Data
from compas.datastructures import Tree
from compas.datastructures import TreeNode
from .sceneobject import SceneObject
from .context import redraw
from .context import clear


class SceneObjectNode(TreeNode):
    def __init__(self, sceneobject):
        super(SceneObjectNode, self).__init__(name=sceneobject.name)
        self.object = sceneobject

    @property
    def parent_object(self):
        if self.parent and isinstance(self.parent, SceneObjectNode):
            return self.parent.object
        return None

    @property
    def children_objects(self):
        return [child.object for child in self.children]


class SceneTree(Tree):
    def __init__(self, name=None):
        super(SceneTree, self).__init__(name=name)
        root = TreeNode(name="root")
        self.add(root)

    @property
    def objects(self):
        return [node.object for node in self.nodes if isinstance(node, SceneObjectNode)]

    def add_object(self, sceneobject, parent=None):
        node = SceneObjectNode(sceneobject)
        if parent is None:
            self.add(node, parent=self.root)
        else:
            parent_node = self.get_node_from_object(parent)
            self.add(node, parent=parent_node)

        sceneobject._node = node

    def get_node_from_object(self, sceneobject):
        for node in self.nodes:
            if isinstance(node, SceneObjectNode):
                if node.object == sceneobject:
                    return node
        raise ValueError("Scene object not in scene")


class Scene(Data):
    def __init__(self, name=None, context=None):
        super(Scene, self).__init__(name)
        self._tree = SceneTree("Scene")
        self.context = context

    @property
    def tree(self):
        return self._tree

    @property
    def objects(self):
        return self.tree.objects

    def add(self, item, parent=None, **kwargs):
        sceneobject = build_scene_object(item, context=self.context, **kwargs)
        self.tree.add_object(sceneobject, parent=parent)
        return sceneobject

    def remove(self, sceneobject):
        node = self._get_node(sceneobject)
        self.tree.remove(node)

    def clear(self):
        guids = []
        for sceneobject in self.sceneobjects:
            guids += sceneobject.guids
            sceneobject._guids = None
        clear(guids=guids)

    def redraw(self):
        self.clear()

        drawn_objects = []
        for sceneobject in self.sceneobjects:
            drawn_objects += sceneobject.draw()

        if drawn_objects:
            redraw()

        return drawn_objects

    def print_hierarchy(self):
        self.tree.print_hierarchy()
