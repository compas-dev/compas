import bpy  # type: ignore

from compas.geometry import NurbsSurface

# =============================================================================
# To Blender
# =============================================================================


def nurbssurface_to_blender_surface(nurbssurface: NurbsSurface, u=32, v=32) -> bpy.types.Curve:
    """Convert a COMPAS NURBS surface to a Blender surface.

    Parameters
    ----------
    nurbssurface : :class:`compas.geometry.NurbsSurface`
        A COMPAS NURBS surface.

    Returns
    -------
    :class:`bpy.types.Curve`
        A Blender surface.

    """
    surf = bpy.data.curves.new(name=nurbssurface.name, type="SURFACE")
    surf.dimensions = "3D"
    surf.resolution_u = u
    surf.resolution_v = v

    # add the U(V) splines
    for points, weights in zip(nurbssurface.points, nurbssurface.weights):
        spline = surf.splines.new("NURBS")
        spline.points.add(len(points) - 1)

        for i, (point, weight) in enumerate(zip(points, weights)):
            spline.points[i].co = [point[0], point[1], point[2], weight]
            spline.points[i].weight = weight

        spline.use_endpoint_u = True
        spline.use_endpoint_v = True
        spline.order_u = nurbssurface.degree_u + 1
        spline.order_v = nurbssurface.degree_v + 1

    return surf


# =============================================================================
# To COMPAS
# =============================================================================
