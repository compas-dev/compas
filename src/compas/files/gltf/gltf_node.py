from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from math import fabs

from compas.files.gltf.gltf_children import GLTFChildren
from compas.files.gltf.helpers import get_matrix_from_col_major_list
from compas.files.gltf.helpers import matrix_to_col_major_order
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
    children : GLTFChildren
        Validated list of keys referencing :attr:`compas.files.GLTFNode.context.nodes`.
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
    mesh_key : int
        Key of the mesh within :attr:`compas.files.GLTFNode.context.meshes`.
    weights : list of floats
        Weights used for computing morph targets in the attached mesh.
    position : tuple
        xyz-coordinates of the node, calculated from the matrix and tree structure.
    transform : list of lists
        Matrix representing the displacement from the root node to the node.
    key : int
        Key of the node used in :attr:`compas.files.GLTFNode.context.nodes`.
    camera : int
        Key of the camera in :attr:`compas.files.GLTFNode.context.cameras`.
    skin : int
        Key of the skin in :attr:`compas.files.GLTFNode.context.skins`.
    extras : object
        Application-specific data.
    extensions : object
    context : GLTFContent
        GLTF context in which the node exists.
    mesh_data : GLTFMesh
        GLTFMesh used by this node.
    vertices : list
        List of xyz-coordinates of the points of the mesh used by this node.
    faces : list
        List of tuples of indices of the vertices of the faces of the mesh used by this node.

    """
    def __init__(self, context, name=None, extras=None, extensions=None):
        self.name = name
        self._children = GLTFChildren(context, [])
        self._matrix = None
        self._translation = None
        self._rotation = None
        self._scale = None
        self._mesh_key = None
        self.weights = None

        self.position = None
        self.transform = None
        self._key = None

        self._camera = None
        self._skin = None
        self.extras = extras
        self.extensions = extensions

        self.context = context
        self._set_key()

    def _set_key(self):
        key = len(self.context.nodes)
        while key in self.context.nodes:
            key += 1
        self.context.nodes[key] = self
        self._key = key

    @property
    def key(self):
        return self._key

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = GLTFChildren(self.context, value or [])

    @property
    def mesh_key(self):
        return self._mesh_key

    @mesh_key.setter
    def mesh_key(self, value):
        if value is not None and value not in self.context.meshes:
            raise Exception('Cannot find mesh {}'.format(value))
        self._mesh_key = value

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value):
        if value is not None and value not in self.context.cameras:
            raise Exception('Cannot find camera {}'.format(value))
        self._camera = value

    @property
    def skin(self):
        return self._skin

    @skin.setter
    def skin(self, value):
        if value is not None and value not in self.context.skin:
            raise Exception('Cannot find skin {}'.format(value))
        self._skin = value

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
        if not (self.translation or self.rotation or self.scale or self._matrix):
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

    @property
    def mesh_data(self):
        return self.context.meshes.get(self.mesh_key)

    @property
    def vertices(self):
        return self.context.get_node_vertices(self)

    @property
    def faces(self):
        return self.context.get_node_faces(self)

    def get_matrix_from_trs(self):
        """If the node's displacement from the origin is given by its translation, rotation and
        scale attributes, this method returns the matrix given by the composition of these
        attributes.

        Returns
        -------

        """
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

    def add_child(self, child_name=None, child_extras=None):
        """Creates a :class:`compas.files.GLTFNode` with name `child_name` (default `None`) and extras `child_extras`
        (default `None`), and adds this node to the children of this node.

        Parameters
        ----------
        child_name : str
        child_extras : object

        Returns
        -------
        :class:`compas.files.GLTFNode`
        """
        return self.context.add_child_to_node(self, child_name, child_extras)

    def add_mesh(self, mesh):
        """Adds an existing mesh to this node if `mesh` is a valid mesh key, or creates and adds a
        mesh to this node and its context.

        Parameters
        ----------
        mesh : Union[int, Mesh]

        Returns
        -------

        """
        return self.context.add_mesh_to_node(self, mesh)

    def to_data(self, node_index_by_key, mesh_index_by_key, camera_index_by_key, skin_index_by_key):
        """Returns a JSONable dictionary object in accordance with glTF specifications.

        Parameters
        ----------
        node_index_by_key : dict
        mesh_index_by_key : dict
        camera_index_by_key : dict
        skin_index_by_key : dict

        Returns
        -------
        dict
        """
        node_dict = {}
        if self.name is not None:
            node_dict['name'] = self.name
        if self.children:
            node_dict['children'] = [node_index_by_key[key] for key in self.children]
        if self.matrix and self.matrix != identity_matrix(4):
            node_dict['matrix'] = matrix_to_col_major_order(self.matrix)
        else:
            if self.translation:
                node_dict['translation'] = self.translation
            if self.rotation:
                node_dict['rotation'] = self.rotation
            if self.scale:
                node_dict['scale'] = self.scale
        if self.mesh_key is not None:
            node_dict['mesh'] = mesh_index_by_key[self.mesh_key]
        if self._camera is not None:
            node_dict['camera'] = camera_index_by_key[self._camera]
        if self._skin is not None:
            node_dict['skin'] = skin_index_by_key[self._skin]
        if self.extras:
            node_dict['extras'] = self.extras
        if self.extensions is not None:
            node_dict['extensions'] = self.extensions
        return node_dict

    @classmethod
    def from_data(cls, node, context):
        """Creates a :class:`compas.files.GLTFNode` from a glTF node dictionary
        and inserts it in the provided context.

        Parameters
        ----------
        node : dict
        context : :class:`compas.files.GLTFContent`

        Returns
        -------
        :class:`compas.files.GLTFNode`
        """
        if node is None:
            return None
        gltf_node = cls(
            context=context,
            name=node.get('name'),
            extras=node.get('extras'),
            extensions=node.get('extensions'),
        )
        # Accessing protected attribute to bypass validation:
        # Nodes may reference children that haven't yet been added to the GLTFContent
        gltf_node.children._values = node.get('children', [])

        gltf_node.translation = node.get('translation')
        gltf_node.rotation = node.get('rotation')
        gltf_node.scale = node.get('scale')
        gltf_node.matrix = get_matrix_from_col_major_list(node['matrix']) if 'matrix' in node else None
        gltf_node.weights = node.get('weights')
        gltf_node.mesh_key = node.get('mesh')
        gltf_node.camera = node.get('camera')
        gltf_node.skin = node.get('skin')
        return gltf_node
