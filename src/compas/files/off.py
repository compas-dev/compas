from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
from compas import _iotools


class OFF(object):
    """Read and write files in OFF format.

    References
    ----------
    * http://shape.cs.princeton.edu/benchmark/documentation/off_format.html
    * http://www.geomview.org/docs/html/OFF.html
    * http://segeval.cs.princeton.edu/public/off_format.html

    See Also
    --------
    * :class:`OFFReader`
    * :class:`OFFWriter`

    """

    def __init__(self, filepath):
        self.filepath = filepath
        self._reader = None
        self._is_read = False
        self._writer = None

    def read(self):
        """Read and parse the contents of the file."""
        self._reader = OFFReader(self.filepath)
        self._reader.open()
        self._reader.pre()
        self._reader.read()
        self._reader.post()
        self._is_read = True

    def write(self, mesh, **kwargs):
        """Write a mesh to the file.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            The mesh.
        author : :obj:`str`, optional
            The author name to include in the header.
        email : :obj:`str`, optional
            The email of the author to include in the header.
        date : :obj:`str`, optional
            The date to include in the header.
        precision : :obj:`str`, optional
            COMPAS precision specification for parsing geometric data.
        """
        self._writer = OFFWriter(self.filepath, mesh, **kwargs)
        self._writer.write()

    @property
    def reader(self):
        """:class:`OFFReader` - A OFF file reader."""
        if not self._is_read:
            self.read()
        return self._reader


class OFFReader(object):
    """Class for reading raw geometric data from OFF files.

    Parameters
    ----------
    filepath : path string, file-like object or URL string
        A path, a file-like object or a URL pointing to a file.

    Notes
    -----
    The OFF reader currently only supports reading of vertices and faces of polygon meshes.
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.content = None
        self.vertices = []
        """List[List[:obj:`float`, :obj:`float`, :obj:`float`]] -
        List of lists of vertex coordinates.
        """
        self.faces = []
        """List[List[:obj:`int`] -
        List of lists of references to vertex coordinates.
        """
        self.v = 0
        self.f = 0
        self.e = 0

    def open(self):
        """Open the file and read its contents."""
        with _iotools.open_file(self.filepath, 'r') as f:
            self.content = f.readlines()

    def pre(self):
        """Pre-process the contents."""
        lines = []
        is_continuation = False
        needs_decode = None

        for line in self.content:
            # Check this only one time
            if needs_decode is None:
                needs_decode = hasattr(line, 'decode')
            if needs_decode:
                line = line.decode('utf-8')
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
        """Post-process the contents."""
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
    """Class for writing geometric data to a OBJ file.
    The parser converts the raw geometric data of the file
    into corresponding COMPAS geometry objects and data structures.

    Parameters
    ----------
    filepath : path string, file-like object or URL string
        A path, a file-like object or a URL pointing to a file.
    mesh : :class:`compas.datastructures.Mesh`
        Mesh to write to the file.
    author : :obj:`str`, optional
        The author name to include in the header.
    email : :obj:`str`, optional
        The email of the author to include in the header.
    date : :obj:`str`, optional
        The date to include in the header.
    precision : :obj:`str`, optional
        COMPAS precision specification for parsing geometric data.
    """

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
        """Write the meshes to the file."""
        with _iotools.open_file(self.filepath, 'w') as self.file:
            self.write_header()
            self.write_vertices()
            self.write_faces()

    def write_header(self):
        """Write the header info."""
        self.file.write("OFF\n")
        if self.author:
            self.file.write("# author: {}\n".format(self.author))
        if self.email:
            self.file.write("# email: {}\n".format(self.email))
        if self.date:
            self.file.write("# date: {}\n".format(self.date))
        self.file.write("{} {} {}\n".format(self.v, self.f, self.e))

    def write_vertices(self):
        """Write the vertices."""
        for key in self.mesh.vertices():
            x, y, z = self.mesh.vertex_coordinates(key)
            self.file.write(self.vertex_tpl.format(x, y, z))

    def write_faces(self):
        """Write the faces."""
        key_index = self.mesh.key_index()
        for fkey in self.mesh.faces():
            vertices = self.mesh.face_vertices(fkey)
            v = len(vertices)
            self.file.write("{0} {1}\n".format(v, " ".join([str(key_index[key]) for key in vertices])))
