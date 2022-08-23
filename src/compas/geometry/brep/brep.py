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


class BrepType(object):
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


class BrepOrientation(object):
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
            "Vertices: {}".format(len(self.vertices)),
            "Edges: {}".format(len(self.edges)),
            "Loops: {}".format(len(self.loops)),
            "Faces: {}".format(len(self.faces)),
            "Frame: {}".format(self.frame),
            "Area: {}".format(self.area),
            "Volume: {}".format(self.volume),
        ]
        return "\n".join(lines)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def DATASCHEMA(self):
        import schema

        return schema.Schema(
            {
                "faces": list,
            }
        )

    @property
    def JSONSCHEMANAME(self):
        return "brep"

    @property
    def data(self):
        faces = []
        for face in self.faces:
            faces.append(face.data)
        return {"faces": faces}

    @data.setter
    def data(self):
        raise NotImplementedError

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def native_brep(self):
        """The native representation of the Brep wrapped by this instance

        Returns
        -------
        Any
            A native backend type
        """
        raise NotImplementedError

    @property
    def orientation(self):
        """
        Returns the current orientation of this Brep.

        Returns
        -------
        :class:`~compas.geometry.BrepOrientation`
        """
        raise NotImplementedError

    @property
    def type(self):
        """
        Returns the type of this Brep.

        Returns
        -------
        :class:`~compas.geometry.BrepType`
        """
        raise NotImplementedError

    @property
    def is_shell(self):
        """
        Returns True if the geometry of this Brep is a shell.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_solid(self):
        """
        Returns True if the geometry of this Brep is a solid.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_compound(self):
        """
        Returns True if the geometry of this Brep is a compound.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_compoundsolid(self):
        """
        Returns True if the geometry of this Brep is a compound solid.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_orientable(self):
        """
        Returns True if the geometry of this Brep is orientable.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_closed(self):
        """
        Returns True if the geometry of this Brep is closed.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_infinite(self):
        """
        Returns True if the geometry of this Brep is infinte.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_convex(self):
        """
        Returns True if the geometry of this Brep is convex.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_manifold(self):
        """
        Returns True if the geometry of this Brep is a manifold.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_surface(self):
        """
        Returns True if the geometry of this Brep is a surface.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    # ==============================================================================
    # Geometric Components
    # ==============================================================================

    @property
    def points(self):
        """
        Returns the points which underly this brap's vertices.

        Returns
        -------
        List[:class:`~compas.geometry.Point`]
        """
        raise NotImplementedError

    @property
    def curves(self):
        """
        Returns the curves which underly this breb's edges.

        Returns
        -------
        List[:class:`compas.geometry.Curve`]
        """
        raise NotImplementedError

    @property
    def surfaces(self):
        """
        Returns the surfaces which underly this brep's faces.

        Returns
        -------
        List[:class:`~compas.geometry.NurbsSurface`]
        """
        raise NotImplementedError

    # ==============================================================================
    # Topological Components
    # ==============================================================================

    @property
    def vertices(self):
        """
        Return the vertices of this brep.

        Returns
        -------
        List[:class:`compas.geometry.BrepVertex`]
        """
        raise NotImplementedError

    @property
    def edges(self):
        """
        Return the edges of this brep.

        Returns
        -------
        List[:class:`compas.geometry.BrepEdge`]
        """
        raise NotImplementedError

    @property
    def loops(self):
        """
        Return the loops of this brep.

        Returns
        -------
        List[:class:`compas.geometry.BrepLoop`]
        """
        raise NotImplementedError

    @property
    def faces(self):
        """
        Return the faces of this brep.

        Returns
        -------
        List[:class:`compas.geometry.BrepFace]
        """
        raise NotImplementedError

    @property
    def shells(self):
        """
        Returns the shells of this brep, if any.
        TODO: do we have a type for this? is this just a list of faces?
        Returns
        -------
        """
        raise NotImplementedError

    @property
    def solids(self):
        """
        Returns the solids of this brep.
        TODO: do we have a type for this?
        Returns
        -------
        """
        raise NotImplementedError

    # ==============================================================================
    # Geometric Properties
    # ==============================================================================

    @property
    def frame(self):
        """
        Returns the Frame of this Brep.

        Returns
        -------
        :class:`~compas.geometry.Frame`
        """
        raise NotImplementedError

    @property
    def area(self):
        """
        Returns the calculated area of this brep.

        Returns
        -------
        float
        """
        raise NotImplementedError

    @property
    def volume(self):
        """
        Returns the calculated volume of this brep.

        Returns
        -------
        float
        """
        raise NotImplementedError

    @property
    def centroid(self):
        """Returns the center of mass point of this Brep.

        Returns
        -------
        :class:`~compas.geometry.Point`

        """
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_brep(cls, brep):
        """Create a Brep from an instance of a backend Brep.

        Parameters
        ----------
        brep : an instance of a Brep from a supported Brep backend
            e.g. Rhino.Geometry.Brep

        Returns
        -------
        :class:`~compas.geometry.Brep`
        """
        return from_brep(brep)

    @classmethod
    def from_step_file(cls, filename):
        """Conctruct a BRep from the data contained in a STEP file.

        Parameters
        ----------
        filename : str

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        return from_step_file(filename)

    @classmethod
    def from_polygons(cls, polygons):
        """Construct a Brep from a set of polygons.

        Parameters
        ----------
        polygons : list[:class:`~compas.geometry.Polygon`]

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        return from_polygons(polygons)

    @classmethod
    def from_curves(cls, curves):
        """Construct a Brep from a set of curves.

        Parameters
        ----------
        curves : List[:class:`~compas.geometry.NurbsCurve`]

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        return from_curves(curves)

    @classmethod
    def from_box(cls, box):
        """Construct a Brep from a COMPAS box.

        Parameters
        ----------
        box : :class:`~compas.geometry.Box`

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        return from_box(box)

    @classmethod
    def from_sphere(cls, sphere):
        """Construct a Brep from a COMPAS sphere.

        Parameters
        ----------
        sphere : :class:`~compas.geometry.Sphere`

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        return from_sphere(sphere)

    @classmethod
    def from_cylinder(cls, cylinder):
        """Construct a Brep from a COMPAS cylinder.

        Parameters
        ----------
        cylinder : :class:`~compas.geometry.Cylinder`

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        return from_cylinder(cylinder)

    @classmethod
    def from_cone(cls, cone):
        """Construct a Brep from a COMPAS cone.

        Parameters
        ----------
        cone : :class:`~compas.geometry.Cone`

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        return from_cone(cone)

    @classmethod
    def from_torus(cls, torus):
        """Construct a Brep from a COMPAS torus.

        Parameters
        ----------
        torus : :class:`~compas.geometry.Torus`

        Returns
        -------
        :class:`~compas.geometry.BRep`

        """
        return from_torus(torus)

    @classmethod
    def from_mesh(cls, mesh):
        """Construct a Brep from a COMPAS mesh.

        Parameters
        ----------
        mesh : :class:`~compas.datastructures.Mesh`

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        return from_mesh(mesh)

    @classmethod
    def from_brepfaces(cls, faces):
        """Make a Brep from a list of Brep faces forming an open or closed shell.

        Parameters
        ----------
        faces : List[:class:`~compas.geometry.BrepFace`]

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        raise NotImplementedError

    @classmethod
    def from_extrusion(cls, curve, vector):
        """Construct a Brep by extruding a closed curve along a direction vector."""
        raise NotImplementedError

    @classmethod
    def from_sweep(cls, profile, path):
        """Construct a BRep by sweeping a profile along a path.

        Parameters
        ----------
        profile : Union[:class:`~compas.geometry.BrepEdge`, :class:`~compas.geometry.BrepFace`]
            the profile to sweep. Either an edge or a face.
        path : :class:`~compas.geometry.BrepLoop`
            the path to sweep along

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        raise NotImplementedError

    # ==============================================================================
    # Boolean Constructors
    # ==============================================================================

    @classmethod
    def from_boolean_difference(cls, brep_a, brep_b):
        """Construct a Brep from the boolean difference of two other Breps.

        Parameters
        ----------
        brep_a : :class:`~compas.geometry.Brep`
        brep_b : :class:`~compas.geometry.Brep`

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        raise NotImplementedError

    @classmethod
    def from_boolean_intersection(cls, brep_a, brep_b):
        """Construct a BRep from the boolean intersection of two other Breps.

        Parameters
        ----------
        brep_a : :class:`~compas.geometry.Brep`
        brep_b : :class:`~compas.geometry.Brep`

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        raise NotImplementedError

    @classmethod
    def from_boolean_union(cls, brep_a, brep_b):
        """Construct a Brep from the boolean union of two other Breps.

        Parameters
        ----------
        brep_a : :class:`~compas.geometry.Brep`
        brep_b : :class:`~compas.geometry.Brep`

        Returns
        -------
        :class:`~compas.geometry.Brep`

        """
        raise NotImplementedError

    # ==============================================================================
    # Converters
    # ==============================================================================

    def to_json(self, filepath):
        """Export the BRep to a JSON file.

        Parameters
        ----------
        filepath : str
            Location of the file.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def to_step(self, filepath):
        """Write the BRep shape to a STEP file.

        Parameters
        ----------
        filepath : str
            Location of the file.
        schema : str, optional
            STEP file format schema.
        unit : str, optional
            Base units for the geometry in the file.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def to_tesselation(self, linear_deflection=LINEAR_DEFLECTION):
        """Create a tesselation of the shape for visualisation.

        Parameters
        ----------
        linear_deflection : float, optional
            Allowable deviation between curved geometry and mesh discretisation.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`

        """
        raise NotImplementedError

    def to_meshes(self, u=16, v=16):
        """Convert the faces of this Brep shape to meshes.

        Parameters
        ----------
        u : int, optional
            The number of mesh faces in the U direction of the underlying surface geometry of every face of the Brep.
        v : int, optional
            The number of mesh faces in the V direction of the underlying surface geometry of every face of the Brep.

        Returns
        -------
        list[:class:`~compas.datastructures.Mesh`]

        """
        raise NotImplementedError

    def to_viewmesh(self, precision):
        """
        Convert this Brep to a view mesh
        Parameters
        ----------
        precision:
            float

        Returns
        -------

        """
        raise NotImplementedError

    # ==============================================================================
    # Relationships
    # ==============================================================================

    def vertex_neighbors(self, vertex):
        """Identify the neighbouring vertices of a given vertex.

        Parameters
        ----------
        vertex : :class:`~compas.geometry.BrepVertex`

        Returns
        -------
        List[:class:`~compas.geometry.BrepVertex`]

        """
        raise NotImplementedError

    def vertex_edges(self, vertex):
        """Identify the edges connected to a given vertex.

        Parameters
        ----------
        vertex : :class:`~compas.geometry.BrepVertex`

        Returns
        -------
        List[:class:`~compas.geometry.BrepEdge`]

        """
        raise NotImplementedError

    def vertex_faces(self, vertex):
        """Identify the faces connected to a vertex.

        Parameters
        ----------
        vertex : :class:`~compas.geometry.BrepVertex`

        Returns
        -------
        List[:class:`~compas.geometry.BrepFace`]

        """
        raise NotImplementedError

    # ==============================================================================
    # Other Methods
    # ==============================================================================

    def trim(self, trimming_plane, tolerance):
        """Trim this Brep using the given trimming plane

        Parameters
        ----------
        trimming_plane: defines the trimming plane
            :class:`~compas.geometry.Frame

        tolerance: the tolerance to use when trimming
            float
        """
        raise NotImplementedError

    def is_valid(self):
        """
        Returns True if this brep is a vaild brep.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    def make_solid(self):
        """Convert the current shape to a solid if it is a shell.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def sew(self):
        """Sew together the individual parts of the shape.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def fix(self):
        """Fix the shell.

        Returns
        -------
        None

        """
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

    def contours(self, planes):
        """Generate contour lines by slicing the Brep shape with a series of planes.

        Parameters
        ----------
        planes : list[:class:`~compas.geometry.Plane`]
            The slicing planes.

        Returns
        -------
        list[list[:class:`~compas.geometry.Polyline`]]
            A list of polylines per plane.

        """
        raise NotImplementedError

    def slice(self, plane):
        """Slice through the BRep with a plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`

        Returns
        -------
        :class:`~compas.geometry.BrepFace`
        """

    def split(self, other):
        """Slice through the BRep with a plane.

        Parameters
        ----------
        other : :class:`~compas.geomtery.Brep`
            Another Brep.

        Returns
        -------
        List[:class:`~compas.geometry.Brep`]
        """
        raise NotImplementedError

    def overlap(self, other, deflection=LINEAR_DEFLECTION, tolerance=0.0):
        """Compute the overlap between this BRep and another.

        Parameters
        ----------
        other : :class:`~compas.geometry.Brep`
            The other Brep.
        deflection : float, optional
            Allowable deflection for mesh generation used for proximity detection.
        tolerance : float, optional
            Tolerance for overlap calculation.

        Returns
        -------
        Tuple[List[:class:`~compas.geometry.BrepFace`]]

        """
        raise NotImplementedError
