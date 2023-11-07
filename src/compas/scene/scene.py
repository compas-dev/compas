from compas.datastructures import Tree
from compas.datastructures import TreeNode
from compas.artists import Artist

class Scene(Tree):
    def __init__(self, name=None, attributes=None):
        super(Scene, self).__init__(name, attributes)
        root = TreeNode(name='root')
        super(Scene, self).add(root)

    def add(self, item, parent=None, **kwargs):
        sceneobject = Artist(item, **kwargs)
        name = item.name or item.__class__.__name__
        node = TreeNode(name, attributes={'sceneobject': sceneobject})

        if parent is None:
            super(Scene, self).add(node, parent=self.root)
        else:
            parent_node = self._get_node(parent)
            super(Scene, self).add(node, parent=parent_node)

        return sceneobject

    def _get_node(self, sceneobject):
        for node in self.nodes:
            if 'sceneobject' in node.attributes:
                if node.attributes['sceneobject'] == sceneobject:
                    return node
        raise Exception('Scene object not in scene')

    def redraw(self):
        for node in self.nodes:
            if 'sceneobject' in node.attributes:
                node.attributes['sceneobject'].draw()
