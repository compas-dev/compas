from ._curve import Curve  # noqa: F401
from .bezier import BezierCurve  # noqa: F401

try:
    import compas_occ  # noqa F401
except (ImportError, ModuleNotFoundError):
    from .nurbs import NurbsCurve
else:
    from compas_occ.geometry import NurbsCurve  # noqa F401
