from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from math import fabs

from compas.geometry import identity_matrix
from compas.geometry import matrix_from_quaternion
from compas.geometry import matrix_from_scale_factors
from compas.geometry import matrix_from_translation
from compas.geometry import multiply_matrices


class GLTFNode(object):
    """Object representing the COMPAS consumable part of a glTF node.

    Attributes
    ----------
    name : str
        Name of the node.
    children : list
        Child nodes referenced by node_key.
    matrix : list of lists
        Matrix representing the displacement from node's parent to the node.
        Default value is the identity matrix.
        Cannot be set when any of translation, rotation or scale is set.
    translation : list of floats
        xyz-coordinates of the translation displacement of the node.
        Cannot be set when :attr:`compas.files.GLTFNode.matrix` is set.
    rotation : list of floats
        Unit quaternion representing the rotational displacement of the node.
        Cannot be set when :attr:`compas.files.GLTFNode.matrix` is set.
    scale : list of floats
        List of length 3 representing the scaling displacement of the node.
        Cannot be set when :attr:`compas.files.GLTFNode.matrix` is set.
    mesh_index : int
        Index of the associated mesh within the JSON.
    weights : list of floats
        Weights used for computing morph targets in the attached mesh.
    position : tuple
        xyz-coordinates of the node, calculated from the matrix and tree structure.
    transform : list of lists
        Matrix representing the displacement from the root node to the node.
    mesh_data : :class:`compas.files.MeshData`
        Contains mesh data, if any.
    node_key : int or str
        Key of the node used in :attr:`compas.files.GLTFScene.nodes`.
    camera : int
        Index of the camera in :attr:`compas.files.GLTF.ancillaries`.
    skin : int
        Index of the skin in :attr:`compas.files.GLTF.ancillaries`.
    extras : object
        Application-specific data.
    """
    def __init__(self):
        self.name = None
        self.children = []
        self._matrix = None
        self._translation = None
        self._rotation = None
        self._scale = None
        self.mesh_index = None
        self.weights = None

        self.position = None
        self.transform = None
        self._mesh_data = None
        self.node_key = None

        self.camera = None
        self.skin = None
        self.extras = None

    @property
    def mesh_data(self):
        return self._mesh_data

    @mesh_data.setter
    def mesh_data(self, value):
        if not value.faces or not value.vertices:
            raise Exception('Invalid mesh at node {}.  Meshes are expected '
                            'to have vertices and faces.'.format(self.node_key))
        self._mesh_data = value

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, value):
        if value is None:
            self._translation = value
            return
        if self._matrix:
            raise Exception('Cannot set translation when matrix is set.')
        if not isinstance(value, list) or len(value) != 3:
            raise Exception('Invalid translation. Translations are expected to be of the form [x, y, z].')
        self._translation = value

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        if value is None:
            self._rotation = value
            return
        if self._matrix:
            raise Exception('Cannot set rotation when matrix is set.')
        if not isinstance(value, list) or len(value) != 4 or fabs(sum([q**2 for q in value]) - 1) > 1e-03:
            raise Exception('Invalid rotation.  Rotations are expected to be given as '
                            'unit quaternions of the form [q1, q2, q3, q4]')
        self._rotation = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if value is None:
            self._scale = value
            return
        if self._matrix:
            raise Exception('Cannot set scale when matrix is set.')
        if not isinstance(value, list) or len(value) != 3:
            raise Exception('Invalid scale.  Scales are expected to be of the form [s1, s2, s3]')
        self._scale = value

    @property
    def matrix(self):
        if not self.translation and not self.rotation and not self.scale and not self._matrix:
            return identity_matrix(4)
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        if value is None:
            self._matrix = value
            return
        if self.translation or self.rotation or self.scale:
            raise Exception('Cannot set matrix when translation, rotation or scale is set.')
        if not isinstance(value, list) or not value or not value[0] or not isinstance(value[0], list):
            raise Exception('Invalid matrix. A list of lists is expected.')
        if len(value) != 4 or len(value[0]) != 4:
            raise Exception('Invalid matrix. A 4x4 matrix is expected.')
        if value[3] != [0, 0, 0, 1]:
            raise Exception('Invalid matrix.  A matrix without shear or skew is expected.  It must be of '
                            'the form TRS, where T is a translation, R is a rotation and S is a scaling.')
        self._matrix = value

    def get_matrix_from_trs(self):
        matrix = identity_matrix(4)
        if self.translation:
            translation = matrix_from_translation(self.translation)
            matrix = multiply_matrices(matrix, translation)
        if self.rotation:
            rotation = matrix_from_quaternion(self.rotation)
            matrix = multiply_matrices(matrix, rotation)
        if self.scale:
            scale = matrix_from_scale_factors(self.scale)
            matrix = multiply_matrices(matrix, scale)
        return matrix
