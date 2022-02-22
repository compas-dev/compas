from collections import defaultdict
from compas.colors import Color


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
        self.public_name = name
        self.private_name = '_' + name
        self.default_name = 'default_' + ''.join(name.split('_'))

    def __get__(self, obj, otype=None):
        return getattr(obj, self.private_name) or defaultdict(lambda: getattr(obj, self.default_name))

    def __set__(self, obj, value):
        if not value:
            return

        if isinstance(value, dict):
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
