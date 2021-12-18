from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import OrderedDict
from collections import defaultdict

import compas
from compas import _iotools
from compas.utilities import geometric_key


class OBJ(object):
    """Class for working with OBJ files.

    Currently, reading is only supported for polygonal geometry.
    Writing is only supported for meshes.

    Parameters
    ----------
    filepath : path string, file-like object or URL string
        A path, a file-like object or a URL pointing to a file.
    precision : :obj:`str`, optional
        A COMPAS precision specification.

    Examples
    --------
    Reading and writing of a single mesh.

    .. code-block:: python

        from compas.datastructures import Mesh
        from compas.files import OBJ

        mesh = Mesh.from_polyhedron(12)

        # write to file
        obj = OBJ('mesh.obj')
        obj.write(mesh)

        # read from file
        obj = OBJ('mesh.obj')
        obj.read()

        mesh = Mesh.from_vertices_and_faces(obj.vertices, obj.faces)

    Reading and writing of multiple meshes as separate objects in a single OBJ file.

    .. code-block:: python

        from compas.geometry import Pointcloud, Translation
        from compas.datastructures import Mesh
        from compas.files import OBJ

        meshes = []
        for point in Pointcloud.from_bounds(10, 10, 10, 100):
            mesh = Mesh.from_polyhedron(12)
            mesh.transform(Translation.from_vector(point))
            meshes.append(mesh)

        # write to file
        obj = OBJ('meshes.obj')
        obj.write(meshes)

        # read from file
        obj = OBJ('meshes.obj')
        obj.read()

        meshes = []
        for name in obj.objects:
            mesh = Mesh.from_vertices_and_faces(* obj.objects[name])
            mesh.name = name
            meshes.append(mesh)

    References
    ----------
    * http://paulbourke.net/dataformats/obj/

    See Also
    --------
    * :class:`OBJReader`
    * :class:`OBJParser`
    * :class:`OBJWriter`

    """

    def __init__(self, filepath, precision=None):
        self.filepath = filepath
        self.precision = precision
        self._is_parsed = False
        self._reader = None
        self._parser = None
        self._writer = None

    def read(self):
        """Read and parse the contents of the file."""
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
        unweld : :obj:`bool`, optional
            Flag indicating that the vertices of the faces should be unwelded.
        author : :obj:`str`, optional
            The author name to include in the header.
        email : :obj:`str`, optional
            The email of the author to include in the header.
        date : :obj:`str`, optional
            The date to include in the header.
        """
        self._writer = OBJWriter(self.filepath, mesh, precision=self.precision, unweld=unweld, **kwargs)
        self._writer.write()

    @property
    def reader(self):
        """:class:`OBJReader` - A OBJ file reader."""
        if not self._is_parsed:
            self.read()
        return self._reader

    @property
    def parser(self):
        """:class:`OBJParser` - A OBJ data parser."""
        if not self._is_parsed:
            self.read()
        return self._parser

    @property
    def vertices(self):
        """List[List[:obj:`float`]] - The vertices found in the parsed data."""
        return self.parser.vertices

    @property
    def lines(self):
        """List[Tuple[:obj:`int`, :obj:`int`]] - The lines found in the parsed data, as vertex pairs."""
        return self.parser.lines

    @property
    def faces(self):
        """List[List[:obj:`int`]] - The faces found in the parsed data, as lists of vertices."""
        return self.parser.faces

    @property
    def objects(self):
        """Dict[:obj:`str`, Tuple[List[List[:obj:`float`, :obj:`float`, :obj:`float`]], List[List[:obj:`int`]]]] -
        The objects found in the parsed data, as a mapping between object names and tuples of lists of vertices and faces.
        """
        return self.parser.objects

    @property
    def groups(self):
        return self.parser.groups


class OBJReader(object):
    """Class for reading raw geometric data from OBJ files.

    Parameters
    ----------
    filepath : path string, file-like object or URL string
        A path, a file-like object or a URL pointing to a file.

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
        # vertex data
        self.vertices = []
        """List[List[:obj:`float`, :obj:`float`, :obj:`float`]] -
        List of lists of vertex coordinates.
        """
        self.weights = []
        """List[:obj:`float`] - List of vertex weights."""
        self.textures = []
        """"""
        self.normals = []
        """List[List[:obj:`float`, :obj:`float`, :obj:`float`]] -
        List of lists of normal components.
        """
        # polygonal geometry
        self.points = []
        """List[:obj:`int`] -
        List of references to vertex coordinates.
        """
        self.lines = []
        """List[Tuple[:obj:`int`, :obj:`int`]] -
        List of pairs of references to vertex coordinates.
        """
        self.faces = []
        """List[List[:obj:`int`] -
        List of lists of references to vertex coordinates.
        """
        # free-form geometry
        # self.curves = []
        # """"""
        # self.curves2 = []
        # """"""
        # self.surfaces = []
        # """"""
        # free-form attributes
        # self.deg = None
        # """"""
        # self.bmat = None
        # """"""
        # self.step = None
        # """"""
        # self.cstype = None
        # """"""
        # free-form statements
        # parm, trim, hole, scrv, sp, end
        # grouping
        self.groups = defaultdict(list)
        """Dict[:obj:`str`, Tuple[List[:obj:`int`], List[List[:obj:`int`]]]] -
        Groups of mesh objects defined by their vertices and faces.
        """
        self.objects = defaultdict(list)
        """Dict[:obj:`str`, Tuple[List[:obj:`int`], List[List[:obj:`int`]]]] -
        Named mesh objects defined by their vertices and faces.
        """
        self.group = None
        self.object = None

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

        """
        if not self.content:
            return
        for line in self.content:
            parts = line.split()
            if not parts:
                continue
            head = parts[0]
            tail = parts[1:]
            if head == '#':
                self._read_comment(tail)
                continue
            if head == 'v':
                self._read_vertex_coordinates(tail)
                continue
            if head == 'vt':
                self._read_vertex_texture(tail)
                continue
            if head == 'vn':
                self._read_vertex_normal(tail)
                continue
            if head == 'vp':
                self._read_parameter_vertex(tail)
                continue
            if head in ('p', 'l', 'f'):
                self._read_polygonal_geometry(head, tail)
                continue
            if head in ('deg', 'bmat', 'step', 'cstype'):
                self._read_freeform_attribute(head, tail)
                continue
            if head in ('curv', 'curv2', 'surf'):
                self._read_freeform_geometry(head, tail)
                continue
            if head in ('parm', 'trim', 'hole', 'scrv', 'sp', 'end'):
                self._read_freeform_statement(head, tail)
                continue
            if head in ('g', 's', 'mg', 'o'):
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
        if name == 'p':
            self.points.append(int(data[0]) - 1)
            ref = 'p', len(self.points) - 1
            self.groups[self.group].append(ref)
            self.objects[self.object].append(ref)
        # line
        elif name == 'l':
            if len(data) < 2:
                return
            self.lines.append([int(i) - 1 for i in data])
            ref = 'l', len(self.lines) - 1
            self.groups[self.group].append(ref)
            self.objects[self.object].append(ref)
        # face
        elif name == 'f':
            if len(data) < 3:
                return
            face = []
            for d in data:
                parts = d.split('/')
                i = int(parts[0]) - 1
                face.append(i)
            self.faces.append(face)
            ref = 'f', len(self.faces) - 1
            self.groups[self.group].append(ref)
            self.objects[self.object].append(ref)

    def _read_freeform_attribute(self, name, data):
        if name == 'deg':
            self.deg = [int(i) for i in data]
            return
        if name == 'bmat':
            return
        if name == 'step':
            return
        if name == 'cstype':
            self.cstype = data
            return

    def _read_freeform_geometry(self, name, data):
        # curv u0 u1 v1 v2 ...
        # u0: starting parameter value for the curve
        # u1: ending parameter value for the curve
        # v1: vertex reference number for control point
        # v2: vertex reference number for control point
        # ...
        if name == 'curv':
            if self.deg[0] == 1:
                if len(data) == 4:
                    self.lines.append((int(data[2]) - 1, int(data[3]) - 1))
                    ref = 'l', len(self.lines) - 1
                    self.groups[self.group].append(ref)
                    self.objects[self.object].append(ref)
                    return
                if len(data) > 4:
                    self.lines.append([int(d) - 1 for d in data[2:]])
                    ref = 'l', len(self.lines) - 1
                    self.groups[self.group].append(ref)
                    self.objects[self.object].append(ref)
                    return

    def _read_freeform_statement(self, name, data):
        pass

    def _read_grouping(self, name, data):
        if name == 'o':
            self.object = ' '.join(data)
            self.objects[self.object] = []
            return
        if name == 'g':
            self.group = ' '.join(data)
            self.groups[self.group] = []
            self.objects[self.object].append(('g', self.group))
            return


class OBJParser(object):
    """Class for parsing data from a OBJ file.
    The parser converts the raw geometric data of the file
    into corresponding COMPAS geometry objects and data structures.

    Parameters
    ----------
    reader : :class:`OBJReader`
        A OBJ file reader.
    precision : :obj:`str`
        COMPAS precision specification for parsing geometric data.
    """

    def __init__(self, reader, precision=None):
        self.precision = precision
        self.reader = reader
        """:class:`OBJReader` - An OBJ file reader."""
        self.vertices = None
        """List[List[:obj:`float`, :obj:`float`, :obj:`float`]] -
        List of lists of parsed vertex coordinates.
        Parsed vertices are unique up to the specified precision.
        """
        # self.weights = None
        # """List[:obj:`float`] - List of vertex weights."""
        # self.textures = None
        # """List[:obj:`float`] - List of vertex textures."""
        # self.normals = None
        self.points = None
        """List[:obj:`int`] -
        List of references to parsed vertex coordinates.
        """
        self.lines = None
        """List[Tuple[:obj:`int`, :obj:`int`]] -
        List of pairs of references to parsed vertex coordinates.
        """
        self.polylines = None
        """List[List[:obj:`int`] -
        List of lists of references to parsed vertex coordinates.
        """
        self.faces = None
        """List[List[:obj:`int`] -
        List of lists of references to parsed vertex coordinates.
        """
        # self.curves = None
        # self.curves2 = None
        # self.surfaces = None
        self.groups = None
        """Dict[:obj:`str`, Tuple[List[:obj:`int`], List[List[:obj:`int`]]]] -
        Groups of mesh objects defined by their parsed vertices and faces.
        """
        self.objects = None
        """Dict[:obj:`str`, Tuple[List[:obj:`int`], List[List[:obj:`int`]]]] -
        Named mesh objects defined by their parsed vertices and faces.
        """

    def parse(self):
        """Parse the contents of the file."""
        index_key = OrderedDict()
        vertex = OrderedDict()

        for i, xyz in enumerate(iter(self.reader.vertices)):
            key = geometric_key(xyz, self.precision)
            index_key[i] = key
            vertex[key] = xyz

        key_index = {key: index for index, key in enumerate(vertex)}
        index_index = {index: key_index[key] for index, key in iter(index_key.items())}

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
                if item[0] == 'f':
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
    filepath : path string, file-like object or URL string
        A path, a file-like object or a URL pointing to a file.
    meshes : List[:class:`compas.datastructures.Mesh`]
        List of meshes to write to the file.
    precision : :obj:`str`, optional
        COMPAS precision specification for parsing geometric data.
    unweld : :obj:`bool`, optional
        Flag indicating that the face vertices should be unwelded.
    author : :obj:`str`, optional
        The author name to include in the header.
    email : :obj:`str`, optional
        The email of the author to include in the header.
    date : :obj:`str`, optional
        The date to include in the header.
    """

    def __init__(self, filepath, meshes, precision=None, unweld=False, author=None, email=None, date=None):
        self.filepath = filepath
        self.meshes = meshes if isinstance(meshes, (list, tuple)) else [meshes]
        self.author = author
        self.email = email
        self.date = date
        self.precision = precision or compas.PRECISION
        self.unweld = unweld
        self.vertex_tpl = "v {0:." + self.precision + "}" + " {1:." + self.precision + "}" + " {2:." + self.precision + "}\n"
        self.v = sum(mesh.number_of_vertices() for mesh in self.meshes)
        self.f = sum(mesh.number_of_faces() for mesh in self.meshes)
        self.e = sum(mesh.number_of_edges() for mesh in self.meshes)
        self._v = 1
        self.file = None

    def write(self):
        """Write the meshes to the file."""
        with _iotools.open_file(self.filepath, 'w') as self.file:
            self.write_header()
            self.write_meshes()

    def write_header(self):
        """Write the header info."""
        self.file.write('# OBJ\n')
        self.file.write('# COMPAS\n')
        self.file.write('# version: {}\n'.format(compas.__version__))
        self.file.write('# precision: {}\n'.format(self.precision))
        self.file.write('# V F E: {} {} {}\n'.format(self.v, self.f, self.e))
        if self.author:
            self.file.write('# author: {}\n'.format(self.author))
        if self.email:
            self.file.write('# email: {}\n'.format(self.email))
        if self.date:
            self.file.write('# date: {}\n'.format(self.date))
        self.file.write('\n')

    def write_meshes(self):
        """Write the mesh data."""
        for index, mesh in enumerate(self.meshes):
            name = mesh.name
            if name == 'Mesh':
                name = 'Mesh {}'.format(index)
            self.file.write('o {}\n'.format(name))
            if self.unweld:
                self._write_vertices_and_faces(mesh)
            else:
                self._write_vertices(mesh)
                self._write_faces(mesh)
                self._v += mesh.number_of_vertices()

    def _write_vertices(self, mesh):
        for key in mesh.vertices():
            x, y, z = mesh.vertex_coordinates(key)
            self.file.write(self.vertex_tpl.format(x, y, z))

    def _write_faces(self, mesh):
        key_index = mesh.key_index()
        for fkey in mesh.faces():
            vertices = mesh.face_vertices(fkey)
            vertices = [key_index[key] + self._v for key in vertices]
            vertices_str = ' '.join([str(index) for index in vertices])
            self.file.write('f {0}\n'.format(vertices_str))

    def _write_vertices_and_faces(self, mesh):
        for face in mesh.faces():
            vertices = mesh.face_vertices(face)
            indices = []
            for vertex in vertices:
                x, y, z = mesh.vertex_coordinates(vertex)
                self.file.write(self.vertex_tpl.format(x, y, z))
                indices.append(self._v)
                self._v += 1
            indices_str = ' '.join([str(i) for i in indices])
            self.file.write('f {0}\n'.format(indices_str))
