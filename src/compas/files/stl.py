from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import struct

from compas import _iotools
from compas.geometry import Translation
from compas.tolerance import TOL


class STL(object):
    """Class for working with STL files.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.
    precision : int, optional
        Precision for converting numbers to strings.
        Default is :attr:`TOL.precision`.

    Attributes
    ----------
    reader : :class:`STLReader`
        A STL file reader.
    parser : :class:`STLParser`
        A STL file parser.

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
        """Read and parse the contents of the file.

        Returns
        -------
        None

        """
        self._reader = STLReader(self.filepath)
        self._parser = STLParser(self._reader, precision=self.precision)
        self._is_parsed = True

    def write(self, mesh, **kwargs):
        """Write a mesh to the file.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            The mesh.
        binary : bool, optional
            Flag indicating that the file should be written in binary format.
        solid_name : str, optional
            The name of the solid.
            Defaults to the name of the mesh.
        precision : str, optional
            COMPAS precision specification for parsing geometric data.

        Returns
        -------
        None

        """
        self._writer = STLWriter(self.filepath, mesh, **kwargs)
        self._writer.write()


class STLReader(object):
    """Class for reading raw geometric data from STL files.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.

    References
    ----------
    * http://paulbourke.net/dataformats/stl/

    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None
        self.header = None
        self.facets = []
        self.read()

    def read(self):
        """Read the data.

        Returns
        -------
        None

        """
        is_binary = False
        with _iotools.open_file(self.filepath, "rb") as file:
            line = file.readline().strip()
            if b"solid" in line:
                is_binary = False
            else:
                is_binary = True
        try:
            if not is_binary:
                self._read_ascii()
            else:
                self._read_binary()
        except Exception:
            # raise if it was already detected as binary, but failed anyway
            if is_binary:
                raise
            # else, ascii parsing failed, try binary
            is_binary = True
            self._read_binary()

    # ==========================================================================
    # ascii
    #
    # @see: https://en.wikipedia.org/wiki/STL_(file_format)
    #
    # solid name
    # facet normal ni nj nk
    #     outer loop
    #         vertex v1x v1y v1z
    #         vertex v2x v2y v2z
    #         vertex v3x v3y v3z
    #     endloop
    # endfacet
    # endsolid name
    #
    # ==========================================================================

    def _read_ascii(self):
        with _iotools.open_file(self.filepath, "r") as file:
            self.file = file
            self.file.seek(0)
            self.facets = self._read_solids_ascii()

    def _read_solids_ascii(self):
        if not self.file:
            return

        solids = {}
        facets = []

        while True:
            line = self.file.readline().strip()

            if not line:
                break

            parts = line.split()

            if parts[0] == "solid":
                if len(parts) == 2:
                    name = parts[1]
                else:
                    name = "solid"
                solids[name] = []

            elif parts[0] == "endsolid":
                name = None

            elif parts[0] == "facet":
                facet = {"normal": None, "vertices": None}
                if parts[1] == "normal":
                    facet["normal"] = [float(parts[i]) for i in range(2, 5)]

            elif parts[0] == "outer" and parts[1] == "loop":
                vertices = []

            elif parts[0] == "vertex":
                xyz = [float(parts[i]) for i in range(1, 4)]
                vertices.append(xyz)

            elif parts[0] == "endloop":
                facet["vertices"] = vertices

            elif parts[0] == "endfacet":
                solids[name].append(facet)
                facets.append(facet)

            # no known line start matches, maybe not ascii
            elif not parts[0].isalnum():
                raise RuntimeError("File is not ASCII")

        return facets

    # ==========================================================================
    # binary
    #
    # @see: https://en.wikipedia.org/wiki/STL_(file_format)
    #
    # UINT8[80] - Header
    # UINT32 - Number of triangles
    #
    # foreach triangle
    # REAL32[3] - Normal vector
    # REAL32[3] - Vertex 1
    # REAL32[3] - Vertex 2
    # REAL32[3] - Vertex 3
    # UINT16 - Attribute byte count
    # end
    #
    # ==========================================================================

    def _read_uint16(self):
        bytes_ = self.file.read(2)
        return struct.unpack("<H", bytes_)[0]

    def _read_uint32(self):
        bytes_ = self.file.read(4)
        return struct.unpack("<I", bytes_)[0]

    def _read_binary(self):
        with _iotools.open_file(self.filepath, "rb") as file:
            self.file = file
            self.file.seek(0)
            self.header = self._read_header_binary()
            self.facets = self._read_facets_binary()

    def _read_header_binary(self):
        bytes_ = self.file.read(80)
        return struct.unpack("80s", bytes_)[0]

    def _read_number_of_facets_binary(self):
        return self._read_uint32()

    def _read_facet_binary(self):
        # Read full facet at once
        # 4 bytes per float * 3 floats per vector/vertex * 4 items (1 vector + 3 vertices)
        bytes_ = self.file.read(48)
        floats_ = struct.unpack("<12f", bytes_)

        normal = floats_[0:3]
        vertices = (floats_[3:6], floats_[6:9], floats_[9:12])
        keys = (bytes_[12:24], bytes_[24:36], bytes_[36:48])

        # Skip two-byte attributes, it's not used anywhere (by anyone - on this planet)
        self.file.seek(2, 1)

        return {"normal": normal, "vertices": vertices, "keys": keys}

    def _read_facets_binary(self):
        facets = []
        n = self._read_number_of_facets_binary()
        for i in range(n):
            facets.append(self._read_facet_binary())
        return facets


class STLParser(object):
    """Class for parsing data from a STL file.

    The parser converts the raw geometric data of the file
    into corresponding COMPAS geometry objects and data structures.

    Parameters
    ----------
    reader : :class:`STLReader`
        A STL file reader.
    precision : str, optional
        COMPAS precision specification for parsing geometric data.

    Attributes
    ----------
    vertices : list[list[float]]
        The vertex coordinates.
    faces : list[list[int]]
        The faces as lists of vertex indices.

    """

    def __init__(self, reader, precision=None):
        self.precision = precision
        self.reader = reader
        self.vertices = None
        self.faces = None
        self.parse()

    def parse(self):
        """Parse the the data found by the reader.

        Returns
        -------
        None

        """
        gkey_index = {}
        vertices = []
        faces = []
        for facet in self.reader.facets:
            face = []
            facet_vertices = facet["vertices"]
            for i in range(3):
                xyz = facet_vertices[i]
                if "keys" in facet:
                    gkey = facet["keys"][i]
                else:
                    gkey = TOL.geometric_key(xyz, self.precision)
                if gkey not in gkey_index:
                    gkey_index[gkey] = len(vertices)
                    vertices.append(xyz)
                face.append(gkey_index[gkey])
            faces.append(face)
        self.vertices = vertices
        self.faces = faces


class STLWriter(object):
    """Class for writing geometric data to a STL file.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.
    mesh : :class:`compas.datastructures.Mesh`
        The mesh.
    binary : bool, optional
        Flag indicating that the file should be written in binary format.
    solid_name : str, optional
        The name of the solid.
        Defaults to the name of the mesh.
    precision : str, optional
        COMPAS precision specification for parsing geometric data.

    """

    def __init__(self, filepath, mesh, binary=False, solid_name=None, precision=None):
        self.filepath = filepath
        self.mesh = mesh
        self.solid_name = solid_name or mesh.name
        self.precision = precision
        self.file = None
        self.binary = binary

    @property
    def _vertex_xyz(self):
        bbox = self.mesh.aabb()
        xmin, ymin, zmin = bbox.xmin, bbox.ymin, bbox.zmin
        if not self.binary and (xmin < 0 or ymin < 0 or zmin < 0):
            T = Translation.from_vector([-xmin, -ymin, -zmin])
            mesh = self.mesh.transformed(T)
        else:
            mesh = self.mesh
        return {vertex: mesh.vertex_attributes(vertex, "xyz") for vertex in mesh.vertices()}

    def write(self):
        """Write the data to a file.

        Returns
        -------
        None

        """
        if not self.mesh.is_trimesh():
            raise ValueError("Mesh must be triangular to be encoded in STL.")
        if not self.binary:
            with _iotools.open_file(self.filepath, "w") as self.file:
                self._write_header()
                self._write_faces()
                self._write_footer()
        else:
            with _iotools.open_file(self.filepath, "wb") as self.file:
                self.file.seek(0)
                self._write_binary_header()
                self._write_binary_num_faces()
                self._write_binary_faces()

    def _write_header(self):
        if not self.file:
            return
        self.file.write("solid {}\n".format(self.solid_name))

    def _write_footer(self):
        if not self.file:
            return
        self.file.write("endsolid {}\n".format(self.solid_name))

    def _write_faces(self):
        if not self.file:
            return
        vertex_xyz = self._vertex_xyz
        for face in self.mesh.faces():
            normal = list(self.mesh.face_normal(face))
            self.file.write("facet normal {0} {1} {2}\n".format(*normal))
            self.file.write("    outer loop\n")
            for vertex in self.mesh.face_vertices(face):
                self.file.write("        vertex {0} {1} {2}\n".format(*vertex_xyz[vertex]))
            self.file.write("    endloop\n")
            self.file.write("endfacet\n")

    def _write_binary_header(self):
        if not self.file:
            return
        self.file.write(b"\0" * 80)

    def _write_binary_num_faces(self):
        if not self.file:
            return
        try:
            self.file.write(struct.pack("<L", self.mesh.number_of_faces()))
        except struct.error:
            raise ValueError("Mesh must have fewer than 4294967295 faces to be written to binary STL.")

    def _write_binary_faces(self):
        if not self.file:
            return
        vertex_xyz = self._vertex_xyz
        for face in self.mesh.faces():
            normal = list(self.mesh.face_normal(face))
            self.file.write(struct.pack("<3f", *normal))
            for vertex in self.mesh.face_vertices(face):
                self.file.write(struct.pack("<3f", *vertex_xyz[vertex]))
            self.file.write(b"\0\0")
