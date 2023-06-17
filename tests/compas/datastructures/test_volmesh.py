import compas
from compas.datastructures import VolMesh


def test_volmesh_data():
    vmesh1 = VolMesh.from_obj(compas.get("boxes.obj"))

    data1 = vmesh1.to_data()
    data1_ = vmesh1.to_data()

    assert data1 == data1_

    vmesh2 = VolMesh.from_data(data1_)

    data2 = vmesh2.to_data()
    data2_ = vmesh2.to_data()

    assert data2 == data2_
    assert data1 == data2
