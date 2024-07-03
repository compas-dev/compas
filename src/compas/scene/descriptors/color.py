from compas.colors import Color


class ColorAttribute(object):
    """A descriptor for color attributes.

    Parameters
    ----------
    default : :class:`compas.colors.Color`, optional
        The default value of the attribute.
        Default is ``None``.

    """

    def __init__(self, default=None, **kwargs):
        super(ColorAttribute, self).__init__(**kwargs)
        self.default = Color.coerce(default)

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
        """Get the color stored in the private attribute corresponding to the public attribute name of the descriptor.

        Parameters
        ----------
        obj : object
            The instance owning the instance of the descriptor.
        otype : object, optional
            The type owning the instance of the descriptor.

        Returns
        -------
        :class:`compas.colors.Color`
            The color stored in the private attribute corresponding to the public attribute name of the descriptor.
            If the private attribute does not exist, the default value of the descriptor is returned.

        """
        if not hasattr(obj, self.private_name):
            setattr(obj, self.private_name, None)

        color = getattr(obj, self.private_name)

        if color is None:
            color = Color.coerce(self.default)
            setattr(obj, self.private_name, color)

        return color

    def __set__(self, obj, value):
        """Set a new value for the descriptor.

        Parameters
        ----------
        obj : object
            The owner of the descriptor.
        value : :class:`compas.colors.Color`
            The new value for the descriptor.
            This value is stored in the corresponding private attribute.

        Returns
        -------
        None

        """
        if not value:
            return

        setattr(obj, self.private_name, Color.coerce(value))
