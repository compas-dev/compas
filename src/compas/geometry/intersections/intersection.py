class Intersection:
    def __init__(self):
        pass

    def is_a(self):
        return self.__class__.__name__

    def is_overlap(self):
        pass

    def is_point(self):
        pass

    @property
    def overlapA(self):
        pass

    @property
    def overlapB(self):
        pass

    @property
    def ParameterA(self):
        pass

    @property
    def ParameterB(self):
        pass

    @property
    def PointA(self):
        pass

    @property
    def PointA2(self):
        pass

    @property
    def PointB(self):
        pass

    @property
    def PointB2(self):
        pass

    @property
    def SurfaceOverlapParameter(self):
        pass

    @property
    def SurfacePointParameter(self):
        pass


class IntersectionArcArc(Intersection):
    pass


class IntersectionBrepBrep(Intersection):
    pass


class IntersectionBrepPlane(Intersection):
    pass


class IntersectionBrepSurface(Intersection):
    pass


class IntersectionCircleCircle(Intersection):
    pass


class IntersectionCurveBrep(Intersection):
    pass


class IntersectionCurveBrepFace(Intersection):
    pass


class IntersectionCurveCurve(Intersection):
    pass


class IntersectionCurveLine(Intersection):
    pass


class IntersectionCurvePlane(Intersection):
    pass


class IntersectionCurveSelf(Intersection):
    pass


class IntersectionCurveSurface(Intersection):
    pass


class IntersectionLineBox(Intersection):
    pass


class IntersectionLineCircle(Intersection):
    pass


class IntersectionLineCylinder(Intersection):
    pass


class IntersectionLineLine(Intersection):
    pass


class IntersectionLinePlane(Intersection):
    pass


class IntersectionLineSphere(Intersection):
    pass


class IntersectionMeshLine(Intersection):
    pass


class IntersectionMeshMesh(Intersection):
    pass


class IntersectionMeshPlane(Intersection):
    pass


class IntersectionMeshPolyline(Intersection):
    pass


class IntersectionPlaneCircle(Intersection):
    pass


class IntersectionPlanePlane(Intersection):
    pass


class IntersectionPlanePlanePlane(Intersection):
    pass


class IntersectionPlaneSphere(Intersection):
    pass


class IntersectionSphereSphere(Intersection):
    pass


class IntersectionSurfaceSurface(Intersection):
    pass
