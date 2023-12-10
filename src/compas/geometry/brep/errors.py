class BrepError(Exception):
    """Represents a generic error in the Brep context"""

    pass


class BrepInvalidError(BrepError):
    """Raised when the process of re-constructing a Brep has resulted in an invalid Brep"""

    pass


class BrepTrimmingError(BrepError):
    """Raised when a trimming operation has failed or had not result"""

    pass


class BrepFilletError(BrepError):
    """Raised when a fillet operation has failed or had not result"""

    pass
