import pickle
from compas.data import Data


class DataObject(Data):

    def __init__(self):
        super(DataObject, self).__init__()
        self.point = [0, 0, 0]
        self.normal = [0, 0, 1]
        self.radius = 1.0

    @property
    def data(self):
        return {'plane': {'point': self.point, 'normal': self.normal}, 'radius': self.radius}

    @data.setter
    def data(self, data):
        self.point = data['plane']['point']
        self.normal = data['plane']['normal']
        self.radius = data['radius']


def test_pickling():
    d1 = DataObject()
    s = pickle.dumps(d1)
    d2 = pickle.loads(s)
    assert all(a == b for a, b in zip(d1.point, d2.point))
    assert all(a == b for a, b in zip(d1.normal, d2.normal))
    assert d1.radius == d2.radius
