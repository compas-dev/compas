from compas.geometry import Transformation


__all__ = ["Object3D"]


class Object3D(object):

    """
    """

    __module__ = "compas.geometry"

    def __init__(self, geometry=None, attributes=None):

        self.geometry = geometry
        self.attributes = attributes

        self._parent = None
        self._children = []

        self.transformation = Transformation()

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    def get_parents(self, parent_chain=None):
        if parent_chain is None:
            parent_chain = []
        if self._parent is not None:
            parent_chain.append(self._parent)
            self._parent.get_parents(parent_chain)
        return parent_chain

    @property
    def transformation_world(self):
        T_world = self.transformation.copy()
        for p in self.get_parents():
            T_world *= p.transformation
        return T_world

    def apply_transformation(self, T):
        self.transformation *= T

    def add_child(self, child):

        if child == self:
            raise ValueError('cannot add object itself')
        if child._parent is not None:
            child._parent.remove(child)
        child._parent = self
        self._children.append(child)

    def remove_child(self, child):
        child._parent = None
        self._children.remove(child)


if __name__ == "__main__":

    obj1 = Object3D()
    obj2 = Object3D()
    obj3 = Object3D()

    obj1.add_child(obj2)
    obj2.add_child(obj3)

    print(obj3.get_parents())
