import compas
from compas.datastructures import VolMesh
from compas.utilities import DataEncoder
import json



def test_data_setter():

    v1 = VolMesh.from_obj(compas.get("boxes.obj"))
    data1 = v1.to_data()
    json_str = json.dumps(data1, cls=DataEncoder)

    v2 = VolMesh.from_data(json.loads(json_str))
    data2 = v2.to_data()

    assert data1 == data2