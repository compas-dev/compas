from compas.data import Data
from compas.datastructures import Tree
from compas.datastructures import TreeNode
from .context import build_scene_object
from .context import redraw


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
        self.tree.remove_node(node)

    def _get_node(self, sceneobject):
        for node in self.tree.nodes:
            if "sceneobject" in node.attributes:
                if node.attributes["sceneobject"] == sceneobject:
                    return node
        raise Exception("Scene object not in scene")

    def redraw(self):
        drawn_objects = []
        for sceneobject in self.sceneobjects:
            drawn_object = sceneobject.draw()

            # TODO: unify output of draw(), so we don't have to do this
            if isinstance(drawn_object, (list, tuple)):
                for item in drawn_object:
                    if isinstance(item, (list, tuple)):
                        drawn_objects.extend(item)
                    else:
                        drawn_objects.append(item)
            else:
                drawn_objects.append(drawn_object)

        if drawn_objects:
            redraw()

        return drawn_objects

    def print_hierarchy(self):
        self.tree.print_hierarchy()
