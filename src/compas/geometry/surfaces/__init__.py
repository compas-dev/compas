from ._surface import Surface  # noqa F401

try:
    import compas_occ  # noqa F401
except ImportError:
    from .nurbs import NurbsSurface
else:
    from compas_occ.geometry import NurbsSurface  # noqa F401
