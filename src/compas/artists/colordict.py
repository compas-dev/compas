import compas
from collections import defaultdict

if compas.PY2:
    from collections import Mapping
else:
    from collections.abc import Mapping
from compas.colors import Color


class DescriptorProtocol(type):
    """Meta class to provide support for the descriptor protocol in Python versions lower than 3.6"""

    def __init__(cls, name, bases, attrs):
        for k, v in iter(attrs.items()):
            if hasattr(v, "__set_name__"):
                v.__set_name__(cls, k)


class ColorDict(object):
    """Descriptor for color dictionaries.

    To use this descriptor, some requirements need to be fulfilled.

    The descriptor should be assigned to a class attribute
    that has a protected counterpart that will hold the actual dictionary values,
    and a corresponding attribute that defines the default value for missing colors.
    Both the protected attribute and the default attribute should follow a specific naming convention.

    For example, to create the property ``vertex_color`` on a ``MeshArtist``,
    the ``MeshArtist`` should have ``self._vertex_color`` for storing the actual dictionary values,
    and ``self.default_vertexcolor`` for storing the replacement value for missing entries in the dict.

    The descriptor will then ensure that all values assigned to ``vertex_color`` will result in the creation
    of a ``defaultdict`` that always returns instances of ``compas.colors.Color``
    such that colors can be reliably converted between color spaces as needed, regardless of the input.

    """

    def __set_name__(self, owner, name):
        """Record the name of the attribute this descriptor is assigned to.
        The attribute name is then used to identify the corresponding private attribute, and the attribute containing a default value.

        Parameters
        ----------
        owner : object
            The class owning the attribute.
        name : str
            The name of the attribute.

        Returns
        -------
        None

        Notes
        -----
        In Python 3.6+ this method is called automatically.
        For earlier versions it needs to be used with a custom metaclass (``DescriptorProtocol``).

        """
        self.public_name = name
        self.private_name = "_" + name
        self.default_name = "default_" + "".join(name.split("_"))

    def __get__(self, obj, otype=None):
        """Get the color dict stored in the private attribute corresponding to the public attribute name of the descriptor.

        Parameters
        ----------
        obj : object
            The instance owning the instance of the descriptor.
        otype : object, optional
            The type owning the instance of the descriptor.

        Returns
        -------
        defaultdict
            A defaultdict with the value stored in the default attribute corresponding to the descriptor as a default value.

        """
        default = getattr(obj, self.default_name)
        d = getattr(obj, self.private_name)
        if d is not None:
            return d
        return defaultdict(lambda: default)

    def __set__(self, obj, value):
        """Set a new value for the descriptor.

        Parameters
        ----------
        obj : object
            The owner of the descriptor.
        value : dict[Any, :class:`~compas.colors.Color`] | :class:`~compas.colors.Color`
            The new value for the descriptor.
            This value is stored in the corresponding private attribute in the form of a defaultdict.

        Returns
        -------
        None

        """
        if not value:
            return

        if isinstance(value, Mapping):
            default = getattr(obj, self.default_name)
            item_color = defaultdict(lambda: default)
            for item in value:
                color = Color.coerce(value[item])
                if color:
                    item_color[item] = color
            setattr(obj, self.private_name, item_color)

        else:
            color = Color.coerce(value)
            setattr(obj, self.private_name, defaultdict(lambda: color))
