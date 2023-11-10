from compas.data import Data
from compas.datastructures import Tree
from compas.datastructures import TreeNode
from compas.scene import SceneObject

class Scene(Data):
    def __init__(self, name=None):
        super(Scene, self).__init__(name)
        self._tree = Tree("Scene")
        root = TreeNode(name='root')
        self.tree.add(root)

    @property
    def tree(self):
        return self._tree
    
    @property
    def sceneobjects(self):
        return [node.attributes['sceneobject'] for node in self.tree.nodes if 'sceneobject' in node.attributes]

    def add(self, item, parent=None, **kwargs):
        sceneobject = SceneObject(item, **kwargs)
        name = item.name or item.__class__.__name__
        node = TreeNode(name, attributes={'sceneobject': sceneobject})

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
            if 'sceneobject' in node.attributes:
                if node.attributes['sceneobject'] == sceneobject:
                    return node
        raise Exception('Scene object not in scene')

    def redraw(self):
        for sceneobject in self.sceneobjects:
            sceneobject.draw()
