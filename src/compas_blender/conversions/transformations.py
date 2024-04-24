import mathutils  # type: ignore

from compas.geometry import Transformation

# =============================================================================
# To Blender
# =============================================================================


def transformation_to_blender(transformation):
    """Convert a COMPAS transformation to a Blender transformation.

    Parameters
    ----------
    transformation : :class:`compas.geometry.Transformation`
        A COMPAS transformation.

    Returns
    -------
    :class:`mathutils.Matrix`
        A Blender transformation.

    """
    return mathutils.Matrix(transformation.matrix)


# =============================================================================
# To COMPAS
# =============================================================================


def transformation_to_compas(matrix):
    """Convert a Blender transformation to a COMPAS transformation.

    Parameters
    ----------
    matrix : :class:`mathutils.Matrix`
        A Blender transformation.

    Returns
    -------
    :class:`compas.geometry.Transformation`
        A COMPAS transformation.

    """
    return Transformation.from_matrix(matrix)
