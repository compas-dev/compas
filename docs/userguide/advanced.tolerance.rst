********************************************************************************
Dealing with Tolerances
********************************************************************************

.. rst-class:: lead

:class:`compas.tolerance.Tolerance` provides a consistent way of dealing with 
tolerances, precision, comparisons, approximations, number formatting, etc. in COMPAS and across COMPAS packages.

Defaults
========

Different tolerance values are used for different checks and comparisons.
These are the default values:

>>> from compas.tolerance import Tolerance
>>> tol = Tolerance()
>>> tol.absolute
1e-09
>>> tol.relative
1e-06
>>> tol.angular
1e-06
>>> tol.approximation
1e-03
>>> tol.precision
6


Comparisons
===========

Comparisons of numbers involves two types of tolerances: absolute and relative.
The absolute tolerance is a fixed value.
The relative tolerance is relative to the magnitude of the numbers being compared.
When comparing two numbers the following formula is used:

.. math::

    |a - b| \leq relative \cdot |b| + absolute

This means that the relative tolerance dominates the comparison for larger numbers,
while the absolute tolerance becaomes dominant when numbers are close to zero.

>>> tol.is_close(1.1, 1)
False
>>> tol.is_close(100000.1, 1)
True
>>> tol.is_close(1 + 1e-5, 1)
False
>>> tol.is_close(1 + 1e-6, 1)
True
>>> tol.is_close(0 + 1e-6, 0)
False
>>> tol.is_close(0 + 1e-9, 0)
True


Zero, Positive, Negative
========================

Comparisons to zero, and checking if a number is positive or negative, are special cases, and only involve the absolute tolerance.

>>> tol.is_zero(0)
True
>>> tol.is_zero(1e-9)
True
>>> tol.is_zero(1e-8)
False
>>> tol.is_zero(1e-8, tol=1e-8)
True
>>> tol.is_positive(1e-8)
True
>>> tol.is_positive(1e-9)
False
>>> tol.is_negative(-1e-8)
True
>>> tol.is_negative(-1e-9)
False


Number Formatting
=================

By default, numbers are formatted (in strings) using the precision value.

>>> tol.format_number(1.23456)
'1.235'

To use a precision value based on the tolerance, use :meth:`compas.tolerance.Tolerance.precision_from_tolerance`.

>>> tol.format_number(1.23456, precision=tol.precision_from_tolerance())
'1.234560000'

Positive precision values are interpreted as the number of digits after the decimal point.
Negative precision values are interpreted as the number of digits before the decimal point.
So higher values increase precision, and lower number decrease it.

>>> tol.format_number(1.23456, precision=2)
'1.23'
>>> tol.format_number(1.23456, precision=6)
'1.234560'

>>> tol.format_number(123456, precision=-2)
'123460'
>>> tol.format_number(123456, precision=-6)
'100000'
