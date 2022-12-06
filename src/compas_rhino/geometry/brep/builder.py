from compas.geometry import BrepInvalidError
from compas_rhino.conversions import point_to_rhino


import Rhino


TOLERANCE = 1e-6


class RhinoLoopBuilder(object):
    """Builds a Brep loop.

    Attributes
    ----------
    result : :rhino: Rhino.Geometry.BrepTrim
        The created loop.

    """

    def __init__(self, loop=None, instance=None):
        self.loop = loop
        self.instance = instance

    def add_trim(self, curve, edge_index, is_reversed, iso_status):
        """Add trim to the new Brep.

        Parameters
        ==========
        curve : :rhino:`Rhino.Geometry.NurbsCurve`
            The curve representing the geometry of this trim.
        edge_index : int
            The index of the already added edge which corresponds with this trim.
        is_reversed : bool
            True if this trim is reversed in direction from its associated edge.
        iso_status : :rhino:`Rhino.Geometry.IsoStatus`
            The iso status of this trim.

        Returns
        =======
        :rhino:`Rhino.Geometry.BrepTrim`
            The newly added BrepTrim instance.

        """
        c_index = self.instance.AddTrimCurve(curve)
        edge = self.instance.Edges[edge_index]
        trim = self.instance.Trims.Add(edge, is_reversed, self.loop, c_index)
        trim.IsoStatus = iso_status
        trim.SetTolerances(TOLERANCE, TOLERANCE)
        return trim

    @property
    def result(self):
        return self.loop


class RhinoFaceBuilder(object):
    """Builds a BrepFace.

    Serves as context for reconstructing the loop elements associated with this face.

    Attributes
    ==========
    result : :rhino:`Rhino.Geometry.BrepFace`
        The resulting BrepFace.

    """

    def __init__(self, face=None, instance=None):
        self.face = face
        self.instance = instance

    @property
    def result(self):
        return self.face

    def add_loop(self, loop_type):
        """Add a new loop to this face.

        Returns a new builder to be used by all the trims of the newly added loop.

        Parameters
        ==========
        loop_type : :rhino:`Rhino.Geometry.BrepLoopType`
            The enumeration value representing the type of this loop.

        Returns
        =======
        :class:`compas_rhino.geometry.RhinoLoopBuilder`

        """
        loop = self.instance.Loops.Add(loop_type, self.face)
        return RhinoLoopBuilder(loop, self.instance)


class RhinoBrepBuilder(object):
    """Reconstructs a Rhino.Geometry.Brep from COMPAS types

    Attributes
    ==========
    result : :rhino:`Rhino.Geometry.Brep`
        The Brep resulting from the reconstruction, if successful.

    """

    def __init__(self):
        self._instance = Rhino.Geometry.Brep()

    @property
    def result(self):
        is_valid, log = self._instance.IsValidWithLog()
        if not is_valid:
            raise BrepInvalidError("Brep reconstruction failed!\n{}".format(log))
        return self._instance

    def add_vertex(self, point):
        """Add vertext to a new Brep

        point : :class:`~compas.geometry.Point`

        Returns
        -------
        :rhino:`Rhino.Geometry.BrepVertex`

        """
        return self._instance.Vertices.Add(point_to_rhino(point), TOLERANCE)

    def add_edge(self, edge_curve, start_vertex, end_vertex):
        """Add edge to the new Brep

        edge_curve : :class:`~compas_rhino.geometry.RhinoNurbsCurve`
        start_vertex: int
            index of the vertex at the start of this edge
        end_vertex: int
            index of the vertex at the end of this edge

        Returns
        -------
        :rhino:`Rhino.Geometry.BrepEdge`

        """
        curve_index = self._instance.AddEdgeCurve(edge_curve)
        s_vertex = self._instance.Vertices[start_vertex]
        e_vertex = self._instance.Vertices[end_vertex]
        return self._instance.Edges.Add(s_vertex, e_vertex, curve_index, TOLERANCE)

    def add_face(self, surface):
        """Creates and adds a new face to the brep.

        Returns a new builder to be used by all the loops related to his new face to add themselves.

        Parameters
        ==========
        surface : :rhino:`Rhino.Geometry.Surface`
            The surface of this face.

        Returns
        =======
        :class:`compas_rhino.geometry.RhinoFaceBuilder`

        """
        surface_index = self._instance.AddSurface(surface.rhino_surface)
        face = self._instance.Faces.Add(surface_index)
        return RhinoFaceBuilder(face=face, instance=self._instance)
