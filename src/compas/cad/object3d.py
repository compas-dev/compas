from compas.geometry import Transformation


__all__ = ["Object3D"]


class Object3D(object):

    """
    Base object3d class that stores local/world transformation of geometry and its parent/children hierrachy
    """

    __module__ = "compas.cad"

    def __init__(self, geometry=None, attributes=None):

        self.geometry = geometry
        self.attributes = attributes

        self._parent = None
        self._children = []

        self.transformation = Transformation()

    def __repr__(self):
        s = "Object3D"
        if self.geometry:
            s += '.' + self.geometry.__class__.__name__
        if self.attributes:
            s += '.' + self.attributes.__repr__()
        return s

    @property
    def parent(self):
        """get the parent node of this object3d"""
        return self._parent

    @property
    def children(self):
        """get the children nodes of this object3d"""
        return self._children

    def get_parents(self, parent_list=None):
        """get flat list of all parental nodes of this object3d"""
        if parent_list is None:
            parent_list = []
        if self.parent is not None:
            parent_list.append(self.parent)
            self.parent.get_parents(parent_list)
        return parent_list

    def get_children(self, children_list=None):
        """get flat list of all children nodes of this object3d"""
        if children_list is None:
            children_list = []
        for child in self.children:
            children_list.append(child)
            child.get_children(children_list)
        return children_list

    @property
    def transformation_world(self):
        """get the global transformation of this object3d"""
        T_world = self.transformation.copy()
        for p in self.get_parents():
            T_world *= p.transformation
        return T_world

    def apply_transformation(self, T):
        """apply a transformation to this object3d"""
        self.transformation *= T

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
        """assign an artist to visualize this object3d in a give frontend"""
        raise NotImplementedError()

    def draw(self, **kwargs):
        """draw this object3d through assigned artist"""
        # self.artist.draw(**kwargs)
        raise NotImplementedError()

    def redraw(self, **kwargs):
        """update and redraw this object3d through assigned artist"""
        # self.artist.redraw(**kwargs)
        raise NotImplementedError()


if __name__ == "__main__":

    from compas.geometry import Point

    obj1 = Object3D(geometry=Point(0, 0, 0), attributes={"name": "obj1"})
    obj2 = Object3D(geometry=Point(1, 0, 0), attributes={"name": "obj2"})
    obj3 = Object3D(geometry=Point(2, 0, 0), attributes={"name": "obj3"})
    obj4 = Object3D(geometry=Point(3, 0, 0), attributes={"name": "obj4"})

    obj1.add(obj2)
    obj1.add(obj3)
    obj3.add(obj4)

    print(obj4.get_parents())
    print(obj1.get_children())
