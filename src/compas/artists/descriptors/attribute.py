class Attribute(object):
    """Descriptor for text dictionaries."""

    def __init__(self, default=None, **kwargs):
        super(Attribute, self).__init__(**kwargs)
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
