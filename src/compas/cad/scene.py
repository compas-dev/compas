__all__ = ["Scene"]


class Scene(object):

    """
    Scence class serves as a container to store object3ds for visualization
    """

    __module__ = "compas.cad"

    def __init__(self):
        self._children = []

    @property
    def children(self):
        """get the children nodes of this scene"""
        return self._children

    def get_parents(self, _):
        pass

    def get_children(self, children_list=None):
        """get flat list of all children nodes of this scene"""
        if children_list is None:
            children_list = []
        for child in self.children:
            children_list.append(child)
            child.get_children(children_list)
        return children_list

    def add(self, child):
        """add a child node under this object3d"""
        if child == self:
            raise ValueError("cannot add object itself")
        if child._parent is not None:
            child._parent.remove(child)
        child._parent = self
        self._children.append(child)

    def remove(self, child):
        """remove a child node under this object3d"""
        child._parent = None
        self._children.remove(child)

    def create_artist(self, frontend=None):
        """assign an artist to visualize this scene in a give frontend"""
        raise NotImplementedError()

    def draw(self, **kwargs):
        """draw this all of object3Ds under this scene through assigned artist"""
        # self.artist.draw(**kwargs)
        raise NotImplementedError()

    def redraw(self, **kwargs):
        """update and redraw this scene through assigned artist"""
        # self.artist.redraw(**kwargs)
        raise NotImplementedError()


if __name__ == "__main__":

    from compas.cad import Object3D

    scene = Scene()

    o1 = Object3D()
    o2 = Object3D()
    o1.add(o2)
    scene.add(o1)

    print(scene.get_children())
    print(o2.get_parents())

    scene.remove(o1)
    print(scene.get_children())
    print(o2.get_parents())
