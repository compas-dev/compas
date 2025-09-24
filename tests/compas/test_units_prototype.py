"""
Test suite for units and uncertainties support in COMPAS.

This test suite validates the prototype implementation and ensures
backward compatibility is maintained.
"""

import pytest
import math
from compas.units import units, UNITS_AVAILABLE, UNCERTAINTIES_AVAILABLE


class TestUnitsModule:
    """Test the units module functionality."""
    
    def test_units_availability(self):
        """Test that units are detected correctly."""
        # This test will pass regardless of whether pint is installed
        assert isinstance(UNITS_AVAILABLE, bool)
        assert isinstance(UNCERTAINTIES_AVAILABLE, bool)
    
    def test_quantity_creation(self):
        """Test quantity creation with graceful degradation."""
        # Should work regardless of pint availability
        result = units.Quantity(1.0, 'meter')
        
        if UNITS_AVAILABLE:
            assert hasattr(result, 'magnitude')
            assert result.magnitude == 1.0
        else:
            assert result == 1.0
    
    @pytest.mark.skipif(not UNITS_AVAILABLE, reason="pint not available")
    def test_unit_conversions(self):
        """Test basic unit conversions work correctly."""
        meter = units.Quantity(1.0, 'meter')
        millimeter = units.Quantity(1000.0, 'millimeter')
        
        # They should be equivalent
        assert meter.to('millimeter').magnitude == pytest.approx(1000.0)
        assert millimeter.to('meter').magnitude == pytest.approx(1.0)
    
    @pytest.mark.skipif(not UNCERTAINTIES_AVAILABLE, reason="uncertainties not available") 
    def test_uncertainty_creation(self):
        """Test uncertainty creation."""
        import uncertainties
        
        val = uncertainties.ufloat(1.0, 0.1)
        assert val.nominal_value == 1.0
        assert val.std_dev == 0.1


class TestUnitAwarePoint:
    """Test the unit-aware Point implementation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Import the prototype
        import sys
        import os
        sys.path.insert(0, '/tmp/units_analysis')
        from point_prototype import UnitAwarePoint
        self.Point = UnitAwarePoint
    
    def test_traditional_usage(self):
        """Test that traditional Point usage is unchanged."""
        p1 = self.Point(1.0, 2.0, 3.0)
        p2 = self.Point(4.0, 5.0, 6.0)
        
        # Coordinates should be plain floats
        assert isinstance(p1.x, float)
        assert isinstance(p1.y, float) 
        assert isinstance(p1.z, float)
        
        # Values should be correct
        assert p1.x == 1.0
        assert p1.y == 2.0
        assert p1.z == 3.0
        
        # Distance calculation should work
        distance = p1.distance_to(p2)
        assert isinstance(distance, float)
        assert distance == pytest.approx(5.196, abs=1e-3)
    
    def test_point_arithmetic(self):
        """Test point arithmetic operations."""
        p1 = self.Point(1.0, 2.0, 3.0)
        
        # Addition
        p2 = p1 + [1.0, 1.0, 1.0]
        assert p2.x == 2.0
        assert p2.y == 3.0
        assert p2.z == 4.0
        
        # Subtraction
        p3 = p2 - [1.0, 1.0, 1.0]
        assert p3.x == 1.0
        assert p3.y == 2.0
        assert p3.z == 3.0
        
        # Scalar multiplication
        p4 = p1 * 2.0
        assert p4.x == 2.0
        assert p4.y == 4.0
        assert p4.z == 6.0
    
    def test_point_indexing(self):
        """Test point indexing behavior."""
        p = self.Point(1.0, 2.0, 3.0)
        
        # Index access
        assert p[0] == 1.0
        assert p[1] == 2.0
        assert p[2] == 3.0
        
        # Iteration
        coords = list(p)
        assert coords == [1.0, 2.0, 3.0]
    
    def test_data_serialization(self):
        """Test data serialization compatibility."""
        p1 = self.Point(1.0, 2.0, 3.0)
        
        # Should be serializable
        data = p1.__data__
        assert data == [1.0, 2.0, 3.0]
        
        # Should be reconstructible
        p2 = self.Point.__from_data__(data)
        assert p2.x == p1.x
        assert p2.y == p1.y
        assert p2.z == p1.z
    
    @pytest.mark.skipif(not UNITS_AVAILABLE, reason="pint not available")
    def test_unit_aware_usage(self):
        """Test unit-aware Point functionality."""
        p1 = self.Point(1.0 * units.meter, 2.0 * units.meter, 3.0 * units.meter)
        
        # Coordinates should be pint quantities
        assert hasattr(p1.x, 'magnitude')
        assert hasattr(p1.x, 'units')
        assert p1.x.magnitude == 1.0
        
        # Mixed units should work
        p2 = self.Point(1000 * units.millimeter, 2000 * units.millimeter, 3000 * units.millimeter)
        
        # Distance should be calculated correctly with units
        distance = p1.distance_to(p2)
        assert hasattr(distance, 'magnitude')
        assert distance.magnitude == pytest.approx(0.0, abs=1e-10)
    
    @pytest.mark.skipif(not UNITS_AVAILABLE, reason="pint not available")
    def test_unit_arithmetic(self):
        """Test arithmetic with units."""
        p1 = self.Point(1.0 * units.meter, 2.0 * units.meter, 3.0 * units.meter)
        
        # Addition with compatible units should work
        p2 = p1 + [1.0 * units.meter, 1.0 * units.meter, 1.0 * units.meter]
        assert hasattr(p2.x, 'magnitude')
        assert p2.x.magnitude == 2.0
        
        # Scalar multiplication should preserve units
        p3 = p1 * 2.0
        assert hasattr(p3.x, 'magnitude')
        assert p3.x.magnitude == 2.0
    
    @pytest.mark.skipif(not UNCERTAINTIES_AVAILABLE, reason="uncertainties not available")
    def test_uncertainty_usage(self):
        """Test Point with uncertainties."""
        import uncertainties
        
        p1 = self.Point(
            uncertainties.ufloat(1.0, 0.1),
            uncertainties.ufloat(2.0, 0.1),
            uncertainties.ufloat(3.0, 0.1)
        )
        
        # Coordinates should have uncertainties
        assert hasattr(p1.x, 'nominal_value')
        assert hasattr(p1.x, 'std_dev')
        assert p1.x.nominal_value == 1.0
        assert p1.x.std_dev == 0.1
        
        # Distance calculation should propagate uncertainties
        p2 = self.Point(4.0, 5.0, 6.0)
        distance = p1.distance_to(p2)
        
        assert hasattr(distance, 'nominal_value')
        assert hasattr(distance, 'std_dev')
        assert distance.nominal_value == pytest.approx(5.196, abs=1e-3)
        assert distance.std_dev > 0  # Should have some uncertainty


class TestEnhancedSerialization:
    """Test enhanced JSON serialization."""
    
    def setup_method(self):
        """Set up test fixtures."""
        import sys
        sys.path.insert(0, '/tmp/units_analysis')
        from enhanced_encoders import EnhancedDataEncoder, EnhancedDataDecoder
        from point_prototype import UnitAwarePoint
        
        self.encoder = EnhancedDataEncoder
        self.decoder = EnhancedDataDecoder
        self.Point = UnitAwarePoint
    
    def test_plain_serialization(self):
        """Test that plain objects serialize correctly."""
        import json
        
        p = self.Point(1.0, 2.0, 3.0)
        
        # Should serialize without errors
        json_str = json.dumps(p, cls=self.encoder)
        assert isinstance(json_str, str)
        assert len(json_str) > 0
        
        # Should deserialize correctly
        p_reconstructed = json.loads(json_str, cls=self.decoder)
        assert p_reconstructed.x == p.x
        assert p_reconstructed.y == p.y
        assert p_reconstructed.z == p.z
    
    @pytest.mark.skipif(not UNITS_AVAILABLE, reason="pint not available")
    def test_unit_serialization(self):
        """Test serialization of unit-aware objects."""
        import json
        
        p = self.Point(1.0 * units.meter, 2.0 * units.meter, 3.0 * units.meter)
        
        # Should serialize without errors
        json_str = json.dumps(p, cls=self.encoder)
        assert isinstance(json_str, str)
        assert '__pint_quantity__' in json_str
        
        # Should deserialize correctly
        p_reconstructed = json.loads(json_str, cls=self.decoder)
        assert hasattr(p_reconstructed.x, 'magnitude')
        assert p_reconstructed.x.magnitude == p.x.magnitude
    
    @pytest.mark.skipif(not UNCERTAINTIES_AVAILABLE, reason="uncertainties not available")
    def test_uncertainty_serialization(self):
        """Test serialization of uncertainty objects."""
        import json
        import uncertainties
        
        p = self.Point(
            uncertainties.ufloat(1.0, 0.1),
            uncertainties.ufloat(2.0, 0.1),
            uncertainties.ufloat(3.0, 0.1)
        )
        
        # Should serialize without errors
        json_str = json.dumps(p, cls=self.encoder)
        assert isinstance(json_str, str)
        assert '__uncertainties_ufloat__' in json_str
        
        # Should deserialize correctly
        p_reconstructed = json.loads(json_str, cls=self.decoder)
        assert hasattr(p_reconstructed.x, 'nominal_value')
        assert p_reconstructed.x.nominal_value == p.x.nominal_value
        assert p_reconstructed.x.std_dev == p.x.std_dev


# Run basic tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])