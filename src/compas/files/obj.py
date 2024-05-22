from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import OrderedDict
from collections import defaultdict

import compas
from compas import _iotools
from compas.tolerance import TOL


class OBJ(object):
    """Class for working with OBJ files.

    Currently, reading is only supported for polygonal geometry.
    Writing is only supported for meshes.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.
    precision : str, optional
        A COMPAS precision specification.

    Attributes
    ----------
    reader : :class:`OBJReader`, read-only
        A OBJ file reader.
    parser : :class:`OBJParser`, read-only
        A OBJ data parser.
    vertices : list[list[float]], read-only
        The vertices found in the parsed data.
    lines : list[tuple[int, int]], read-only
        The lines found in the parsed data, as vertex pairs.
    faces : list[list[int]], read-only
        The faces found in the parsed data, as lists of vertices.
    objects : dict[str, tuple[list[list[float, float, float]], list[list[int]]]], read-only
        The objects found in the parsed data, as a mapping between object names and tuples of lists of vertices and faces.

    References
    ----------
    * http://paulbourke.net/dataformats/obj/

    Examples
    --------
    Reading and writing of a single mesh.

    >>> from compas.datastructures import Mesh
    >>> from compas.files import OBJ

    Write mesh data to a file.

    >>> mesh = Mesh.from_polyhedron(12)
    >>> obj = OBJ("mesh.obj")
    >>> obj.write(mesh)

    Read mesh data from a file.

    >>> obj = OBJ("mesh.obj")
    >>> obj.read()
    >>> mesh = Mesh.from_vertices_and_faces(obj.vertices, obj.faces)

    Reading and writing of multiple meshes as separate objects in a single OBJ file.

    >>> from compas.geometry import Pointcloud, Translation
    >>> from compas.datastructures import Mesh
    >>> from compas.files import OBJ

    Write mesh data to a file.

    >>> meshes = []
    >>> for point in Pointcloud.from_bounds(10, 10, 10, 100):
    ...     mesh = Mesh.from_polyhedron(12)
    ...     mesh.transform(Translation.from_vector(point))
    ...     meshes.append(mesh)
    >>> obj = OBJ("meshes.obj")
    >>> obj.write(meshes)

    Read mesh data from a file.

    >>> obj = OBJ("meshes.obj")
    >>> obj.read()
    >>> meshes = []
    >>> for name in obj.objects:
    ...     mesh = Mesh.from_vertices_and_faces(*obj.objects[name])
    ...     mesh.name = name
    ...     meshes.append(mesh)

    """

    def __init__(self, filepath, precision=None):
        self.filepath = filepath
        self.precision = precision
        self._is_parsed = False
        self._reader = None
        self._parser = None
        self._writer = None

    def read(self):
        """Read and parse the contents of the file.

        Returns
        -------
        None
        """
        self._reader = OBJReader(self.filepath)
        self._parser = OBJParser(self._reader, precision=self.precision)
        self._reader.open()
        self._reader.pre()
        self._reader.read()
        self._reader.post()
        self._parser.parse()
        self._is_parsed = True

    def write(self, mesh, unweld=False, **kwargs):
        """Write a mesh to the file.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            The mesh.
        unweld : bool, optional
            Flag indicating that the vertices of the faces should be unwelded.
        author : str, optional
            The author name to include in the header.
        email : str, optional
            The email of the author to include in the header.
        date : str, optional
            The date to include in the header.

        Returns
        -------
        None

        """
        self._writer = OBJWriter(self.filepath, mesh, precision=self.precision, unweld=unweld, **kwargs)
        self._writer.write()

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

    @property
    def vertices(self):
        return self.parser.vertices

    @property
    def lines(self):
        return self.parser.lines

    @property
    def faces(self):
        return self.parser.faces

    @property
    def objects(self):
        return self.parser.objects

    @property
    def groups(self):
        return self.parser.groups


class OBJReader(object):
    """Class for reading raw geometric data from OBJ files.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.

    Attributes
    ----------
    vertices : list[list[float, float, float]]
        List of lists of vertex coordinates.
    weights : list[float]
        List of vertex weights.
    normals : list[list[float, float, float]]
        List of lists of normal components.
    points : list[int]
        List of references to vertex coordinates.
    lines : list[tuple[int, int]]
        List of pairs of references to vertex coordinates.
    faces : list[list[int]
        List of lists of references to vertex coordinates.
    groups : dict[str, tuple[list[int], list[list[int]]]]
        Groups of mesh objects defined by their vertices and faces.
    objects : dict[str, tuple[list[int], list[list[int]]]]
        Named mesh objects defined by their vertices and faces.

    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.content = None
        # vertex data
        self.vertices = []
        self.weights = []
        self.textures = []
        self.normals = []
        # polygonal geometry
        self.points = []
        self.lines = []
        self.faces = []
        # free-form geometry
        # self.curves = []
        # self.curves2 = []
        # self.surfaces = []
        # free-form attributes
        # self.deg = None
        # self.bmat = None
        # self.step = None
        # self.cstype = None
        # free-form statements
        # parm, trim, hole, scrv, sp, end
        # grouping
        self.groups = defaultdict(list)
        self.objects = defaultdict(list)
        self.group = None
        self.object = None

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

        Every line is split into a *head* and a *tail*.
        The *head* determines the meaning of the data found in *tail*.

        * ``#``: comment
        * ``v``: vertex coordinates
        * ``vt``: vertex texture
        * ``vn``: vertex normal
        * ``vp``: parameter vertex
        * ``p``: point
        * ``l``: line
        * ``f``: face
        * ``deg``: freeform attribute *degree*
        * ``bmat``: freeform attribute *basis matrix*
        * ``step``: freeform attribute *step size*
        * ``cstype``: freeform attribute *curve or surface type*
        * ``o``: start of named object
        * ``g``: start of a named group

        Returns
        -------
        None

        """
        if not self.content:
            return
        for line in self.content:
            parts = line.split()
            if not parts:
                continue
            head = parts[0]
            tail = parts[1:]
            if head == "#":
                self._read_comment(tail)
                continue
            if head == "v":
                self._read_vertex_coordinates(tail)
                continue
            if head == "vt":
                self._read_vertex_texture(tail)
                continue
            if head == "vn":
                self._read_vertex_normal(tail)
                continue
            if head == "vp":
                self._read_parameter_vertex(tail)
                continue
            if head in ("p", "l", "f"):
                self._read_polygonal_geometry(head, tail)
                continue
            if head in ("deg", "bmat", "step", "cstype"):
                self._read_freeform_attribute(head, tail)
                continue
            if head in ("curv", "curv2", "surf"):
                self._read_freeform_geometry(head, tail)
                continue
            if head in ("parm", "trim", "hole", "scrv", "sp", "end"):
                self._read_freeform_statement(head, tail)
                continue
            if head in ("g", "s", "mg", "o"):
                self._read_grouping(head, tail)
                continue

    def _read_comment(self, data):
        """Read a comment.

        Comments start with ``#``.

        """
        pass

    def _read_vertex_coordinates(self, data):
        """Read the coordinates of a vertex.

        Two types of formats are possible:

        * x y z
        * x y z w

        """
        if len(data) == 3:
            self.vertices.append([float(x) for x in data])
            self.weights.append(1.0)
            return
        if len(data) == 4:
            self.vertices.append([float(x) for x in data[:3]])
            self.weights.append(float(data[3]))

    def _read_vertex_texture(self, data):
        pass

    def _read_vertex_normal(self, data):
        pass

    def _read_parameter_vertex(self, data):
        pass

    def _read_polygonal_geometry(self, name, data):
        # point
        if name == "p":
            self.points.append(int(data[0]) - 1)
            ref = "p", len(self.points) - 1
            self.groups[self.group].append(ref)
            self.objects[self.object].append(ref)
        # line
        elif name == "l":
            if len(data) < 2:
                return
            self.lines.append([int(i) - 1 for i in data])
            ref = "l", len(self.lines) - 1
            self.groups[self.group].append(ref)
            self.objects[self.object].append(ref)
        # face
        elif name == "f":
            if len(data) < 3:
                return
            face = []
            for d in data:
                parts = d.split("/")
                i = int(parts[0]) - 1
                face.append(i)
            self.faces.append(face)
            ref = "f", len(self.faces) - 1
            self.groups[self.group].append(ref)
            self.objects[self.object].append(ref)

    def _read_freeform_attribute(self, name, data):
        if name == "deg":
            self.deg = [int(i) for i in data]
            return
        if name == "bmat":
            return
        if name == "step":
            return
        if name == "cstype":
            self.cstype = data
            return

    def _read_freeform_geometry(self, name, data):
        # curv u0 u1 v1 v2 ...
        # u0: starting parameter value for the curve
        # u1: ending parameter value for the curve
        # v1: vertex reference number for control point
        # v2: vertex reference number for control point
        # ...
        if name == "curv":
            if self.deg[0] == 1:
                if len(data) == 4:
                    self.lines.append((int(data[2]) - 1, int(data[3]) - 1))
                    ref = "l", len(self.lines) - 1
                    self.groups[self.group].append(ref)
                    self.objects[self.object].append(ref)
                    return
                if len(data) > 4:
                    self.lines.append([int(d) - 1 for d in data[2:]])
                    ref = "l", len(self.lines) - 1
                    self.groups[self.group].append(ref)
                    self.objects[self.object].append(ref)
                    return

    def _read_freeform_statement(self, name, data):
        pass

    def _read_grouping(self, name, data):
        if name == "o":
            self.object = " ".join(data)
            self.objects[self.object] = []
            return
        if name == "g":
            self.group = " ".join(data)
            self.groups[self.group] = []
            self.objects[self.object].append(("g", self.group))
            return


class OBJParser(object):
    """Class for parsing data from a OBJ file.

    The parser converts the raw geometric data of the file
    into corresponding COMPAS geometry objects and data structures.

    Parameters
    ----------
    reader : :class:`OBJReader`
        A OBJ file reader.
    precision : int, optional
        Precision for converting numbers to strings.
        Default is :attr:`TOL.precision`.

    Attributes
    ----------
    reader : :class:`OBJReader`
        An OBJ file reader.
    vertices : list[list[float, float, float]]
        List of lists of parsed vertex coordinates.
        Parsed vertices are unique up to the specified precision.
    points : list[int]
        List of references to parsed vertex coordinates.
    lines : list[tuple[int, int]]
        List of pairs of references to parsed vertex coordinates.
    polylines : list[list[int]
        List of lists of references to parsed vertex coordinates.
    faces : list[list[int]
        List of lists of references to parsed vertex coordinates.
    groups : dict[str, tuple[list[int], list[list[int]]]]
        Groups of mesh objects defined by their parsed vertices and faces.
    objects : dict[str, tuple[list[int], list[list[int]]]]
        Named mesh objects defined by their parsed vertices and faces.

    """

    def __init__(self, reader, precision=None):
        self.precision = precision
        self.reader = reader
        self.vertices = None
        # self.weights = None
        # self.textures = None
        # self.normals = None
        self.points = None
        self.lines = None
        self.polylines = None
        self.faces = None
        # self.curves = None
        # self.curves2 = None
        # self.surfaces = None
        self.groups = None
        self.objects = None

    def parse(self):
        """Parse the the data found by the reader.

        Returns
        -------
        None

        """
        index_key = OrderedDict()
        vertex = OrderedDict()

        for i, xyz in enumerate(iter(self.reader.vertices)):
            key = TOL.geometric_key(xyz, self.precision)
            index_key[i] = key
            vertex[key] = xyz

        vertex_index = {key: index for index, key in enumerate(vertex)}
        index_index = {index: vertex_index[key] for index, key in iter(index_key.items())}

        self.vertices = [xyz for xyz in iter(vertex.values())]
        self.points = [index_index[index] for index in self.reader.points]
        self.lines = [[index_index[index] for index in line] for line in self.reader.lines if len(line) == 2]
        self.polylines = [[index_index[index] for index in line] for line in self.reader.lines if len(line) > 2]
        self.faces = [[index_index[index] for index in face] for face in self.reader.faces]
        self.groups = self.reader.groups
        self.objects = {}
        for name in self.reader.objects:
            faces = []
            for item in self.reader.objects[name]:
                if item[0] == "f":
                    faces.append(self.faces[item[1]])
            vertices = {}
            for face in faces:
                for vertex in face:
                    vertices[vertex] = self.vertices[vertex]
            self.objects[name] = vertices, faces


class OBJWriter(object):
    """Class for writing geometric data to a OBJ file.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.
    meshes : list[:class:`compas.datastructures.Mesh`]
        list of meshes to write to the file.
    precision : str, optional
        COMPAS precision specification for parsing geometric data.
    unweld : bool, optional
        Flag indicating that the face vertices should be unwelded.
    author : str, optional
        The author name to include in the header.
    email : str, optional
        The email of the author to include in the header.
    date : str, optional
        The date to include in the header.

    """

    def __init__(
        self,
        filepath,
        meshes,
        precision=None,
        unweld=False,
        author=None,
        email=None,
        date=None,
    ):
        self.filepath = filepath
        self.meshes = meshes if isinstance(meshes, (list, tuple)) else [meshes]
        self.author = author
        self.email = email
        self.date = date
        self.precision = precision or TOL.precision
        self.unweld = unweld
        self.v = sum(mesh.number_of_vertices() for mesh in self.meshes)
        self.f = sum(mesh.number_of_faces() for mesh in self.meshes)
        self.e = sum(mesh.number_of_edges() for mesh in self.meshes)
        self._v = 1
        self.file = None

    def write(self):
        """Write the meshes to the file.

        Returns
        -------
        None

        """
        with _iotools.open_file(self.filepath, "w") as self.file:
            self._write_header()
            self._write_meshes()

    def _write_header(self):
        if not self.file:
            return
        self.file.write("# OBJ\n")
        self.file.write("# COMPAS\n")
        self.file.write("# version: {}\n".format(compas.__version__))
        self.file.write("# precision: {}\n".format(self.precision))
        self.file.write("# V F E: {} {} {}\n".format(self.v, self.f, self.e))
        if self.author:
            self.file.write("# author: {}\n".format(self.author))
        if self.email:
            self.file.write("# email: {}\n".format(self.email))
        if self.date:
            self.file.write("# date: {}\n".format(self.date))
        self.file.write("\n")

    def _write_meshes(self):
        if not self.file:
            return
        for index, mesh in enumerate(self.meshes):
            name = mesh.name
            if name == "Mesh":
                name = "Mesh {}".format(index)
            self.file.write("o {}\n".format(name))
            if self.unweld:
                self._write_vertices_and_faces(mesh)
            else:
                self._write_vertices(mesh)
                self._write_faces(mesh)
                self._v += mesh.number_of_vertices()

    def _write_vertices(self, mesh):
        if not self.file:
            return
        for key in mesh.vertices():
            x, y, z = mesh.vertex_coordinates(key)
            self.file.write(
                "v {0} {1} {2}\n".format(
                    TOL.format_number(x, self.precision),
                    TOL.format_number(y, self.precision),
                    TOL.format_number(z, self.precision),
                )
            )

    def _write_faces(self, mesh):
        if not self.file:
            return
        vertex_index = mesh.vertex_index()
        for face in mesh.faces():
            vertices = mesh.face_vertices(face)
            vertices = [vertex_index[key] + self._v for key in vertices]
            vertices_str = " ".join([str(index) for index in vertices])
            self.file.write("f {0}\n".format(vertices_str))

    def _write_vertices_and_faces(self, mesh):
        if not self.file:
            return
        for face in mesh.faces():
            vertices = mesh.face_vertices(face)
            indices = []
            for vertex in vertices:
                x, y, z = mesh.vertex_coordinates(vertex)
                self.file.write(
                    "v {0} {1} {2}\n".format(
                        TOL.format_number(x, self.precision),
                        TOL.format_number(y, self.precision),
                        TOL.format_number(z, self.precision),
                    )
                )
                indices.append(self._v)
                self._v += 1
            indices_str = " ".join([str(i) for i in indices])
            self.file.write("f {0}\n".format(indices_str))
