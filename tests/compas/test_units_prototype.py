"""
Test suite for units and uncertainties support in COMPAS.

This test suite validates the units functionality and ensures
backward compatibility is maintained.
"""

import pytest
import json
from compas.units import units, UNITS_AVAILABLE, UNCERTAINTIES_AVAILABLE
from compas.data.encoders import DataEncoder, DataDecoder


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


class TestUnitsIntegration:
    """Test units integration with COMPAS components."""
    
    @pytest.mark.skipif(not UNITS_AVAILABLE, reason="pint not available")
    def test_serialization_with_units(self):
        """Test JSON serialization of units."""
        # Create a quantity
        length = units.Quantity(5.0, 'meter')
        
        # Serialize
        json_str = json.dumps(length, cls=DataEncoder)
        assert 'compas.units/PintQuantityEncoder' in json_str
        
        # Deserialize
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        # Should be equivalent
        assert hasattr(reconstructed, 'magnitude')
        assert reconstructed.magnitude == 5.0
        assert str(reconstructed.units) == 'meter'
    
    @pytest.mark.skipif(not UNCERTAINTIES_AVAILABLE, reason="uncertainties not available")
    def test_serialization_with_uncertainties(self):
        """Test JSON serialization of uncertainties."""
        import uncertainties
        
        # Create an uncertain value
        value = uncertainties.ufloat(3.14, 0.01)
        
        # Serialize
        json_str = json.dumps(value, cls=DataEncoder)
        assert 'compas.units/UncertaintiesUFloatEncoder' in json_str
        
        # Deserialize
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        # Should be equivalent
        assert hasattr(reconstructed, 'nominal_value')
        assert reconstructed.nominal_value == 3.14
        assert reconstructed.std_dev == 0.01
    
    def test_serialization_graceful_degradation_units(self):
        """Test that serialization works even without units available."""
        # Create a mock COMPAS-style object that looks like our encoder output
        mock_quantity = {
            'dtype': 'compas.units/PintQuantityEncoder', 
            'data': {'magnitude': 2.5, 'units': 'meter'}
        }
        
        # Serialize and deserialize
        json_str = json.dumps(mock_quantity)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        if UNITS_AVAILABLE:
            # Should reconstruct as a pint quantity
            assert hasattr(reconstructed, 'magnitude')
            assert reconstructed.magnitude == 2.5
        else:
            # Should fallback to magnitude only
            assert reconstructed == 2.5
    
    def test_serialization_graceful_degradation_uncertainties(self):
        """Test that serialization works even without uncertainties available."""
        # Create a mock COMPAS-style object that looks like our encoder output
        mock_ufloat = {
            'dtype': 'compas.units/UncertaintiesUFloatEncoder',
            'data': {'nominal_value': 1.23, 'std_dev': 0.05}
        }
        
        # Serialize and deserialize
        json_str = json.dumps(mock_ufloat)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        if UNCERTAINTIES_AVAILABLE:
            # Should reconstruct as an uncertainties value
            assert hasattr(reconstructed, 'nominal_value')
            assert reconstructed.nominal_value == 1.23
        else:
            # Should fallback to nominal value only
            assert reconstructed == 1.23
    
    def test_backward_compatibility(self):
        """Test that existing serialization still works."""
        # Test with a simple dictionary
        test_data = {'x': 1.0, 'y': 2.0, 'z': 3.0}
        
        # Should serialize and deserialize normally
        json_str = json.dumps(test_data, cls=DataEncoder)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        assert reconstructed == test_data
    
    @pytest.mark.skipif(not UNITS_AVAILABLE, reason="pint not available")
    def test_mixed_data_with_units(self):
        """Test serialization of mixed data containing units."""
        # Create mixed data
        mixed_data = {
            'plain_value': 42.0,
            'length': units.Quantity(10.0, 'meter'),
            'width': units.Quantity(5.0, 'meter'),
            'nested': {
                'height': units.Quantity(3.0, 'meter')
            }
        }
        
        # Serialize
        json_str = json.dumps(mixed_data, cls=DataEncoder)
        assert 'compas.units/PintQuantityEncoder' in json_str
        
        # Deserialize
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        # Check all values
        assert reconstructed['plain_value'] == 42.0
        assert hasattr(reconstructed['length'], 'magnitude')
        assert reconstructed['length'].magnitude == 10.0
        assert hasattr(reconstructed['width'], 'magnitude')
        assert reconstructed['width'].magnitude == 5.0
        assert hasattr(reconstructed['nested']['height'], 'magnitude')
        assert reconstructed['nested']['height'].magnitude == 3.0


# Run basic tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])