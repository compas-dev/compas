from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from compas.utilities import geometric_key


__all__ = [
    'OFF',
    'OFFReader',
]


class OFF(object):
    """Read and write files in OFF format.

    References
    ----------
    * http://shape.cs.princeton.edu/benchmark/documentation/off_format.html
    * http://www.geomview.org/docs/html/OFF.html
    * http://segeval.cs.princeton.edu/public/off_format.html


    """
    def __init__(self, filepath):
        self.reader = OFFReader(filepath)


class OFFReader(object):
    """Read the contents of an *obj* file.

    Parameters
    ----------
    filepath : str
        Path to the file.

    Attributes
    ----------
    vertices : list
        Vertex coordinates.
    weights : list
        Vertex weights.
    textures : list
        Vertex textures.
    normals : list
        Vertex normals.
    points : list
        Point objects, referencing the list of vertices.
    lines : list
        Line objects, referencing the list of vertices.
    faces : list
        Face objects, referencing the list of vertices.
    curves : list
        Curves
    curves2 : list
        Curves
    surfaces : list
        Surfaces

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Bourke, P. *Object Files*.
           Available at: http://paulbourke.net/dataformats/obj/.

    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.content = None
        self.vertices = []
        self.faces = []
        self.v = 0
        self.f = 0
        self.e = 0
        self.open()
        self.pre()
        self.read()
        self.post()

    def open(self):
        if self.filepath.startswith('http'):
            resp = urlopen(self.filepath)
            self.content = iter(resp.read().decode('utf-8').split('\n'))
        else:
            with open(self.filepath, 'r') as fh:
                self.content = iter(fh.readlines())

    def pre(self):
        lines = []
        is_continuation = False
        for line in self.content:
            line = line.rstrip()
            if not line:
                continue
            if is_continuation:
                lines[-1] = lines[-1][:-2] + line
            else:
                lines.append(line)
            if line[-1] == '\\':
                is_continuation = True
            else:
                is_continuation = False
        self.content = iter(lines)

    def post(self):
        pass

    def read(self):
        """Read the contents of the file, line by line.

        OFF
        # comments

        v f e
        x y z
        ...
        x y z
        degree list of vertices

        """
        if not self.content:
            return

        header = next(self.content)
        if not header.lower() == 'off':
            return

        for line in self.content:
            if line.startswith('#'):
                continue

            parts = line.split()
            if not parts:
                continue

            if len(parts) == 3:
                self.v, self.f, self.e = int(parts[0]), int(parts[1]), int(parts[2])
                break

        for line in self.content:
            parts = line.split()
            if not parts:
                continue

            if len(parts) == 3:
                self.vertices.append([float(axis) for axis in parts])
                continue

            if len(parts) > 3:
                f = int(parts[0])
                if f == len(parts[1:]):
                    self.faces.append([int(index) for index in parts[1:]])
                continue



# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas

    off = OFF(compas.get('cube.off'))

    print(off.reader.vertices)
    print(off.reader.faces)
