from compas_rhino.conversions import point_to_rhino


import Rhino


TOLERANCE = 1e-6


class BrepReconstructionError(BaseException):
    pass


class RhinoLoopBuilder(object):
    def __init__(self, loop=None, instance=None):
        self.loop = loop
        self.instance = instance

    def add_trim(self, curve, edge_index, is_reversed, iso_status):
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
    def __init__(self, face=None, instance=None):
        self.face = face
        self.instance = instance

    @property
    def result(self):
        return self.face

    def add_loop(self, loop_type):
        loop = self.instance.Loops.Add(loop_type, self.face)
        return RhinoLoopBuilder(loop, self.instance)


class RhinoBrepBuilder(object):
    """Reconstructs a Rhino.Geometry.Brep from COMPAS types"""   
    
    def __init__(self):
        self._instance = Rhino.Geometry.Brep()

    @property
    def result(self):
        is_valid, log = self._instance.IsValidWithLog()
        if not is_valid:
            raise BrepReconstructionError("Brep reconstruction failed!\n{}".format(log))
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
        surface_index = self._instance.AddSurface(surface.rhino_surface)
        face = self._instance.Faces.Add(surface_index)
        return RhinoFaceBuilder(face=face, instance=self._instance)


