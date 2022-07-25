from compas.geometry import Geometry
from compas.plugins import pluggable
from compas.plugins import PluginNotInstalledError


LINEAR_DEFLECTION = 1e-3


@pluggable(category="factories")
def new_brep(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_brep(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_mesh(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_box(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_cylinder(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_sphere(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_cone(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_surface(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_torus(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_sweep(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_step_file(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_polygons(*args, **kwargs):
    raise PluginNotInstalledError()


@pluggable(category="factories")
def from_curves(*args, **kwargs):
    raise PluginNotInstalledError()


class BrepType:
    """
    Possible types of a Brep
    """

    COMPOUND = 0
    COMPSOLID = 1
    SHELL = 2
    FACE = 3
    WIRE = 4
    EDGE = 5
    VERTEX = 6
    SHAPE = 7


class BrepOrientation:
    """
    Possible orientations of a Brep
    """

    FORWARD = 0
    REVERSED = 1
    INTERNAL = 2
    EXTERNAL = 3


class Brep(Geometry):
    """Contains the topological and geometrical information of a Brep shape.

    This class serves as an interface for a Brep and allows instantiating a Brep object depending on the available Backend.
    Note: this is not a full implementation of Brep and rather relies on COMPAS's plugin system for actual implementation.

    Attributes
    ----------
    vertices : list[:class:`~compas_rhino.geometry.BrepVertex`], read-only
        The vertices of the Brep.
    edges : list[:class:`~compas_rhino.geometry.BrepEdge`], read-only
        The edges of the Brep.
    loops : list[:class:`~compas_rhino.geometry.BrepLoop`], read-only
        The loops of the Brep.
    faces : list[:class:`~compas_rhino.geometry.BrepFace`], read-only
        The faces of the Brep.
    frame : :class:`~compas.geometry.Frame`, read-only
        The local coordinate system of the Brep.
    area : float, read-only
        The surface area of the Brep.
    volume : float, read-only
        The volume of the regions contained by the Brep.

    Other Attributes
    ----------------
    type : :class:`~compas.geometry.BrepType`, read-only
        The type of Brep shape.
    orientation : :class:`~compas.geometry.BrepOrientation`, read-obly
        Orientation of the shape.

    """

    def __new__(cls, *args, **kwargs):
        return new_brep(cls, *args, **kwargs)

    def __init__(self, name=None):
        super(Brep, self).__init__(name=name)

    def __str__(self):
        lines = [
            "Brep",
            "-----",
            "Vertices: {}".format(self.vertices),
            "Edges: {}".format(self.edges),
            "Loops: {}".format(self.loops),
            "Faces: {}".format(self.faces),
            "Frame: {}".format(self.frame),
            "Area: {}".format(self.area),
            "Volume: {}".format(self.volume),
        ]
        return "\n".join(lines)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        faces = []
        for face in self.faces:
            faces.append(face.data)
        return {"faces": faces}

    @data.setter
    def data(self):
        raise NotImplementedError

    @property
    def orientation(self):
        raise NotImplementedError

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def type(self):
        raise NotImplementedError

    @property
    def is_shell(self):
        raise NotImplementedError

    @property
    def is_solid(self):
        raise NotImplementedError

    @property
    def is_compound(self):
        raise NotImplementedError

    @property
    def is_compoundsolid(self):
        raise NotImplementedError

    @property
    def is_orientable(self):
        raise NotImplementedError

    @property
    def is_closed(self):
        raise NotImplementedError

    @property
    def is_infinite(self):
        raise NotImplementedError

    @property
    def is_convex(self):
        raise NotImplementedError

    @property
    def is_manifold(self):
        raise NotImplementedError

    @property
    def is_surface(self):
        raise NotImplementedError

    # ==============================================================================
    # Geometric Components
    # ==============================================================================

    @property
    def points(self):
        raise NotImplementedError

    @property
    def curves(self):
        raise NotImplementedError

    @property
    def surfaces(self):
        raise NotImplementedError

    # ==============================================================================
    # Topological Components
    # ==============================================================================

    @property
    def vertices(self):
        raise NotImplementedError

    @property
    def edges(self):
        raise NotImplementedError

    @property
    def loops(self):
        raise NotImplementedError

    @property
    def faces(self):
        raise NotImplementedError

    @property
    def shells(self):
        raise NotImplementedError

    @property
    def solids(self):
        raise NotImplementedError

    # ==============================================================================
    # Geometric Properties
    # ==============================================================================

    @property
    def frame(self):
        raise NotImplementedError

    @property
    def area(self):
        raise NotImplementedError

    @property
    def volume(self):
        raise NotImplementedError

    @property
    def centroid(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_brep(cls, brep):
        return from_brep(brep)

    @classmethod
    def from_step_file(cls, filename):
        return from_step_file(filename)

    @classmethod
    def from_polygons(cls, polygons):
        return from_polygons(polygons)

    @classmethod
    def from_curves(cls, curves):
        return from_curves(curves)

    @classmethod
    def from_box(cls, box):
        return from_box(box)

    @classmethod
    def from_sphere(cls, sphere):
        return from_sphere(sphere)

    @classmethod
    def from_cylinder(cls, cylinder):
        return from_cylinder(cylinder)

    @classmethod
    def from_cone(cls, cone):
        return from_cone(cone)

    @classmethod
    def from_torus(cls, torus):
        return from_torus(torus)

    @classmethod
    def from_mesh(cls, mesh):
        return from_mesh(mesh)

    @classmethod
    def from_faces(cls, faces):
        raise NotImplementedError

    @classmethod
    def from_extrusion(cls, curve, vector):
        raise NotImplementedError

    @classmethod
    def from_sweep(cls, profile, path):
        raise NotImplementedError

    # create pipe
    # create patch
    # create offset

    # ==============================================================================
    # Boolean Constructors
    # ==============================================================================

    @classmethod
    def from_boolean_difference(cls, A, B):
        raise NotImplementedError

    @classmethod
    def from_boolean_intersection(cls, A, B):
        raise NotImplementedError

    @classmethod
    def from_boolean_union(cls, A, B):
        raise NotImplementedError

    # ==============================================================================
    # Converters
    # ==============================================================================

    def to_json(self, filepath):
        raise NotImplementedError

    def to_step(self, filepath):
        raise NotImplementedError

    def to_tesselation(self, linear_deflection=LINEAR_DEFLECTION):
        raise NotImplementedError

    def to_meshes(self, u=16, v=16):
        raise NotImplementedError

    def to_viewmesh(self):
        raise NotImplementedError

    # ==============================================================================
    # Relationships
    # ==============================================================================

    def vertex_neighbors(self, vertex):
        raise NotImplementedError

    def vertex_edges(self, vertex):
        raise NotImplementedError

    def vertex_faces(self, vertex):
        raise NotImplementedError

    # ==============================================================================
    # Other Methods
    # ==============================================================================

    # flip
    # join
    # join edges
    # join naked edges
    # merge coplanar faces
    # remove fins
    # remove holes
    # repair
    # rotate
    # scale
    # trim
    # rotate
    # translate
    # unjoin edges

    def make_solid(self):
        raise NotImplementedError

    def check(self):
        raise NotImplementedError

    def sew(self):
        raise NotImplementedError

    def fix(self):
        raise NotImplementedError

    def cull_unused_vertices(self):
        """Remove all unused vertices.

        Returns
        -------
        None

        """
        NotImplementedError

    def cull_unused_edges(self):
        """Remove all unused edges.

        Returns
        -------
        None

        """
        NotImplementedError

    def cull_unused_loops(self):
        """Remove all unused loops.

        Returns
        -------
        None

        """
        NotImplementedError

    def cull_unused_faces(self):
        """Remove all unused faces.

        Returns
        -------
        None

        """
        NotImplementedError

    def transform(self, matrix):
        raise NotImplementedError

    def transformed(self, matrix):
        raise NotImplementedError

    def contours(self, planes):
        raise NotImplementedError

    def slice(self, plane):
        raise NotImplementedError

    def split(self, other):
        raise NotImplementedError

    def overlap(self, other, deflection=LINEAR_DEFLECTION, tolerance=0.0):
        raise NotImplementedError
