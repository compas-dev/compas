from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.files.base_reader import BaseReader

__all__ = [
    'OFF',
    'OFFReader',
]


class OFF(object):
    """Read and write files in *OFF* format.

    Notes
    -----
    GeomView Object File Format

    References
    ----------
    * http://shape.cs.princeton.edu/benchmark/documentation/off_format.html
    * http://www.geomview.org/docs/html/OFF.html
    * http://segeval.cs.princeton.edu/public/off_format.html

    """
    def __init__(self, filepath):
        self.reader = OFFReader(filepath)


class OFFReader(BaseReader):
    """Read the contents of an *off* file.
    Arguments
    ---------
    location: str or Path object
        Path or URL to the file.

    Attributes
    ----------
    vertices : list
        Vertex coordinates.
    faces : list
        Face objects, referencing the list of vertices.
    vertex_count : int
        Vertex count stated in beginning of file
    face_count : int
        Face count stated in beginning of file
    edge_count : int
        Edge count stated in beginning of file

    """
    file_signature = {
                      'content': b'OFF',
                      'offset': 0,
    }

    def __init__(self, location):
        super(OFFReader, self).__init__(location)
        self.vertices = []
        self.faces = []
        self.vertex_count = 0
        self.face_count = 0
        self.edge_count = 0
        self.pre()
        self.read_off()
        self.post()

    def pre(self):
        self.check_file_signature()

        lines = []
        is_continuation = False
        for line in self.read():
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

    def read_off(self):
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
            raise Exception('Import failed')

        for line in self.content:
            if line.startswith('#'):
                continue

            parts = line.split()
            if not parts:
                continue

            if len(parts) == 3:
                self.vertex_count, self.face_count, self.edge_count = \
                    int(parts[0]), int(parts[1]), int(parts[2])
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
