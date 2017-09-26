import socket


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['MayaSocket', ]


class MayaSocketError(Exception):
    pass


# see: http://download.autodesk.com/us/maya/2011help/CommandsPython/commandPort.html
# see: http://stackoverflow.com/questions/6485059/sending-multiline-commands-to-maya-through-python-socket
# see: https://docs.python.org/3/howto/sockets.html

class MayaSocket(object):
    """Communicate with Maya through a socket connection."""

    def __init__(self):
        pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
