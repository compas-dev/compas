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
                color = value[item]
                if Color.is_rgb255(color):
                    color = Color.from_rgb255(color[0], color[1], color[2])
                elif Color.is_hex(color):
                    color = Color.from_hex(color)
                else:
                    color = Color(color[0], color[1], color[2])
                item_color[item] = color
            setattr(obj, self.private_name, item_color)

        else:
            if Color.is_rgb255(value):
                color = Color.from_rgb255(value[0], value[1], value[2])
            elif Color.is_hex(value):
                color = Color.from_hex(value)
            else:
                color = Color(value[0], value[1], value[2])
            setattr(obj, self.private_name, defaultdict(lambda: color))
