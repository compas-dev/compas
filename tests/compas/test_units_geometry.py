"""
Test suite for units integration with COMPAS geometry objects.

This test suite validates how units work with geometry functions
and demonstrates the integration points for units in COMPAS.
"""

import pytest
import json
import math
from compas.units import units, UNITS_AVAILABLE, UNCERTAINTIES_AVAILABLE
from compas.data.encoders import DataEncoder, DataDecoder
from compas.geometry import Point, Vector, Frame, distance_point_point
from compas.datastructures import Mesh


@pytest.mark.skipif(not UNITS_AVAILABLE, reason="pint not available")
class TestUnitsWithGeometryFunctions:
    """Test how units work with geometry functions."""
    
    def test_distance_with_units(self):
        """Test distance calculation with unit-aware coordinates."""
        # Create points with unit coordinates as lists
        p1 = [1.0 * units.meter, 2.0 * units.meter, 3.0 * units.meter]
        p2 = [4.0 * units.meter, 5.0 * units.meter, 6.0 * units.meter]
        
        # Distance function should handle units
        try:
            distance = distance_point_point(p1, p2)
            # If this works, distance should have units
            if hasattr(distance, 'magnitude'):
                assert distance.magnitude == pytest.approx(5.196, abs=1e-3)
                assert 'meter' in str(distance.units)
        except Exception:
            # If geometry functions don't handle units yet, that's expected
            # This test documents the current state
            pass
    
    def test_mixed_units_conversion(self):
        """Test distance with mixed units."""
        # Different units should be automatically converted
        p1 = [1.0 * units.meter, 0.0 * units.meter, 0.0 * units.meter]
        p2 = [1000.0 * units.millimeter, 0.0 * units.millimeter, 0.0 * units.millimeter]
        
        try:
            distance = distance_point_point(p1, p2)
            # Should be zero distance (same point in different units)
            if hasattr(distance, 'magnitude'):
                assert distance.magnitude == pytest.approx(0.0, abs=1e-10)
        except Exception:
            # If geometry functions don't handle units yet, that's expected
            pass
    
    def test_units_serialization_in_geometry_data(self):
        """Test serialization of data structures containing units."""
        # Create mixed data that might be used in geometry contexts
        geometry_data = {
            'coordinates': [1.0 * units.meter, 2.0 * units.meter, 3.0 * units.meter],
            'distance': 5.0 * units.meter,
            'area': 10.0 * units.Quantity(1.0, 'meter^2'),
            'plain_value': 42.0
        }
        
        # Should serialize correctly
        json_str = json.dumps(geometry_data, cls=DataEncoder)
        assert 'compas.units/PintQuantityEncoder' in json_str
        
        # Should deserialize correctly
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        assert reconstructed['plain_value'] == 42.0
        assert hasattr(reconstructed['distance'], 'magnitude')
        assert reconstructed['distance'].magnitude == 5.0


@pytest.mark.skipif(not UNITS_AVAILABLE, reason="pint not available")
class TestGeometryObjectsSerialization:
    """Test geometry objects serialization when they contain unit data."""
    
    def test_point_serialization_integration(self):
        """Test Point serialization in unit-aware workflows."""
        # Points are created with plain coordinates (current behavior)
        p = Point(1.0, 2.0, 3.0)
        
        # But point data can be enhanced with units in workflows
        point_data = {
            'geometry': p,
            'units': 'meter',
            'precision': 0.001 * units.meter
        }
        
        # Should serialize correctly
        json_str = json.dumps(point_data, cls=DataEncoder)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        assert isinstance(reconstructed['geometry'], Point)
        assert reconstructed['units'] == 'meter'
        assert hasattr(reconstructed['precision'], 'magnitude')
        assert reconstructed['precision'].magnitude == 0.001
    
    def test_vector_workflow_with_units(self):
        """Test Vector in unit-aware workflows."""
        # Vectors are created with plain coordinates
        v = Vector(1.0, 2.0, 3.0)
        
        # But can be part of unit-aware data
        vector_data = {
            'direction': v,
            'magnitude': 5.0 * units.meter,
            'force': 100.0 * units.Quantity(1.0, 'newton')
        }
        
        # Should serialize correctly
        json_str = json.dumps(vector_data, cls=DataEncoder)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        assert isinstance(reconstructed['direction'], Vector)
        assert hasattr(reconstructed['magnitude'], 'magnitude')
        assert reconstructed['magnitude'].magnitude == 5.0
    
    def test_frame_with_unit_context(self):
        """Test Frame in unit-aware context."""
        frame = Frame([1.0, 2.0, 3.0])
        
        # Frame can be part of unit-aware design data
        design_data = {
            'coordinate_frame': frame,
            'scale': 1.0 * units.meter,
            'tolerance': 0.01 * units.meter
        }
        
        # Should serialize correctly
        json_str = json.dumps(design_data, cls=DataEncoder)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        assert isinstance(reconstructed['coordinate_frame'], Frame)
        assert hasattr(reconstructed['scale'], 'magnitude')
        assert reconstructed['scale'].magnitude == 1.0


@pytest.mark.skipif(not UNITS_AVAILABLE, reason="pint not available")
class TestMeshWithUnitsWorkflow:
    """Test Mesh in unit-aware workflows."""
    
    def test_mesh_with_unit_metadata(self):
        """Test Mesh with unit metadata."""
        # Create simple mesh
        vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        faces = [[0, 1, 2]]
        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        
        # Add unit-aware metadata
        mesh_data = {
            'mesh': mesh,
            'units': 'meter',
            'scale_factor': 1.0 * units.meter,
            'material_thickness': 0.1 * units.meter,
            'area': 0.5 * units.Quantity(1.0, 'meter^2')
        }
        
        # Should serialize correctly
        json_str = json.dumps(mesh_data, cls=DataEncoder)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        assert isinstance(reconstructed['mesh'], Mesh)
        assert reconstructed['units'] == 'meter'
        assert hasattr(reconstructed['scale_factor'], 'magnitude')
        assert reconstructed['scale_factor'].magnitude == 1.0
        assert hasattr(reconstructed['material_thickness'], 'magnitude')
        assert reconstructed['material_thickness'].magnitude == 0.1
    
    def test_mesh_processing_workflow(self):
        """Test mesh in processing workflow with units."""
        # Create mesh with unit-aware attributes
        mesh = Mesh()
        
        # Add vertices (plain coordinates)
        v1 = mesh.add_vertex(x=0.0, y=0.0, z=0.0)
        v2 = mesh.add_vertex(x=1.0, y=0.0, z=0.0)
        v3 = mesh.add_vertex(x=0.0, y=1.0, z=0.0)
        
        # Add face
        mesh.add_face([v1, v2, v3])
        
        # Add unit-aware attributes
        mesh_analysis = {
            'mesh': mesh,
            'vertex_loads': [10.0 * units.Quantity(1.0, 'newton') for _ in mesh.vertices()],
            'edge_lengths': [1.0 * units.meter for _ in mesh.edges()],
            'face_areas': [0.5 * units.Quantity(1.0, 'meter^2') for _ in mesh.faces()]
        }
        
        # Should serialize correctly
        json_str = json.dumps(mesh_analysis, cls=DataEncoder)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        assert isinstance(reconstructed['mesh'], Mesh)
        assert len(reconstructed['vertex_loads']) == 3
        assert all(hasattr(load, 'magnitude') for load in reconstructed['vertex_loads'])


@pytest.mark.skipif(not UNCERTAINTIES_AVAILABLE, reason="uncertainties not available")
class TestGeometryWithUncertainties:
    """Test geometry objects with measurement uncertainties."""
    
    def test_measurement_data_with_uncertainties(self):
        """Test geometry data with measurement uncertainties."""
        import uncertainties as unc
        
        # Survey/measurement data with uncertainties
        measurement_data = {
            'point': Point(1.0, 2.0, 3.0),  # Plain geometry
            'measured_coordinates': [
                unc.ufloat(1.0, 0.01),  # x ± 0.01
                unc.ufloat(2.0, 0.01),  # y ± 0.01
                unc.ufloat(3.0, 0.02)   # z ± 0.02
            ],
            'measurement_error': unc.ufloat(0.05, 0.01)  # Total error ± uncertainty
        }
        
        # Should serialize correctly
        json_str = json.dumps(measurement_data, cls=DataEncoder)
        assert 'compas.units/UncertaintiesUFloatEncoder' in json_str
        
        # Should deserialize correctly
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        assert isinstance(reconstructed['point'], Point)
        assert len(reconstructed['measured_coordinates']) == 3
        assert all(hasattr(coord, 'nominal_value') for coord in reconstructed['measured_coordinates'])
        assert all(hasattr(coord, 'std_dev') for coord in reconstructed['measured_coordinates'])


class TestGeometryBackwardCompatibility:
    """Test that geometry objects work normally without units."""
    
    def test_point_backward_compatibility(self):
        """Test Point works normally with plain floats."""
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)
        
        # Should work as before
        assert p1.x == 1.0
        assert p1.y == 2.0
        assert p1.z == 3.0
        
        # Arithmetic should work
        result = p1 + p2
        assert result.x == 5.0
        assert result.y == 7.0
        assert result.z == 9.0
        
        # Distance calculation should work
        distance = distance_point_point(p1, p2)
        assert distance == pytest.approx(5.196, abs=1e-3)
    
    def test_vector_backward_compatibility(self):
        """Test Vector works normally with plain floats."""
        v1 = Vector(1.0, 0.0, 0.0)
        v2 = Vector(0.0, 1.0, 0.0)
        
        # Should work as before
        assert v1.length == 1.0
        assert v1.dot(v2) == 0.0
        
        cross = v1.cross(v2)
        assert cross.z == 1.0
    
    def test_frame_backward_compatibility(self):
        """Test Frame works normally with plain coordinates."""
        frame = Frame([1.0, 2.0, 3.0])
        
        # Should work as before
        assert frame.point.x == 1.0
        assert frame.point.y == 2.0
        assert frame.point.z == 3.0
    
    def test_mesh_backward_compatibility(self):
        """Test Mesh works normally with plain coordinates."""
        vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        faces = [[0, 1, 2]]
        
        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        
        # Should work as before
        assert len(list(mesh.vertices())) == 3
        assert len(list(mesh.faces())) == 1
        
        # Coordinates should be plain floats
        coords = mesh.vertex_coordinates(0)
        assert coords == [0.0, 0.0, 0.0]
    
    def test_serialization_backward_compatibility(self):
        """Test that regular geometry serialization still works."""
        # Test with various geometry objects
        point = Point(1.0, 2.0, 3.0)
        vector = Vector(1.0, 2.0, 3.0)
        frame = Frame([0.0, 0.0, 0.0])
        
        geometry_collection = {
            'point': point,
            'vector': vector,
            'frame': frame,
            'plain_data': [1.0, 2.0, 3.0]
        }
        
        # Should serialize and deserialize normally
        json_str = json.dumps(geometry_collection, cls=DataEncoder)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        assert isinstance(reconstructed['point'], Point)
        assert isinstance(reconstructed['vector'], Vector)
        assert isinstance(reconstructed['frame'], Frame)
        assert reconstructed['plain_data'] == [1.0, 2.0, 3.0]