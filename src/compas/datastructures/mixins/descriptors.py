__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'VertexCoordinatesDescriptors',
]


class VertexCoordinatesDescriptors(object):

    @property
    def xyz(self):
        """list: The XYZ coordinates of the vertices."""
        return [(a['x'], a['y'], a['z']) for k, a in self.vertices(True)]

    @property
    def xy(self):
        """list: The XY coordinates of the vertices."""
        return [(a['x'], a['y']) for k, a in self.vertices(True)]

    @property
    def x(self):
        """list: The X coordinates of the vertices."""
        return [a['x'] for k, a in self.vertices(True)]

    @property
    def y(self):
        """list: The Y coordinates of the vertices."""
        return [a['y'] for k, a in self.vertices(True)]

    @property
    def z(self):
        """list: The Z coordinates of the vertices."""
        return [a['z'] for k, a in self.vertices(True)]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
