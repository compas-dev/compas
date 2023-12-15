from compas.data import Data
from compas.datastructures import Tree
from compas.datastructures import TreeNode
from .context import build_scene_object
from .context import redraw
from .context import clear


class Scene(Data):
    def __init__(self, name=None, context=None):
        super(Scene, self).__init__(name)
        self._tree = Tree("Scene")
        self.context = context
        root = TreeNode(name="root")
        self.tree.add(root)

    @property
    def tree(self):
        return self._tree

    @property
    def sceneobjects(self):
        return [node.attributes["sceneobject"] for node in self.tree.nodes if "sceneobject" in node.attributes]

    def add(self, item, parent=None, **kwargs):
        sceneobject = build_scene_object(item, context=self.context, **kwargs)
        name = item.name or item.__class__.__name__
        node = TreeNode(name, attributes={"sceneobject": sceneobject})

        if parent is None:
            self.tree.add(node, parent=self.tree.root)
        else:
            parent_node = self._get_node(parent)
            self.tree.add(node, parent=parent_node)

        return sceneobject

    def remove(self, sceneobject):
        node = self._get_node(sceneobject)
        self.tree.remove(node)

    def _get_node(self, sceneobject):
        for node in self.tree.nodes:
            if "sceneobject" in node.attributes:
                if node.attributes["sceneobject"] == sceneobject:
                    return node
        raise Exception("Scene object not in scene")

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
