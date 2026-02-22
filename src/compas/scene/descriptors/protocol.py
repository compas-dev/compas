class DescriptorProtocol(type):
    """Meta class to provide support for the descriptor protocol in Python versions lower than 3.6"""

    def __init__(cls, name, bases, attrs):
        for key, value in iter(attrs.items()):
            if hasattr(value, "__set_name__"):
                value.__set_name__(cls, key)
