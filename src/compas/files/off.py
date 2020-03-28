from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import compas


__all__ = [
    'OFF',
    'OFFReader',
    'OFFWriter',
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
        self.filepath = filepath
        self._reader = None
        self._is_read = False
        self._writer = None

    def read(self):
        self._reader = OFFReader(self.filepath)
        self._reader.open()
        self._reader.pre()
        self._reader.read()
        self._reader.post()
        self._is_read = True

    def write(self, mesh, **kwargs):
        self._writer = OFFWriter(self.filepath, mesh, **kwargs)
        self._writer.write()

    @property
    def reader(self):
        if not self._is_read:
            self.read()
        return self._reader


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
    faces : list
        Face objects, referencing the list of vertices.

    Notes
    -----
    The OFF reader currently only supports reading of vertices and faces of polygon meshes.

    References
    ----------

    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.content = None
        self.vertices = []
        self.faces = []
        self.v = 0
        self.f = 0
        self.e = 0

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

        while len(self.vertices) < self.v:
            line = next(self.content)
            parts = line.split()
            if parts:
                self.vertices.append([float(axis) for axis in parts[:3]])

        while len(self.faces) < self.f:
            line = next(self.content)
            parts = line.split()
            if parts:
                f = int(parts[0])
                face = [int(index) for index in parts[1:f + 1]]
                # if len(parts[1:]) >= f:
                #     face = [int(index) for index in parts[1:f + 1]]
                # else:
                #     # add support for color info
                #     face = [int(index) for index in parts[1:]]
                #     while len(face) < f:
                #         line = next(self.content)
                #         line = line.strip()
                #         if not line:
                #             break
                #         parts = line.split()
                #         if not parts:
                #             break
                #         face += [int(index) for index in parts]
                if len(face) == f:
                    self.faces.append(face)


class OFFWriter(object):

    def __init__(self, filepath, mesh, author=None, email=None, date=None, precision=None):
        self.filepath = filepath
        self.mesh = mesh
        self.author = author
        self.email = email
        self.date = date
        self.precision = precision or compas.PRECISION
        self.vertex_tpl = "{0:." + self.precision + "}" + " {1:." + self.precision + "}" + " {2:." + self.precision + "}\n"
        self.v = mesh.number_of_vertices()
        self.f = mesh.number_of_faces()
        self.e = mesh.number_of_edges()
        self.file = None

    def write(self):
        with open(self.filepath, 'w') as self.file:
            self.write_header()
            self.write_vertices()
            self.write_faces()

    def write_header(self):
        self.file.write("OFF\n")
        if self.author:
            self.file.write("# author: {}\n".format(self.author))
        if self.email:
            self.file.write("# email: {}\n".format(self.email))
        if self.date:
            self.file.write("# date: {}\n".format(self.date))
        self.file.write("{} {} {}\n".format(self.v, self.f, self.e))

    def write_vertices(self):
        for key in self.mesh.vertices():
            x, y, z = self.mesh.vertex_coordinates(key)
            self.file.write(self.vertex_tpl.format(x, y, z))

    def write_faces(self):
        key_index = self.mesh.key_index()
        for fkey in self.mesh.faces():
            vertices = self.mesh.face_vertices(fkey)
            v = len(vertices)
            self.file.write("{0} {1}\n".format(v, " ".join([str(key_index[key]) for key in vertices])))


# ==============================================================================
# Main
# ==============================================================================
if __name__ == '__main__':

    import os
    from compas.datastructures import Mesh

    FILE = os.path.join(compas.DATA, 'tubemesh.off')

    mesh = Mesh.from_json(compas.get('tubemesh.json'))
    mesh.to_off(FILE, author="Tom Van Mele")

    off = OFF(FILE)
    print(len(off.reader.vertices) == off.reader.v)
    print(len(off.reader.faces) == off.reader.f)
