from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import struct

import compas
from compas import _iotools


class PLY(object):
    """Class for working with files in Polygon format, also known as Stanford triangle format.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.
    precision : str, optional
        A COMPAS precision specification.

    Attributes
    ----------
    filepath : str
        The path to the file.
    precision : str
        A COMPAS precision specification.
    reader : :class:`PLYReader`
        A PLY file reader.
    parser : :class:`PLYParser`
        A PLY data parser.

    References
    ----------
    * http://paulbourke.net/dataformats/ply/

    """

    def __init__(self, filepath, precision=None):
        self.filepath = filepath
        self.precision = precision
        self._is_parsed = False
        self._reader = None
        self._parser = None
        self._writer = None

    @property
    def reader(self):
        if not self._is_parsed:
            self.read()
        return self._reader

    @property
    def parser(self):
        if not self._is_parsed:
            self.read()
        return self._parser

    def read(self):
        """Read the contents of the file.

        Returns
        -------
        None

        """
        self._reader = PLYReader(self.filepath)
        self._parser = PLYParser(self._reader, precision=self.precision)
        self._is_parsed = True

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
        self._writer = PLYWriter(self.filepath, mesh, **kwargs)
        self._writer.write()


class PLYReader(object):
    """Class for reading raw geometric data from PLY files.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.

    Attributes
    ----------
    filepath : str
        The path to the file.
    file : file
        The file object.
    format : str
        The format of the file.
    comments : list
        The comments in the header.
    header : list
        The lines of the header.
    start_header : int
        The number o the line containing the start of the header.
    end_header : int
        The number o the line containing the end of the header.
    number_of_vertices : int
        The number of vertices in the file.
    number_of_edges : int
        The number of edges in the file.
    number_of_faces : int
        The number of faces in the file.
    vertex_properties : list[tuple]
        The vertex properties.
        Each property is a tuple of the property name and the property type.
    edge_properties : list[tuple]
        The edge properties.
        Each property is a tuple of the property name and the property type.
    face_properties : list
        The face properties.
        Each property is a tuple of the property name and the property type.
    sections : list
        The sections in the file.
        Possible sections are ``vertex``, ``edge`` and ``face``.
    vertices : list
        The vertices found in the file.
        Each vertex is a dictionary of property names and property values.
    edges : list
        The edges found in the file.
        Each edge is a dictionary of property names and property values.
    faces : list
        The faces found in the file.
        Each face is a dictionary of property names and property values.

    """

    keywords = ["ply", "format", "comment", "element", "property", "end_header"]

    property_types = {
        "char": int,
        "uchar": int,
        "short": int,
        "ushort": int,
        "int": int,
        "int32": int,
        "int64": int,
        "uint": int,
        "uint32": int,
        "uint64": int,
        "float": float,
        "float32": float,
        "float64": float,
        "double": float,
    }

    binary_property_types = {
        "int8": "i1",
        "char": "i1",
        "uint8": "u1",
        "uchar": "u1",
        "int16": "i2",
        "short": "i2",
        "uint16": "u2",
        "ushort": "u2",
        "int32": "i4",
        "int": "i4",
        "uint32": "u4",
        "uint": "u4",
        "float32": "f4",
        "float": "f4",
        "float64": "f8",
        "double": "f8",
    }

    number_of_bytes_per_type = {
        "char": 1,
        "uchar": 1,
        "short": 2,
        "ushort": 2,
        "int": 4,
        "uint": 4,
        "float": 4,
        "double": 8,
    }

    struct_format_per_type = {
        "char": "c",
        "uchar": "B",
        "short": "h",
        "ushort": "H",
        "int": "i",
        "uint": "I",
        "float": "f",
        "double": "d",
    }

    binary_byte_order = {"binary_big_endian": ">", "binary_little_endian": "<"}

    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None
        self.format = None
        self.comments = []
        self.header = []
        self.start_header = None
        self.end_header = None
        self.number_of_vertices = 0
        self.number_of_edges = 0
        self.number_of_faces = 0
        self.vertex_properties = []
        self.edge_properties = []
        self.face_properties = []
        self.sections = []
        self.vertices = []
        self.edges = []
        self.faces = []
        self.read()

    def is_valid(self):
        """Verify that the file is valid by reading the header.

        Returns
        -------
        bool

        """
        self._read_header()
        if self.start_header and self.end_header:
            return True
        return False

    def is_binary(self):
        """Verify that the file is in binary format.

        Returns
        -------
        bool

        """
        if self.format == "binary_big_endian":
            return True
        if self.format == "binary_little_endian":
            return True
        return False

    def is_ascii(self):
        """Verify that the file is in ASCII format.

        Returns
        -------
        bool

        """
        if self.format == "ascii":
            return True
        return False

    def read(self):
        """Read the contents of the file.

        Returns
        -------
        None

        """
        self._read_header()
        if self.format == "ascii":
            self._read_data()
        else:
            self._read_data_binary()

    # ==========================================================================
    # read the header
    # ==========================================================================

    def _read_header(self):
        # the header is always in ascii format
        # read it as text
        # otherwise file.tell() can't be used reliably
        # to figure out where the header ends
        with _iotools.open_file(self.filepath) as file:
            file.seek(0)

            line = file.readline().rstrip()

            if line.lower() != "ply":
                raise Exception("not a valid ply file")

            self.start_header = file.tell()

            element_type = None

            while True:
                line = file.readline()
                line = line.rstrip()

                self.header.append(line)

                if line.startswith("format"):  # type: ignore
                    element_type = None
                    self.format = line[len("format") + 1 :].split()[0]

                elif line.startswith("comment"):  # type: ignore
                    element_type = None
                    self.comments.append(line[len("comment") + 1 :])

                elif line.startswith("element"):  # type: ignore
                    parts = line.split()
                    element_type = parts[1]
                    if element_type == "vertex":
                        self.sections.append("vertex")
                        self.number_of_vertices = int(parts[2])
                    elif element_type == "edge":
                        self.sections.append("edge")
                        self.number_of_edges = int(parts[2])
                    elif element_type == "face":
                        self.sections.append("face")
                        self.number_of_faces = int(parts[2])
                    else:
                        element_type = None
                        raise Exception

                elif line.startswith("property"):  # type: ignore
                    parts = line.split()
                    if element_type == "vertex":
                        property_type = parts[1]
                        property_name = parts[2]
                        self.vertex_properties.append((property_name, property_type))
                    elif element_type == "edge":
                        property_type = parts[1]
                        property_name = parts[2]
                        self.edge_properties.append((property_name, property_type))
                    elif element_type == "face":
                        property_type = parts[1]
                        if property_type == "list":
                            property_length = parts[2]
                            property_type = parts[3]
                            property_name = parts[4]
                            self.face_properties.append((property_name, property_type, property_length))
                        else:
                            property_type = parts[1]
                            property_name = parts[2]
                            self.face_properties.append((property_name, property_type))
                    else:
                        element_type = None
                        raise Exception

                elif line == "end_header":
                    element_type = None
                    self.end_header = file.tell()
                    break

                else:
                    pass

    # ==========================================================================
    # read the data
    # ==========================================================================

    def _read_data(self):
        if not self.end_header:
            raise Exception("header has not been read, or the file is not valid")
        with _iotools.open_file(self.filepath) as self.file:
            self.file.seek(self.end_header)
            for section in self.sections:
                if section == "vertex":
                    self._read_vertices()
                elif section == "edge":
                    self._read_edges()
                elif section == "face":
                    self._read_faces()
                else:
                    print("user-defined elements are not supported: {0}".format(section))
                    pass

    def _read_data_binary(self):
        if not self.end_header:
            raise Exception("header has not been read, or the file is not valid")
        with _iotools.open_file(self.filepath, "rb") as self.file:
            self.file.seek(self.end_header)
            for section in self.sections:
                if section == "vertex":
                    self._read_vertices_binary_wo_numpy()
                elif section == "edge":
                    self._read_edges_binary_wo_numpy()
                elif section == "face":
                    self._read_faces_binary_wo_numpy()
                else:
                    print("user-defined elements are not supported: {0}".format(section))
                    pass

    # ==========================================================================
    # read the individual section
    # ==========================================================================

    def _read_vertices(self):
        n = len(self.vertex_properties)
        for _ in range(self.number_of_vertices):
            vertex = {}
            i = 0
            while i < n:
                line = next(self.file)
                parts = line.rstrip().split()
                for prop_str in parts:
                    prop_name, prop_type = self.vertex_properties[i]
                    vertex[prop_name] = self.property_types[prop_type](prop_str)
                    i += 1
            self.vertices.append(vertex)
        # count = 0
        # for line in self.file:
        #     line = line.rstrip()
        #     parts = line.split()
        #     vertex = {}
        #     for i, prop in enumerate(self.vertex_properties):
        #         pname, ptype = prop
        #         vertex[pname] = self.property_types[ptype](parts[i])
        #     self.vertices.append(vertex)
        #     count += 1
        #     if count == self.number_of_vertices:
        #         break

    def _read_edges(self):
        pass

    def _read_faces(self):
        count = 0
        for line in self.file:
            line = line.rstrip()
            parts = line.split()
            face = {}
            for i, prop in enumerate(self.face_properties):
                pname, ptype, plen = prop
                face[pname] = [self.property_types[ptype](part) for part in parts[1:]]
            self.faces.append(face)
            count += 1
            if count == self.number_of_faces:
                break

    # ==========================================================================
    # binary read the individual section
    # ==========================================================================

    # remove numpy dependency by reading the file in chuncks
    # with each chunck equal to the size specified in the header?
    # see: http://stackoverflow.com/questions/4566498/python-file-iterator-over-a-binary-file-with-newer-idiom
    # see: http://stackoverflow.com/questions/27532738/python-iterate-through-binary-file-without-lines

    def _numpy_vertex_ptypes(self):
        ext = self.binary_byte_order[self.format]
        dt = []
        for prop in self.vertex_properties:
            pname, ptype = prop
            dt.append((pname, ext + self.binary_property_types[ptype]))
        return dt

    def _numpy_face_ptypes(self):
        ext = self.binary_byte_order[self.format]
        dt = []
        for prop in self.face_properties:
            if len(prop) == 2:
                pname, ptype = prop
                dt.append((pname, ext + self.binary_property_types[ptype]))
            elif len(prop) == 3:
                pname, ptype, plen = prop
                dt.append(("size", ext + self.binary_property_types[plen]))
                # this seems a nit of a hack
                dt.append(("v1", ext + self.binary_property_types[ptype]))
                dt.append(("v2", ext + self.binary_property_types[ptype]))
                dt.append(("v3", ext + self.binary_property_types[ptype]))
            else:
                pass
        return dt

    def _read_vertices_binary_wo_numpy(self):
        ext = self.binary_byte_order[self.format]
        fmt = ext
        chunk = 0
        for prop in self.vertex_properties:
            pname, ptype = prop
            chunk += self.number_of_bytes_per_type[ptype]
            fmt += self.struct_format_per_type[ptype]
        for i in range(self.number_of_vertices):
            data = self.file.read(chunk)
            data = struct.unpack(fmt, data)
            vertex = {}
            for i, prop in enumerate(self.vertex_properties):
                pname, ptype = prop
                vertex[pname] = data[i]
            self.vertices.append(vertex)

    def _read_vertices_binary(self):
        # use pandas to read the data frames
        import numpy as np

        for line in np.fromfile(
            self.file,
            dtype=np.dtype(self._numpy_vertex_ptypes()),
            count=self.number_of_vertices,
        ):
            vertex = {}
            for i, prop in enumerate(self.vertex_properties):
                pname, ptype = prop
                vertex[pname] = line[i]
            self.vertices.append(vertex)

    def _read_edges_binary_wo_numpy(self):
        pass

    def _read_edges_binary(self):
        pass

    def _read_faces_binary_wo_numpy(self):
        ext = self.binary_byte_order[self.format]
        fmt = ext
        chunk = 0
        for prop in self.face_properties:
            if len(prop) == 2:
                pname, ptype = prop
                chunk += self.number_of_bytes_per_type[ptype]
                fmt += self.struct_format_per_type[ptype]
            elif len(prop) == 3:
                pname, ptype, plen = prop
                chunk += self.number_of_bytes_per_type[plen]
                chunk += self.number_of_bytes_per_type[ptype] * 3
                fmt += self.struct_format_per_type[plen]
                fmt += self.struct_format_per_type[ptype] * 3
            else:
                pass
        for i in range(self.number_of_faces):
            data = self.file.read(chunk)
            data = struct.unpack(fmt, data)
            face = {}
            for i, prop in enumerate(self.face_properties):
                if len(prop) == 2:
                    pname, ptype = prop
                    face[pname] = data[i]
                elif len(prop) == 3:
                    pname, ptype, plen = prop
                    face[pname] = list(data[2:])
            self.faces.append(face)

    def _read_faces_binary(self):
        # use pandas to read the data frames
        # how to deal with faces of variable length?
        import numpy as np

        for line in np.fromfile(
            self.file,
            dtype=np.dtype(self._numpy_face_ptypes()),
            count=self.number_of_faces,
        ):
            face = {}
            for i, prop in enumerate(self.face_properties):
                if len(prop) == 2:
                    pname, ptype = prop
                    face[pname] = line[i]
                elif len(prop) == 3:
                    pname, ptype, plen = prop
                    # type(line) => numpy.void
                    # convert the line to a list
                    line = list(line)
                    face[pname] = line[2:]
                else:
                    pass
            self.faces.append(face)


class PLYParser(object):
    """Class for parsing data from a OBJ file.

    The parser converts the raw geometric data of the file
    into corresponding COMPAS geometry objects and data structures.

    Parameters
    ----------
    reader : :class:`PLYReader`
        A PLY file reader.
    precision : str
        COMPAS precision specification for parsing geometric data.

    Attributes
    ----------
    vertices : list[tuple[float, float, float]]
        The vertex coordinates.
    edges : list[tuple[int, int]]
        Pairs of vertex indices defining the start and end points of edges.
    faces : list[list[int]]
        Lists of vertex indices defining faces.

    """

    def __init__(self, reader, precision=None):
        self.precision = precision
        self.reader = reader
        self.vertices = None
        self.edges = None
        self.faces = None
        self.parse()

    def parse(self):
        """Parse the contents found by a PLY file reader.

        Returns
        -------
        None

        """
        self.vertices = [(vertex["x"], vertex["y"], vertex["z"]) for vertex in self.reader.vertices]
        self.faces = [face["vertex_indices"] for face in self.reader.faces]


class PLYWriter(object):
    """Class for writing geometric data to a PLY file.

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
        """Write the data to a file.

        Returns
        -------
        None

        """
        with _iotools.open_file(self.filepath, "w") as self.file:
            self._write_header()
            self._write_vertices()
            self._write_faces()

    def _write_header(self):
        self.file.write("PLY\n")
        self.file.write("format ascii 1.0\n")
        if self.author:
            self.file.write("comment author: {}\n".format(self.author))
        if self.email:
            self.file.write("comment email: {}\n".format(self.email))
        if self.date:
            self.file.write("comment date: {}\n".format(self.date))
        self.file.write("element vertex {}\n".format(self.v))
        self.file.write("property float x\n")
        self.file.write("property float y\n")
        self.file.write("property float z\n")
        self.file.write("element face {}\n".format(self.f))
        self.file.write("property list uchar int vertex_indices\n")
        self.file.write("end_header\n")

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
