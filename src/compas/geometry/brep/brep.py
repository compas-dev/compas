from compas.geometry import Geometry
from compas.plugins import pluggable


@pluggable(category="factories")
def new_brep(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category="factories")
def new_brep_from_mesh(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category="factories")
def new_brep_from_box(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category="factories")
def new_brep_from_cylinder(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category="factories")
def new_brep_from_sphere(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category="factories")
def new_brep_from_cone(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category="factories")
def new_brep_from_surface(cls, *args, **kwargs):
    raise NotImplementedError


class BRep(Geometry):
    """Class for Boundary Representation of geometric entities.

    Attributes
    ----------
    vertices : list[:class:`~compas_occ.brep.BRepVertex`], read-only
        The vertices of the BRep.
    edges : list[:class:`~compas_occ.brep.BRepEdge`], read-only
        The edges of the BRep.
    loops : list[:class:`~compas_occ.brep.BRepLoop`], read-only
        The loops of the BRep.
    faces : list[:class:`~compas_occ.brep.BRepFace`], read-only
        The faces of the BRep.
    frame : :class:`~compas.geometry.Frame`, read-only
        The local coordinate system of the BRep.
    area : float, read-only
        The surface area of the BRep.
    volume : float, read-only
        The volume of the regions contained by the BRep.

    Other Attributes
    ----------------
    occ_shape : ``TopoDS_Shape``
        The underlying OCC shape of the BRep.
    type : {TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL, TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE}, read-only
        The type of BRep shape.
    orientation : {TopAbs_FORWARD, TopAbs_REVERSED, TopAbs_INTERNAL, TopAbs_EXTERNAL}, read-only
        Orientation of the shape.

    Examples
    --------
    Constructors

    """

    def __new__(cls, *args, **kwargs):
        return new_brep(cls, *args, **kwargs)

    def __init__(self, name=None):
        super(BRep, self).__init__(name=name)

    def __str__(self):
        lines = [
            "BRep",
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
        pass

    @property
    def is_surface(self):
        pass

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
    def from_shape(cls, shape):
        raise NotImplementedError

    @classmethod
    def from_step(cls, filename):
        raise NotImplementedError

    @classmethod
    def from_polygons(cls, polygons):
        raise NotImplementedError

    @classmethod
    def from_curves(cls, curves):
        raise NotImplementedError

    @classmethod
    def from_box(cls, box):
        return new_brep_from_box(cls, box)

    @classmethod
    def from_sphere(cls, sphere):
        raise NotImplementedError

    @classmethod
    def from_cylinder(cls, cylinder):
        raise NotImplementedError

    @classmethod
    def from_cone(cls, cone):
        raise NotImplementedError

    @classmethod
    def from_torus(cls, torus):
        raise NotImplementedError

    @classmethod
    def from_mesh(cls, mesh):
        raise NotImplementedError

    @classmethod
    def from_faces(cls, faces):
        raise NotImplementedError

    @classmethod
    def from_extrusion(cls, curve, vector):
        pass

    @classmethod
    def from_sweep(cls, profile, path):
        pass

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

    def to_step(self, filepath, schema="AP203", unit="MM"):
        raise NotImplementedError

    def to_tesselation(self, linear_deflection=1e-3):
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
        pass

    def cull_unused_edges(self):
        """Remove all unused edges.

        Returns
        -------
        None

        """
        pass

    def cull_unused_loops(self):
        """Remove all unused loops.

        Returns
        -------
        None

        """
        pass

    def cull_unused_faces(self):
        """Remove all unused faces.

        Returns
        -------
        None

        """
        pass

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

    def overlap(self, other, deflection=1e-3, tolerance=0.0):
        raise NotImplementedError
