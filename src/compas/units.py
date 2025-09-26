"""
Unit and uncertainty support for COMPAS.

This module provides optional support for physical units and measurement uncertainties
throughout the COMPAS framework. The implementation follows a gradual typing approach
where unit-aware inputs produce unit-aware outputs, but plain numeric inputs continue
to work as before.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from typing import Union
except ImportError:
    pass

__all__ = ['UnitRegistry', 'units', 'NumericType', 'UNITS_AVAILABLE', 'UNCERTAINTIES_AVAILABLE', 'PintQuantityEncoder', 'UncertaintiesUFloatEncoder']

# Check for optional dependencies
try:
    import pint
    UNITS_AVAILABLE = True
except ImportError:
    UNITS_AVAILABLE = False
    pint = None

try:
    import uncertainties
    UNCERTAINTIES_AVAILABLE = True
except ImportError:
    UNCERTAINTIES_AVAILABLE = False
    uncertainties = None

# Define numeric type union
try:
    NumericType = Union[float, int]
    if UNITS_AVAILABLE:
        NumericType = Union[NumericType, pint.Quantity]
    if UNCERTAINTIES_AVAILABLE:
        NumericType = Union[NumericType, uncertainties.UFloat]
except NameError:
    # typing.Union not available, just use documentation comment
    NumericType = float  # Union[float, int, pint.Quantity, uncertainties.UFloat] when available


class PintQuantityEncoder:
    """Encoder/decoder for pint.Quantity objects following COMPAS data serialization patterns."""
    
    @staticmethod
    def __jsondump__(obj):
        """Serialize a pint.Quantity to COMPAS JSON format.
        
        Parameters
        ----------
        obj : pint.Quantity
            The quantity to serialize.
            
        Returns
        -------
        dict
            Dictionary with dtype and data keys.
        """
        return {
            'dtype': 'compas.units/PintQuantityEncoder',
            'data': {
                'magnitude': obj.magnitude,
                'units': str(obj.units)
            }
        }
    
    @staticmethod
    def __from_data__(data):
        """Reconstruct a pint.Quantity from serialized data.
        
        Parameters
        ----------
        data : dict
            The serialized data containing magnitude and units.
            
        Returns
        -------
        pint.Quantity or float
            The reconstructed quantity, or magnitude if pint not available.
        """
        if UNITS_AVAILABLE:
            # Import units registry from this module
            return units.ureg.Quantity(data['magnitude'], data['units'])
        else:
            # Graceful degradation - return just the magnitude
            return data['magnitude']
    
    @staticmethod 
    def __jsonload__(data, guid=None, name=None):
        """Load method for COMPAS JSON deserialization."""
        return PintQuantityEncoder.__from_data__(data)


class UncertaintiesUFloatEncoder:
    """Encoder/decoder for uncertainties.UFloat objects following COMPAS data serialization patterns."""
    
    @staticmethod
    def __jsondump__(obj):
        """Serialize an uncertainties.UFloat to COMPAS JSON format.
        
        Parameters
        ----------
        obj : uncertainties.UFloat
            The uncertain value to serialize.
            
        Returns
        -------
        dict
            Dictionary with dtype and data keys.
        """
        return {
            'dtype': 'compas.units/UncertaintiesUFloatEncoder',
            'data': {
                'nominal_value': obj.nominal_value,
                'std_dev': obj.std_dev
            }
        }
    
    @staticmethod
    def __from_data__(data):
        """Reconstruct an uncertainties.UFloat from serialized data.
        
        Parameters
        ----------
        data : dict
            The serialized data containing nominal_value and std_dev.
            
        Returns
        -------
        uncertainties.UFloat or float
            The reconstructed uncertain value, or nominal value if uncertainties not available.
        """
        if UNCERTAINTIES_AVAILABLE:
            return uncertainties.ufloat(data['nominal_value'], data['std_dev'])
        else:
            # Graceful degradation - return just the nominal value
            return data['nominal_value']
    
    @staticmethod
    def __jsonload__(data, guid=None, name=None):
        """Load method for COMPAS JSON deserialization."""
        return UncertaintiesUFloatEncoder.__from_data__(data)


class UnitRegistry:
    """Global unit registry for COMPAS.
    
    This class provides a centralized way to create and manage units throughout
    the COMPAS framework. It gracefully handles the case where pint is not available.
    
    Examples
    --------
    >>> from compas.units import units
    >>> length = units.Quantity(1.0, 'meter')  # Returns 1.0 if pint not available
    >>> area = units.Quantity(2.5, 'square_meter')
    """
    
    def __init__(self):
        if UNITS_AVAILABLE:
            self.ureg = pint.UnitRegistry()
            # Use built-in units - no need to redefine basic units
            # The registry already has meter, millimeter, etc.
        else:
            self.ureg = None
    
    def Quantity(self, value, unit=None):
        """Create a quantity with units if available, otherwise return plain value.
        
        Parameters
        ----------
        value : float
            The numeric value.
        unit : str, optional
            The unit string. If None or if pint is not available, returns plain value.
            
        Returns
        -------
        pint.Quantity or float
            A quantity with units if pint is available, otherwise the plain value.
        """
        if UNITS_AVAILABLE and unit and self.ureg:
            return self.ureg.Quantity(value, unit)
        return value
    
    def Unit(self, unit_string):
        """Get a unit object if available.
        
        Parameters
        ----------
        unit_string : str
            The unit string (e.g., 'meter', 'mm', 'inch').
            
        Returns
        -------
        pint.Unit or None
            A unit object if pint is available, otherwise None.
        """
        if UNITS_AVAILABLE and self.ureg:
            return self.ureg.Unit(unit_string)
        return None
    
    @property
    def meter(self):
        """Meter unit for convenience."""
        return self.Unit('m')
    
    @property 
    def millimeter(self):
        """Millimeter unit for convenience."""
        return self.Unit('mm')
        
    @property
    def centimeter(self):
        """Centimeter unit for convenience."""
        return self.Unit('cm')


def ensure_numeric(value):
    """Ensure a value is numeric, preserving units and uncertainties if present.
    
    Parameters
    ----------
    value : any
        Input value that should be numeric.
        
    Returns
    -------
    NumericType
        A numeric value, preserving units/uncertainties if present.
    """
    # Check for pint Quantity
    if hasattr(value, 'magnitude') and hasattr(value, 'units'):
        return value
    
    # Check for uncertainties UFloat  
    if hasattr(value, 'nominal_value') and hasattr(value, 'std_dev'):
        return value
        
    # Convert to float for plain values
    return float(value)


def get_magnitude(value):
    """Get the magnitude of a value, handling units and uncertainties.
    
    Parameters
    ----------  
    value : NumericType
        A numeric value that may have units or uncertainties.
        
    Returns
    -------
    float
        The magnitude/nominal value without units.
    """
    # Handle pint Quantity
    if hasattr(value, 'magnitude'):
        return float(value.magnitude)
    
    # Handle uncertainties UFloat
    if hasattr(value, 'nominal_value'):
        return float(value.nominal_value)
    
    # Plain numeric value
    return float(value)


def has_units(value):
    """Check if a value has units.
    
    Parameters
    ----------
    value : any
        Value to check for units.
        
    Returns  
    -------
    bool
        True if the value has units, False otherwise.
    """
    return hasattr(value, 'magnitude') and hasattr(value, 'units')


def has_uncertainty(value):
    """Check if a value has uncertainty.
    
    Parameters
    ----------
    value : any
        Value to check for uncertainty.
        
    Returns
    -------
    bool  
        True if the value has uncertainty, False otherwise.
    """
    return hasattr(value, 'nominal_value') and hasattr(value, 'std_dev')


# Global registry instance
units = UnitRegistry()