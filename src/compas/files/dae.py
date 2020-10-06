from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import compas
from compas.utilities import geometric_key

# from collada import Collada


__all__ = [
    'DAE',
    'DAEReader',
    'DAEParser',
    # 'DAEWriter',
]


class DAE(object):

    def __init__(self, filepath, precision=None):
        self.filepath = filepath
        self.precision = precision
        self._is_parsed = False
        self._reader = None
        self._parser = None
        self._writer = None

    def read(self):
        self._reader = DAEReader(self.filepath)
        self._parser = DAEParser(self._reader, precision=self.precision)
        self._is_parsed = True

    # def write(self, mesh, **kwargs):
    #     self._writer = DAEWriter(self.filepath, mesh, **kwargs)
    #     self._writer.write()

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


class DAEReader(object):
    """Standard triangle library format.

    References
    ----------
    .. [1] http://paulbourke.net/dataformats/stl/

    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None
        self.header = None
        self.facets = []
        self.read()

    def read(self):
        with open(self.filepath, 'r') as f:
            self.file = f
            self.file.seek(0)
            self.facets = self.read_primitives()

    def read_primitives(self):
        solids = {}
        facets = []

        while True:
            line = self.file.readline().strip()

            if not line:
                break

            parts = line.split()

            if parts[0] == 'solid':
                if len(parts) == 2:
                    name = parts[1]
                else:
                    name = 'solid'
                solids[name] = []

            elif parts[0] == 'endsolid':
                name = None

            elif parts[0] == 'facet':
                facet = {'normal': None, 'vertices': None}
                if parts[1] == 'normal':
                    facet['normal'] = [float(parts[i]) for i in range(2, 5)]

            elif parts[0] == 'outer' and parts[1] == 'loop':
                vertices = []

            elif parts[0] == 'vertex':
                xyz = [float(parts[i]) for i in range(1, 4)]
                vertices.append(xyz)

            elif parts[0] == 'endloop':
                facet['vertices'] = vertices

            elif parts[0] == 'endfacet':
                solids[name].append(facet)
                facets.append(facet)

            # no known line start matches, maybe not ascii
            elif not parts[0].isalnum():
                raise RuntimeError('File is not ASCII')

        return facets


class DAEParser(object):
    """"""

    def __init__(self, reader, precision=None):
        self.precision = precision
        self.reader = reader
        self.vertices = None
        self.faces = None
        self.parse()

    def parse(self):
        gkey_index = {}
        vertices = []
        faces = []
        for facet in self.reader.facets:
            face = []
            facet_vertices = facet['vertices']
            for i in range(3):
                xyz = facet_vertices[i]
                if 'keys' in facet:
                    gkey = facet['keys'][i]
                else:
                    gkey = geometric_key(xyz, self.precision)
                if gkey not in gkey_index:
                    gkey_index[gkey] = len(vertices)
                    vertices.append(xyz)
                face.append(gkey_index[gkey])
            faces.append(face)
        self.vertices = vertices
        self.faces = faces


# class DAEWriter(object):
#     """"""

#     def __init__(self, filepath, mesh, binary=False, solid_name=None, precision=None):
#         self.filepath = filepath
#         self.mesh = mesh
#         self.solid_name = solid_name or mesh.name
#         self.precision = precision or compas.PRECISION
#         self.file = None
#         self.binary = binary

#     @property
#     def vertex_xyz(self):
#         bbox = self.mesh.bounding_box()
#         xmin, ymin, zmin = bbox[0]
#         if xmin < 0 or ymin < 0 or zmin < 0:
#             T = Translation.from_vector([-xmin, -ymin, -zmin])
#             mesh = self.mesh.transformed(T)
#         else:
#             mesh = self.mesh
#         return {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}

#     def write(self):
#         if not self.binary:
#             with open(self.filepath, 'w') as self.file:
#                 self.write_header()
#                 self.write_faces()
#                 self.write_footer()
#         else:
#             raise NotImplementedError

#     def write_header(self):
#         self.file.write("solid {}\n".format(self.solid_name))

#     def write_footer(self):
#         self.file.write("endsolid {}\n".format(self.solid_name))

#     def write_faces(self):
#         vertex_xyz = self.vertex_xyz
#         for face in self.mesh.faces():
#             self.file.write("facet normal {0} {1} {2}\n".format(* self.mesh.face_normal(face)))
#             self.file.write("    outer loop\n")
#             for vertex in self.mesh.face_vertices(face):
#                 self.file.write("        vertex {0} {1} {2}\n".format(* vertex_xyz[vertex]))
#             self.file.write("    endloop\n")
#             self.file.write("endfacet\n")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
