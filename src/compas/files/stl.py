from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import struct
from compas.utilities import geometric_key


__all__ = [
    'STL',
    'STLReader',
    'STLParser',
]


class STL(object):

    def __init__(self, filepath, precision=None):
        self.reader = STLReader(filepath)
        self.parser = STLParser(self.reader, precision=precision)


class STLReader(object):
    """Standard triangle library format.

    See Also
    --------
    * http://paulbourke.net/dataformats/stl/

    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None
        self.header = None
        self.facets = []
        self.read()

    def read(self):
        is_binary = False
        with open(self.filepath, 'rb') as file:
            line = file.readline().strip()
            if b'solid' in line:
                is_binary = False
            else:
                is_binary = True

        try:
            if not is_binary:
                self.read_ascii()
            else:
                self.read_binary()
        except Exception:
            # raise if it was already detected as binary, but failed anyway
            if is_binary: raise

            # else, ascii parsing failed, try binary
            is_binary = True
            self.read_binary()

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

    def read_ascii(self):
        with open(self.filepath, 'r') as file:
            self.file = file
            self.file.seek(0)
            self.facets = self.read_solids_ascii()

    def read_solids_ascii(self):
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
        return struct.unpack('<H', bytes_)[0]

    def _read_uint32(self):
        bytes_ = self.file.read(4)
        return struct.unpack('<I', bytes_)[0]

    def read_binary(self):
        with open(self.filepath, 'rb') as file:
            self.file = file
            self.file.seek(0)
            self.header = self.read_header_binary()
            self.facets = self.read_facets_binary()

    def read_header_binary(self):
        bytes_ = self.file.read(80)
        return struct.unpack('80s', bytes_)[0]

    def read_number_of_facets_binary(self):
        return self._read_uint32()

    def read_facet_binary(self):
        # Read full facet at once
        # 4 bytes per float * 3 floats per vector/vertex * 4 items (1 vector + 3 vertices)
        bytes_ = self.file.read(48)
        floats_ = struct.unpack('<12f', bytes_)

        normal = floats_[0:3]
        vertices = (floats_[3:6], floats_[6:9], floats_[9:12])
        keys = (bytes_[12:24], bytes_[24:36], bytes_[36:48])

        # Skip two-byte attributes, it's not used anywhere (by anyone - on this planet)
        self.file.seek(2, 1)

        return {'normal': normal, 'vertices': vertices, 'keys': keys}

    def read_facets_binary(self):
        facets = []
        n = self.read_number_of_facets_binary()
        for i in range(n):
            facets.append(self.read_facet_binary())
        return facets


class STLParser(object):
    """"""

    def __init__(self, reader, precision=None):
        self.precision = precision
        self.reader    = reader
        self.vertices  = None
        self.faces     = None
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import os
    import compas

    from compas.datastructures import Mesh
    from compas.viewers import MeshViewer
    from compas.utilities import download_file_from_remote
    from compas.topology import connected_components


    source = 'https://raw.githubusercontent.com/ros-industrial/abb/kinetic-devel/abb_irb6600_support/meshes/irb6640/visual/link_1.stl'
    filepath = os.path.join(compas.APPDATA, 'data', 'meshes', 'ros', 'link_1.stl')

    download_file_from_remote(source, filepath, overwrite=False)

    stl = STL(filepath, precision='6f')

    mesh = Mesh.from_vertices_and_faces(stl.parser.vertices, stl.parser.faces)

    vertexgroups = connected_components(mesh.halfedge)
    facegroups = [[] for _ in range(len(vertexgroups))]

    vertexsets = list(map(set, vertexgroups))

    for fkey in mesh.faces():
        vertices = set(mesh.face_vertices(fkey))

        for i, vertexset in enumerate(vertexsets):
            if vertices.issubset(vertexset):
                facegroups[i].append(fkey)
                break

    meshes = []

    for vertexgroup, facegroup in zip(vertexgroups, facegroups):
        key_index = {key: index for index, key in enumerate(vertexgroup)}
        vertices = mesh.get_vertices_attributes('xyz', keys=vertexgroup)
        faces = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in facegroup]

        meshes.append(Mesh.from_vertices_and_faces(vertices, faces))

    viewer = MeshViewer()
    viewer.mesh = meshes[0]
    viewer.show()
