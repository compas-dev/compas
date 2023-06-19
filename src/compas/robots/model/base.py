from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.files import URDFElement
from compas.files import URDFGenericElement
from compas.geometry import Frame


def _parse_floats(values):
    return [float(i) for i in values.split()]


def _generic_from_data_or_data(data):
    try:
        data = URDFGenericElement.from_data(data)
    finally:
        return data


def _attr_to_data(attr):
    return {k: v.data if hasattr(v, "data") else v for k, v in attr.items()}


def _attr_from_data(data):
    return {k: _generic_from_data_or_data(d) for k, d in data.items()}


class ProxyObject(object):
    """Base proxy class to create object proxies.

    An object proxy wraps the proxied object and forwards all calls to it
    unless a method/attribute/property is found first on the proxy itself.

    The magic part is ``__getattr__`` ."""

    def __init__(self, obj):
        self._proxied_object = obj

    def __getattr__(self, attr):
        return getattr(self._proxied_object, attr)

    def __str__(self):
        return str(self._proxied_object)

    def __repr__(self):
        return repr(self._proxied_object)

    @classmethod
    def create_proxy(cls, obj):
        """Creates a proxy wrapping around an object, only if it's not already proxied."""
        if obj and not isinstance(obj, cls):
            return cls(obj)
        return obj


class FrameProxy(ProxyObject):
    """Proxy class that adds URDF functionality to an instance of :class:`Frame`.

    This class is internal and not intended to be referenced externally.
    """

    def get_urdf_element(self):
        attributes = {
            "xyz": "{} {} {}".format(self.point.x, self.point.y, self.point.z),
            "rpy": "{} {} {}".format(*self.euler_angles()),
        }
        return URDFElement("origin", attributes)

    @classmethod
    def from_urdf(cls, attributes, elements=None, text=None):
        """Create origin instance from an URDF element.

        Parameters
        ----------
        attributes : dict[str, Any]
            Attributes of the URDF element.
        elements: list[object], optional
            Children elements of the URDF element.
        text: str, optional
            Text content of the URDF element.

        Returns
        -------
        :class:`FrameProxy`
            Frame proxy instance.

        Examples
        --------
        >>> attributes = {'rpy': '0.0 1.57 0.0', 'xyz': '0.0 0.13 0.0'}
        >>> f = FrameProxy.from_urdf(attributes, [], None)
        >>> f
        Frame(Point(0.000, 0.130, 0.000), Vector(0.001, 0.000, -1.000), Vector(0.000, 1.000, 0.000))

        """
        xyz = _parse_floats(attributes.get("xyz", "0 0 0"))
        rpy = _parse_floats(attributes.get("rpy", "0 0 0"))
        return cls(Frame.from_euler_angles(rpy, static=True, axes="xyz", point=xyz))

    def scale(self, factor):
        """Scale the origin by a given factor.

        Parameters
        ----------
        factor : float
            Scale factor.

        Returns
        -------
        None

        Examples
        --------
        >>> o = FrameProxy(Frame([0, 0, 0], [1, 0, 0], [0, 1, 0]))
        >>> o.scale(10)

        """
        self.point = self.point * factor
