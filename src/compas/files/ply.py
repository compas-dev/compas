from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import struct


__all__ = [
    'PLY',
    'PLYReader',
    'PLYParser',
]


class PLY(object):
    """Polygon file format, or Stanford triangle format.

    See Also
    --------
    * http://paulbourke.net/dataformats/ply/

    """
    def __init__(self, filepath, precision=None):
        self.reader = PLYReader(filepath)
        self.parser = PLYParser(self.reader, precision=precision)


class PLYReader(object):
    """"""

    keywords = ['ply', 'format', 'comment', 'element', 'property', 'end_header']

    property_types = {
        'char'   : int,
        'uchar'  : int,
        'short'  : int,
        'ushort' : int,
        'int'    : int,
        'uint'   : int,
        'float'  : float,
        'double' : float,
    }

    binary_property_types = {
        'int8'   : 'i1',
        'char'   : 'i1',
        'uint8'  : 'u1',
        'uchar'  : 'u1',
        'int16'  : 'i2',
        'short'  : 'i2',
        'uint16' : 'u2',
        'ushort' : 'u2',
        'int32'  : 'i4',
        'int'    : 'i4',
        'uint32' : 'u4',
        'uint'   : 'u4',
        'float32': 'f4',
        'float'  : 'f4',
        'float64': 'f8',
        'double' : 'f8'
    }

    number_of_bytes_per_type = {
        'char'  : 1,
        'uchar' : 1,
        'short' : 2,
        'ushort': 2,
        'int'   : 4,
        'uint'  : 4,
        'float' : 4,
        'double': 8
    }

    struct_format_per_type = {
        'char'  : 'c',
        'uchar' : 'B',
        'short' : 'h',
        'ushort': 'H',
        'int'   : 'i',
        'uint'  : 'I',
        'float' : 'f',
        'double': 'd'
    }

    binary_byte_order = {'binary_big_endian': '>', 'binary_little_endian': '<'}

    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None
        self.format = None
        self.comments = []
        self.header = []
        self.start_header = None
        self.end_header = None
        self.number_of_vertices = None
        self.number_of_edges = None
        self.number_of_faces = None
        self.vertex_properties = []
        self.edge_properties = []
        self.face_properties = []
        self.sections = []
        self.vertices = []
        self.edges = []
        self.faces = []
        self.read()

    def is_valid(self):
        self.read_header()
        if self.start_header and self.end_header:
            return True
        return False

    def is_binary(self):
        if self.format == 'binary_big_endian':
            return True
        if self.format == 'binary_little_endian':
            return True
        return False

    def is_ascii(self):
        if self.format == 'ascii':
            return True
        return False

    def read(self):
        self.read_header()
        if self.format == 'ascii':
            self.read_data()
        else:
            self.read_data_binary()

    # ==========================================================================
    # read the header
    # ==========================================================================

    def read_header(self):
        # the header is always in ascii format
        # read it as text
        # otherwise file.tell() can't be used reliably
        # to figure out where the header ends
        with open(self.filepath) as file:
            file.seek(0)

            line = file.readline().rstrip()

            if line != 'ply':
                raise Exception('not a valid ply file')

            self.start_header = file.tell()

            element_type = None

            while True:
                line = file.readline()
                line = line.rstrip()

                self.header.append(line)

                if line.startswith('format'):
                    element_type = None
                    self.format = line[len('format') + 1:].split(' ')[0]
                    continue

                if line.startswith('comment'):
                    element_type = None
                    self.comments.append(line[len('comment') + 1:])
                    continue

                if line.startswith('element'):
                    parts = line.split()
                    element_type = parts[1]
                    if element_type == 'vertex':
                        self.sections.append('vertex')
                        self.number_of_vertices = int(parts[2])
                    elif element_type == 'edge':
                        self.sections.append('edge')
                        self.number_of_edges = int(parts[2])
                    elif element_type == 'face':
                        self.sections.append('face')
                        self.number_of_faces = int(parts[2])
                    else:
                        element_type = None
                        raise Exception
                    continue

                if line.startswith('property'):
                    parts = line.split()
                    if element_type == 'vertex':
                        property_type = parts[1]
                        property_name = parts[2]
                        self.vertex_properties.append((property_name, property_type))
                    elif element_type == 'edge':
                        property_type = parts[1]
                        property_name = parts[2]
                        self.edge_properties.append((property_name, property_type))
                    elif element_type == 'face':
                        property_type = parts[1]
                        if property_type == 'list':
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
                    continue

                if line == 'end_header':
                    element_type = None
                    self.end_header = file.tell()
                    break

    # ==========================================================================
    # read the data
    # ==========================================================================

    def read_data(self):
        if not self.end_header:
            raise Exception('header has not been read, or the file is not valid')
        with open(self.filepath) as self.file:
            self.file.seek(self.end_header)
            for section in self.sections:
                if section == 'vertex':
                    self.read_vertices()
                elif section == 'edge':
                    self.read_edges()
                elif section == 'face':
                    self.read_faces()
                else:
                    print('user-defined elements are not supported: {0}'.format(section))
                    pass

    def read_data_binary(self):
        if not self.end_header:
            raise Exception('header has not been read, or the file is not valid')
        with open(self.filepath, 'rb') as self.file:
            self.file.seek(self.end_header)
            for section in self.sections:
                if section == 'vertex':
                    self.read_vertices_binary_wo_numpy()
                elif section == 'edge':
                    self.read_edges_binary_wo_numpy()
                elif section == 'face':
                    self.read_faces_binary_wo_numpy()
                else:
                    print('user-defined elements are not supported: {0}'.format(section))
                    pass

    # ==========================================================================
    # read the individual section
    # ==========================================================================

    def read_vertices(self):
        count = 0
        for line in self.file:
            line = line.rstrip()
            parts = line.split()
            vertex = {}
            for i, prop in enumerate(self.vertex_properties):
                pname, ptype = prop
                vertex[pname] = self.property_types[ptype](parts[i])
            self.vertices.append(vertex)
            count += 1
            if count == self.number_of_vertices:
                break

    def read_edges(self):
        pass

    def read_faces(self):
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

    def numpy_vertex_ptypes(self):
        ext = self.binary_byte_order[self.format]
        dt = []
        for prop in self.vertex_properties:
            pname, ptype = prop
            dt.append((pname, ext + self.binary_property_types[ptype]))
        return dt

    def numpy_face_ptypes(self):
        ext = self.binary_byte_order[self.format]
        dt = []
        for prop in self.face_properties:
            if len(prop) == 2:
                pname, ptype = prop
                dt.append((pname, ext + self.binary_property_types[ptype]))
            elif len(prop) == 3:
                pname, ptype, plen = prop
                dt.append(('size', ext + self.binary_property_types[plen]))
                # this seems a nit of a hack
                dt.append(('v1', ext + self.binary_property_types[ptype]))
                dt.append(('v2', ext + self.binary_property_types[ptype]))
                dt.append(('v3', ext + self.binary_property_types[ptype]))
            else:
                pass
        return dt

    def read_vertices_binary_wo_numpy(self):
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

    def read_vertices_binary(self):
        # use pandas to read the data frames
        import numpy as np
        for line in np.fromfile(self.file, dtype=np.dtype(self.numpy_vertex_ptypes()), count=self.number_of_vertices):
            vertex = {}
            for i, prop in enumerate(self.vertex_properties):
                pname, ptype = prop
                vertex[pname] = line[i]
            self.vertices.append(vertex)

    def read_edges_binary_wo_numpy(self):
        pass

    def read_edges_binary(self):
        pass

    def read_faces_binary_wo_numpy(self):
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

    def read_faces_binary(self):
        # use pandas to read the data frames
        # how to deal with faces of variable length?
        import numpy as np
        for line in np.fromfile(self.file, dtype=np.dtype(self.numpy_face_ptypes()), count=self.number_of_faces):
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
    """"""

    def __init__(self, reader, precision=None):
        self.precision = precision
        self.reader    = reader
        self.vertices  = None
        self.edges     = None
        self.faces     = None
        self.parse()

    def parse(self):
        self.vertices = [(vertex['x'], vertex['y'], vertex['z']) for vertex in self.reader.vertices]
        self.faces = [face['vertex_indices'] for face in self.reader.faces]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import os
    import compas

    from compas.datastructures import Mesh

    ply = PLY(compas.get_bunny())

    mesh = Mesh.from_vertices_and_faces(ply.parser.vertices, ply.parser.faces)

    print(mesh.summary())
