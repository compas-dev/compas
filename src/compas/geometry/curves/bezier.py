from compas.geometry import Point
from ._curve import Curve


class BezierCurve(Curve):

    __slots__ = [...]

    @property
    def DATASCHEMA(self):
        import schema
        return schema.Schema({...})

    @property
    def JSONSCHEMANAME(self):
        return 'bezier'

    def __init__(self, points, **kwargs):
        super(BezierCurve, self).__init__(**kwargs)
        self._points = None
        self.points = points

    @property
    def data(self):
        """dict : The data dictionary that represents the curve."""
        return {'points': [point.data for point in self.points]}

    @data.setter
    def data(self, data):
        self.points = [Point.from_data(point) for point in data['points']]

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = [Point(x, y, z) for x, y, z in points]

    @property
    def degree(self):
        return len(self.points) - 1
