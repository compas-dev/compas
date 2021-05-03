from compas.datastructures import Mesh
from compas_rhino.objects.meshobject import MeshObject


class BoxObject(MeshObject):

    def __init__(self, box, **kwargs):
        super(BoxObject, self).__init__(Mesh.from_shape(box), **kwargs)
        self._data = box
