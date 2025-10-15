"""Unit tests for Shape transformation methods.

This test module validates that transform() and transformed() methods correctly
apply scale components of transformations to Shape subclasses.
"""

import pytest
from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import Transformation
from compas.geometry import Translation


# =============================================================================
# Box Tests
# =============================================================================


def test_box_transform_with_uniform_scale():
    """Test that Box.transform() applies uniform scaling correctly."""
    box = Box(1.0, 2.0, 3.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    box.transform(S)
    
    assert box.xsize == pytest.approx(2.0)
    assert box.ysize == pytest.approx(4.0)
    assert box.zsize == pytest.approx(6.0)


def test_box_transform_with_non_uniform_scale():
    """Test that Box.transform() applies non-uniform scaling correctly."""
    box = Box(1.0, 2.0, 3.0)
    S = Scale.from_factors([2.0, 3.0, 4.0])
    box.transform(S)
    
    assert box.xsize == pytest.approx(2.0)
    assert box.ysize == pytest.approx(6.0)
    assert box.zsize == pytest.approx(12.0)


def test_box_transform_with_translation_and_scale():
    """Test that Box.transform() applies combined translation and scaling."""
    box = Box(1.0, 2.0, 3.0)
    T = Translation.from_vector([5, 5, 5])
    S = Scale.from_factors([2.0, 3.0, 4.0])
    combined = T * S
    
    original_center = box.frame.point
    box.transform(combined)
    
    # Check dimensions are scaled
    assert box.xsize == pytest.approx(2.0)
    assert box.ysize == pytest.approx(6.0)
    assert box.zsize == pytest.approx(12.0)
    
    # Check position is translated
    expected_center = Point(5, 5, 5)
    assert box.frame.point.x == pytest.approx(expected_center.x)
    assert box.frame.point.y == pytest.approx(expected_center.y)
    assert box.frame.point.z == pytest.approx(expected_center.z)


def test_box_transformed_with_scale():
    """Test that Box.transformed() returns a scaled copy."""
    box = Box(1.0, 2.0, 3.0)
    S = Scale.from_factors([2.0, 3.0, 4.0])
    
    transformed_box = box.transformed(S)
    
    # Original box should be unchanged
    assert box.xsize == pytest.approx(1.0)
    assert box.ysize == pytest.approx(2.0)
    assert box.zsize == pytest.approx(3.0)
    
    # Transformed box should be scaled
    assert transformed_box.xsize == pytest.approx(2.0)
    assert transformed_box.ysize == pytest.approx(6.0)
    assert transformed_box.zsize == pytest.approx(12.0)


def test_box_transform_preserves_frame_orientation():
    """Test that Box.transform() preserves frame orientation when scaling."""
    box = Box(1.0, 2.0, 3.0, frame=Frame([1, 1, 1], [1, 0, 0], [0, 1, 0]))
    original_xaxis = box.frame.xaxis.copy()
    original_yaxis = box.frame.yaxis.copy()
    original_zaxis = box.frame.zaxis.copy()
    
    S = Scale.from_factors([2.0, 2.0, 2.0])
    box.transform(S)
    
    # Frame axes should remain the same (only position and dimensions change)
    assert box.frame.xaxis.x == pytest.approx(original_xaxis.x)
    assert box.frame.xaxis.y == pytest.approx(original_xaxis.y)
    assert box.frame.xaxis.z == pytest.approx(original_xaxis.z)


# =============================================================================
# Sphere Tests
# =============================================================================


def test_sphere_transform_with_uniform_scale():
    """Test that Sphere.transform() applies uniform scaling correctly."""
    sphere = Sphere(5.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    sphere.transform(S)
    
    assert sphere.radius == pytest.approx(10.0)


def test_sphere_transform_with_non_uniform_scale():
    """Test that Sphere.transform() with non-uniform scale uses average scaling.
    
    For a sphere, non-uniform scaling should use the average of the scale factors
    to maintain the spherical shape.
    """
    sphere = Sphere(3.0)
    S = Scale.from_factors([2.0, 3.0, 4.0])
    sphere.transform(S)
    
    # For sphere, we expect average scaling factor: (2.0 + 3.0 + 4.0) / 3.0 = 3.0
    assert sphere.radius == pytest.approx(9.0)


def test_sphere_transformed_with_scale():
    """Test that Sphere.transformed() returns a scaled copy."""
    sphere = Sphere(5.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    
    transformed_sphere = sphere.transformed(S)
    
    # Original sphere should be unchanged
    assert sphere.radius == pytest.approx(5.0)
    
    # Transformed sphere should be scaled
    assert transformed_sphere.radius == pytest.approx(10.0)


def test_sphere_transform_with_translation_and_scale():
    """Test that Sphere.transform() applies combined translation and scaling."""
    sphere = Sphere(3.0, frame=Frame.worldXY())
    T = Translation.from_vector([10, 10, 10])
    S = Scale.from_factors([2.0, 2.0, 2.0])
    combined = T * S
    
    sphere.transform(combined)
    
    # Check radius is scaled
    assert sphere.radius == pytest.approx(6.0)
    
    # Check position is translated
    assert sphere.frame.point.x == pytest.approx(10.0)
    assert sphere.frame.point.y == pytest.approx(10.0)
    assert sphere.frame.point.z == pytest.approx(10.0)


# =============================================================================
# Cylinder Tests
# =============================================================================


def test_cylinder_transform_with_uniform_scale():
    """Test that Cylinder.transform() applies uniform scaling correctly."""
    cylinder = Cylinder(radius=2.0, height=5.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    cylinder.transform(S)
    
    assert cylinder.radius == pytest.approx(4.0)
    assert cylinder.height == pytest.approx(10.0)


def test_cylinder_transform_with_non_uniform_scale():
    """Test that Cylinder.transform() applies non-uniform scaling correctly.
    
    For a cylinder aligned with Z-axis:
    - X and Y scaling affect the radius (we use the average of X and Y)
    - Z scaling affects the height
    """
    cylinder = Cylinder(radius=2.0, height=5.0)
    S = Scale.from_factors([2.0, 3.0, 4.0])
    cylinder.transform(S)
    
    # Radius should be scaled by average of X and Y factors: (2.0 + 3.0) / 2.0 = 2.5
    assert cylinder.radius == pytest.approx(5.0)
    # Height should be scaled by Z factor: 5.0 * 4.0 = 20.0
    assert cylinder.height == pytest.approx(20.0)


def test_cylinder_transformed_with_scale():
    """Test that Cylinder.transformed() returns a scaled copy."""
    cylinder = Cylinder(radius=2.0, height=5.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    
    transformed_cylinder = cylinder.transformed(S)
    
    # Original cylinder should be unchanged
    assert cylinder.radius == pytest.approx(2.0)
    assert cylinder.height == pytest.approx(5.0)
    
    # Transformed cylinder should be scaled
    assert transformed_cylinder.radius == pytest.approx(4.0)
    assert transformed_cylinder.height == pytest.approx(10.0)


def test_cylinder_transform_with_translation_and_scale():
    """Test that Cylinder.transform() applies combined translation and scaling."""
    cylinder = Cylinder(radius=2.0, height=5.0)
    T = Translation.from_vector([3, 4, 5])
    S = Scale.from_factors([2.0, 2.0, 3.0])
    combined = T * S
    
    cylinder.transform(combined)
    
    # Check dimensions are scaled
    assert cylinder.radius == pytest.approx(4.0)
    assert cylinder.height == pytest.approx(15.0)
    
    # Check position is translated
    assert cylinder.frame.point.x == pytest.approx(3.0)
    assert cylinder.frame.point.y == pytest.approx(4.0)
    assert cylinder.frame.point.z == pytest.approx(5.0)


# =============================================================================
# Cone Tests
# =============================================================================


def test_cone_transform_with_uniform_scale():
    """Test that Cone.transform() applies uniform scaling correctly."""
    cone = Cone(radius=3.0, height=6.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    cone.transform(S)
    
    assert cone.radius == pytest.approx(6.0)
    assert cone.height == pytest.approx(12.0)


def test_cone_transform_with_non_uniform_scale():
    """Test that Cone.transform() applies non-uniform scaling correctly.
    
    For a cone aligned with Z-axis:
    - X and Y scaling affect the radius (we use the average of X and Y)
    - Z scaling affects the height
    """
    cone = Cone(radius=3.0, height=6.0)
    S = Scale.from_factors([2.0, 4.0, 3.0])
    cone.transform(S)
    
    # Radius should be scaled by average of X and Y factors: (2.0 + 4.0) / 2.0 = 3.0
    assert cone.radius == pytest.approx(9.0)
    # Height should be scaled by Z factor: 6.0 * 3.0 = 18.0
    assert cone.height == pytest.approx(18.0)


def test_cone_transformed_with_scale():
    """Test that Cone.transformed() returns a scaled copy."""
    cone = Cone(radius=3.0, height=6.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    
    transformed_cone = cone.transformed(S)
    
    # Original cone should be unchanged
    assert cone.radius == pytest.approx(3.0)
    assert cone.height == pytest.approx(6.0)
    
    # Transformed cone should be scaled
    assert transformed_cone.radius == pytest.approx(6.0)
    assert transformed_cone.height == pytest.approx(12.0)


# =============================================================================
# Capsule Tests
# =============================================================================


def test_capsule_transform_with_uniform_scale():
    """Test that Capsule.transform() applies uniform scaling correctly."""
    capsule = Capsule(radius=2.0, height=4.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    capsule.transform(S)
    
    assert capsule.radius == pytest.approx(4.0)
    assert capsule.height == pytest.approx(8.0)


def test_capsule_transform_with_non_uniform_scale():
    """Test that Capsule.transform() applies non-uniform scaling correctly.
    
    For a capsule aligned with Z-axis:
    - X and Y scaling affect the radius (we use the average of X and Y)
    - Z scaling affects the height
    """
    capsule = Capsule(radius=2.0, height=4.0)
    S = Scale.from_factors([2.0, 3.0, 4.0])
    capsule.transform(S)
    
    # Radius should be scaled by average of X and Y factors: (2.0 + 3.0) / 2.0 = 2.5
    assert capsule.radius == pytest.approx(5.0)
    # Height should be scaled by Z factor: 4.0 * 4.0 = 16.0
    assert capsule.height == pytest.approx(16.0)


def test_capsule_transformed_with_scale():
    """Test that Capsule.transformed() returns a scaled copy."""
    capsule = Capsule(radius=2.0, height=4.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    
    transformed_capsule = capsule.transformed(S)
    
    # Original capsule should be unchanged
    assert capsule.radius == pytest.approx(2.0)
    assert capsule.height == pytest.approx(4.0)
    
    # Transformed capsule should be scaled
    assert transformed_capsule.radius == pytest.approx(4.0)
    assert transformed_capsule.height == pytest.approx(8.0)


# =============================================================================
# Torus Tests
# =============================================================================


def test_torus_transform_with_uniform_scale():
    """Test that Torus.transform() applies uniform scaling correctly."""
    torus = Torus(radius_axis=5.0, radius_pipe=2.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    torus.transform(S)
    
    assert torus.radius_axis == pytest.approx(10.0)
    assert torus.radius_pipe == pytest.approx(4.0)


def test_torus_transform_with_non_uniform_scale():
    """Test that Torus.transform() applies non-uniform scaling correctly.
    
    For a torus in the XY plane:
    - X and Y scaling affect the axis radius (we use the average of X and Y)
    - Z scaling affects the pipe radius
    """
    torus = Torus(radius_axis=5.0, radius_pipe=2.0)
    S = Scale.from_factors([2.0, 3.0, 4.0])
    torus.transform(S)
    
    # Axis radius should be scaled by average of X and Y factors: (2.0 + 3.0) / 2.0 = 2.5
    assert torus.radius_axis == pytest.approx(12.5)
    # Pipe radius should be scaled by Z factor
    assert torus.radius_pipe == pytest.approx(8.0)


def test_torus_transformed_with_scale():
    """Test that Torus.transformed() returns a scaled copy."""
    torus = Torus(radius_axis=5.0, radius_pipe=2.0)
    S = Scale.from_factors([2.0, 2.0, 2.0])
    
    transformed_torus = torus.transformed(S)
    
    # Original torus should be unchanged
    assert torus.radius_axis == pytest.approx(5.0)
    assert torus.radius_pipe == pytest.approx(2.0)
    
    # Transformed torus should be scaled
    assert transformed_torus.radius_axis == pytest.approx(10.0)
    assert transformed_torus.radius_pipe == pytest.approx(4.0)


# =============================================================================
# Volume Verification Tests
# =============================================================================


def test_box_volume_after_transform():
    """Test that Box volume is correctly updated after transformation with scale."""
    box = Box(2.0, 3.0, 4.0)
    original_volume = box.volume
    
    S = Scale.from_factors([2.0, 2.0, 2.0])
    box.transform(S)
    
    # Volume should scale by factor^3 = 8
    expected_volume = original_volume * 8
    assert box.volume == pytest.approx(expected_volume)


def test_sphere_volume_after_transform():
    """Test that Sphere volume is correctly updated after transformation with scale."""
    sphere = Sphere(3.0)
    original_volume = sphere.volume
    
    S = Scale.from_factors([2.0, 2.0, 2.0])
    sphere.transform(S)
    
    # Volume should scale by factor^3 = 8
    expected_volume = original_volume * 8
    assert sphere.volume == pytest.approx(expected_volume)


def test_cylinder_volume_after_transform():
    """Test that Cylinder volume is correctly updated after transformation with scale."""
    cylinder = Cylinder(radius=2.0, height=5.0)
    original_volume = cylinder.volume
    
    S = Scale.from_factors([2.0, 2.0, 2.0])
    cylinder.transform(S)
    
    # Volume should scale by factor^3 = 8
    expected_volume = original_volume * 8
    assert cylinder.volume == pytest.approx(expected_volume)
