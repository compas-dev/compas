from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from compas.utilities import geometric_key


__all__ = [
    'OBJ',
    'OBJReader',
    'OBJParser',
]


class OBJ(object):
    """Read and write files in OBJ format.

    See Also
    --------
    * http://paulbourke.net/dataformats/obj/

    """
    def __init__(self, filepath, precision=None):
        self.reader = OBJReader(filepath)
        self.parser = OBJParser(self.reader, precision=precision)


class OBJReader(object):
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
        self.curves = []
        self.curves2 = []
        self.surfaces = []
        # free-form attributes
        self.deg = None
        self.bmat = None
        self.step = None
        self.cstype = None
        # free-form statements
        # parm, trim, hole, scrv, sp, end
        # grouping
        self.groups = {}
        self.objects = {}
        self.group = None
        # open file path and read
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
            if self.group:
                self.groups[self.group].append(('p', len(self.points) - 1))
        # line
        elif name == 'l':
            if len(data) < 2:
                return
            self.lines.append([int(i) - 1 for i in data])
            if self.group:
                self.groups[self.group].append(('l', len(self.lines) - 1))
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
            if self.group:
                self.groups[self.group].append(('f', len(self.faces) - 1))

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
                    if self.group:
                        self.groups[self.group].append(('l', len(self.lines) - 1))
                    return
                if len(data) > 4:
                    self.lines.append([int(d) - 1 for d in data[2:]])
                    # if self.group:
                    #     self.groups[self.group].append(('l', len(self.lines) - 1))
                    return

    def _read_freeform_statement(self, name, data):
        pass

    def _read_grouping(self, name, data):
        if name == 'g':
            self.group = data[0]
            self.groups[self.group] = []
            return


class OBJParser(object):
    """"""
    def __init__(self, reader, precision=None):
        self.precision = precision
        self.reader    = reader
        self.vertices  = None
        self.weights   = None
        self.textures  = None
        self.normals   = None
        self.points    = None
        self.lines     = None
        self.polylines = None
        self.faces     = None
        self.curves    = None
        self.curves2   = None
        self.surfaces  = None
        self.groups    = None
        self.objects   = None
        self.parse()

    def parse(self):
        index_key = {}
        vertex = {}

        for i, xyz in enumerate(iter(self.reader.vertices)):
            key = geometric_key(xyz, self.precision)
            index_key[i] = key
            vertex[key] = xyz

        key_index = {key: index for index, key in enumerate(vertex)}
        index_index = {index: key_index[key] for index, key in iter(index_key.items())}

        self.vertices  = [xyz for xyz in iter(vertex.values())]
        self.points    = [index_index[index] for index in self.reader.points]
        self.lines     = [[index_index[index] for index in line] for line in self.reader.lines if len(line) == 2]
        self.polylines = [[index_index[index] for index in line] for line in self.reader.lines if len(line) > 2]
        self.faces     = [[index_index[index] for index in face] for face in self.reader.faces]
        self.groups    = self.reader.groups


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas

    obj = OBJ(compas.get('faces.obj'))

    print(obj.parser.vertices)
    print(obj.parser.lines)
    print(obj.parser.points)
    print(obj.parser.faces)
