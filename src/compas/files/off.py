from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
from compas import _iotools


class OFF(object):
    """Class for working with OFF files.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.

    Attributes
    ----------
    reader : :class:`OFFReader`, read-only
        A OFF file reader.

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

    @property
    def reader(self):
        if not self._is_read:
            self.read()
        return self._reader

    def read(self):
        """Read and parse the contents of the file.

        Returns
        -------
        None

        """
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
        author : str, optional
            The author name to include in the header.
        email : str, optional
            The email of the author to include in the header.
        date : str, optional
            The date to include in the header.
        precision : str, optional
            COMPAS precision specification for parsing geometric data.

        Returns
        -------
        None

        """
        self._writer = OFFWriter(self.filepath, mesh, **kwargs)
        self._writer.write()


class OFFReader(object):
    """Class for reading raw geometric data from OFF files.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.

    Attributes
    ----------
    vertices : list[list[float, float, float]]
        List of lists of vertex coordinates.
    faces : list[list[int]
        List of lists of references to vertex coordinates.

    Notes
    -----
    The OFF reader currently only supports reading of vertices and faces of polygon meshes.

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
        """Open the file and read its contents.

        Returns
        -------
        None

        """
        with _iotools.open_file(self.filepath, "r") as f:
            self.content = f.readlines()

    def pre(self):
        """Pre-process the contents.

        Returns
        -------
        None

        """
        lines = []
        is_continuation = False
        needs_decode = None

        for line in self.content:
            # Check this only one time
            if needs_decode is None:
                needs_decode = hasattr(line, "decode")
            if needs_decode:
                line = line.decode("utf-8")
            line = line.rstrip()
            if not line:
                continue
            if is_continuation:
                lines[-1] = lines[-1][:-2] + line
            else:
                lines.append(line)
            if line[-1] == "\\":
                is_continuation = True
            else:
                is_continuation = False
        self.content = iter(lines)

    def post(self):
        """Post-process the contents.

        Returns
        -------
        None

        """
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

        Returns
        -------
        None

        """
        if not self.content:
            return

        header = next(self.content)
        if not header.lower() == "off":
            return

        for line in self.content:
            if line.startswith("#"):
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
                face = [int(index) for index in parts[1 : f + 1]]
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

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.
    mesh : :class:`compas.datastructures.Mesh`
        Mesh to write to the file.
    author : str, optional
        The author name to include in the header.
    email : str, optional
        The email of the author to include in the header.
    date : str, optional
        The date to include in the header.
    precision : str, optional
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
        """Write the meshes to the file.

        Returns
        -------
        None

        """
        with _iotools.open_file(self.filepath, "w") as self.file:
            self._write_header()
            self._write_vertices()
            self._write_faces()

    def _write_header(self):
        self.file.write("OFF\n")
        if self.author:
            self.file.write("# author: {}\n".format(self.author))
        if self.email:
            self.file.write("# email: {}\n".format(self.email))
        if self.date:
            self.file.write("# date: {}\n".format(self.date))
        self.file.write("{} {} {}\n".format(self.v, self.f, self.e))

    def _write_vertices(self):
        for key in self.mesh.vertices():
            x, y, z = self.mesh.vertex_coordinates(key)
            self.file.write(self.vertex_tpl.format(x, y, z))

    def _write_faces(self):
        vertex_index = self.mesh.vertex_index()
        for face in self.mesh.faces():
            vertices = self.mesh.face_vertices(face)
            v = len(vertices)
            self.file.write("{0} {1}\n".format(v, " ".join([str(vertex_index[vertex]) for vertex in vertices])))
