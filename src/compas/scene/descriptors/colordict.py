import compas

if compas.PY2:
    from collections import Mapping
else:
    from collections.abc import Mapping
from compas.colors.colordict import ColorDict


class ColorDictAttribute(object):
    """Descriptor for color dictionaries."""

    def __init__(self, default=None, **kwargs):
        super(ColorDictAttribute, self).__init__(**kwargs)
        self.default = default

    def __set_name__(self, owner, name):
        """Record the name of the attribute this descriptor is assigned to.
        The attribute name is then used to identify the corresponding private attribute.

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
        self.name = name
        self.private_name = "_" + name

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

        if not hasattr(obj, self.private_name):
            setattr(obj, self.private_name, None)

        colordict = getattr(obj, self.private_name)

        if colordict is None:
            colordict = ColorDict(default=self.default)
            setattr(obj, self.private_name, colordict)

        return colordict

    def __set__(self, obj, value):
        """Set a new value for the descriptor.

        Parameters
        ----------
        obj : object
            The owner of the descriptor.
        value : dict[Any, :class:`compas.colors.Color`] | :class:`compas.colors.Color`
            The new value for the descriptor.
            This value is stored in the corresponding private attribute in the form of a defaultdict.

        Returns
        -------
        None

        """
        if not value:
            return

        colordict = getattr(obj, self.name)

        if isinstance(value, Mapping):
            colordict.clear()
            colordict.update(value)

        elif isinstance(value, ColorDict):
            colordict.clear()
            colordict.default = value.default
            colordict.update(value)

        else:
            colordict.clear()
            colordict.default = value
