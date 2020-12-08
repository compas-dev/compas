import compas
from compas.datastructures import VolMesh


def test_data():

    vmesh1 = VolMesh.from_obj(compas.get('boxes.obj'))

    data1 = vmesh1.to_data()

    vmesh1.to_json('vmesh1.json')
    vmesh1.from_json('vmesh1.json')

    vmesh1.validate_data()
    vmesh1.validate_json()

    data1_ = vmesh1.to_data()

    assert data1 == data1_

    vmesh2 = VolMesh.from_data(data1_)

    vmesh2.validate_data()
    vmesh2.validate_json()

    data2 = vmesh2.to_data()

    vmesh2.to_json('vmesh2.json')
    vmesh2.from_json('vmesh2.json')

    data2_ = vmesh2.to_data()

    assert data2 == data2_

    assert data1 == data2