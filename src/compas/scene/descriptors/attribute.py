class Attribute:
    """Base descriptor storing a default value.

    Parameters
    ----------
    default
        The descriptor's default value.

    """

    def __init__(self, default: object = None) -> None:
        super().__init__()
        self.default = default

    def __set_name__(self, owner: type[object], name: str) -> None:
        """Record the public and private attribute names.

        Parameters
        ----------
        owner
            The class owning the attribute.
        name
            The name of the attribute.

        """
        self.name = name
        self.private_name = "_" + name
