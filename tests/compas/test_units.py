"""
Test suite for units and uncertainties support in COMPAS.

This test suite validates the units functionality and ensures
backward compatibility is maintained.
"""

import pytest
import json
import compas
from compas.units import units, UNITS_AVAILABLE, UNCERTAINTIES_AVAILABLE
from compas.data.encoders import DataEncoder, DataDecoder


class TestUnitsModule:
    """Test the units module functionality."""
    
    def test_units_availability(self):
        """Test that units are detected correctly."""
        assert isinstance(UNITS_AVAILABLE, bool)
        assert isinstance(UNCERTAINTIES_AVAILABLE, bool)
    
    def test_quantity_creation(self):
        """Test quantity creation."""
        result = units.Quantity(1.0, 'meter')
        # Should work regardless of pint availability
        assert result is not None
    
    def test_unit_registry_properties(self):
        """Test unit registry properties."""
        # These should not raise errors regardless of availability
        meter = units.meter
        mm = units.millimeter
        cm = units.centimeter
        
        # Properties should be consistent
        assert (meter is None) == (not UNITS_AVAILABLE)
        assert (mm is None) == (not UNITS_AVAILABLE)
        assert (cm is None) == (not UNITS_AVAILABLE)


class TestUnitsWithPint:
    """Test units functionality when pint is available."""
    
    def test_unit_conversions(self):
        """Test basic unit conversions work correctly."""
        if compas.IPY or not UNITS_AVAILABLE:
            return  # Skip on IronPython or when pint not available
            
        meter = units.Quantity(1.0, 'meter')
        millimeter = units.Quantity(1000.0, 'millimeter')
        
        # They should be equivalent
        assert meter.to('millimeter').magnitude == pytest.approx(1000.0)
        assert millimeter.to('meter').magnitude == pytest.approx(1.0)
    
    def test_serialization_with_units(self):
        """Test JSON serialization of units."""
        if compas.IPY or not UNITS_AVAILABLE:
            return  # Skip on IronPython or when pint not available
            
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
    
    def test_mixed_data_with_units(self):
        """Test serialization of mixed data containing units."""
        if compas.IPY or not UNITS_AVAILABLE:
            return  # Skip on IronPython or when pint not available
            
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


class TestUncertaintiesWithUncertainties:
    """Test uncertainties functionality when uncertainties is available."""
    
    def test_uncertainty_creation(self):
        """Test uncertainty creation."""
        if compas.IPY or not UNCERTAINTIES_AVAILABLE:
            return  # Skip on IronPython or when uncertainties not available
            
        import uncertainties
        
        val = uncertainties.ufloat(1.0, 0.1)
        assert val.nominal_value == 1.0
        assert val.std_dev == 0.1
    
    def test_serialization_with_uncertainties(self):
        """Test JSON serialization of uncertainties."""
        if compas.IPY or not UNCERTAINTIES_AVAILABLE:
            return  # Skip on IronPython or when uncertainties not available
            
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


class TestBackwardCompatibility:
    """Test that existing functionality still works."""
    
    def test_regular_data_serialization(self):
        """Test that plain objects serialize correctly."""
        test_data = {'x': 1.0, 'y': 2.0, 'z': 3.0}
        
        # Should serialize and deserialize normally
        json_str = json.dumps(test_data, cls=DataEncoder)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        assert reconstructed == test_data


class TestGracefulDegradation:
    """Test graceful degradation when dependencies are not available."""
    
    def test_units_disabled(self, monkeypatch):
        """Test behavior when units are artificially disabled."""
        # Monkey patch to simulate missing pint
        monkeypatch.setattr('compas.units.UNITS_AVAILABLE', False)
        monkeypatch.setattr('compas.units.pint', None)
        
        # Create mock COMPAS-style object that looks like our encoder output
        mock_quantity = {
            'dtype': 'compas.units/PintQuantityEncoder', 
            'data': {'magnitude': 2.5, 'units': 'meter'}
        }
        
        # Serialize and deserialize
        json_str = json.dumps(mock_quantity)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        # Should fallback to magnitude only
        assert reconstructed == 2.5
    
    def test_uncertainties_disabled(self, monkeypatch):
        """Test behavior when uncertainties are artificially disabled."""
        # Monkey patch to simulate missing uncertainties
        monkeypatch.setattr('compas.units.UNCERTAINTIES_AVAILABLE', False)
        monkeypatch.setattr('compas.units.uncertainties', None)
        
        # Create mock COMPAS-style object that looks like our encoder output
        mock_ufloat = {
            'dtype': 'compas.units/UncertaintiesUFloatEncoder',
            'data': {'nominal_value': 1.23, 'std_dev': 0.05}
        }
        
        # Serialize and deserialize
        json_str = json.dumps(mock_ufloat)
        reconstructed = json.loads(json_str, cls=DataDecoder)
        
        # Should fallback to nominal value only
        assert reconstructed == 1.23