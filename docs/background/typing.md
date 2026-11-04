# Type Annotations

COMPAS type annotations describe the values that an API can consume. They help
static type checkers find mistakes, but they do not add runtime validation or
conversion.

## Numeric input families

The aliases in `compas._typing` cover the numeric families used by COMPAS APIs:

- `RealInput` accepts the built-in `int` and `float` families and NumPy integer
  and floating scalar families.
- `IntegralInput` accepts the built-in `int` family and the NumPy integer scalar
  family.
- `NumericArray`, `FloatingArray`, and `IntegerArray` describe NumPy arrays by
  scalar family. `Float64Array` and `Int32Array` describe the two cases where an
  exact dtype is part of the contract.
- `CoordinateInput`, `CoordinatesInput`, and `IndicesInput` combine structural
  Python inputs with the corresponding NumPy array families.

These aliases intentionally support duck typing. APIs should operate on the
capabilities they need instead of requiring a particular concrete container or
performing nominal type checks. Conversion belongs at an explicit boundary only
when an implementation requires a specific representation.

Python's `bool` is a subclass of `int`, so static checkers include it in the
built-in integer family. NumPy's `bool_` is not a NumPy integer and is excluded.
An API that cannot meaningfully accept boolean values should reject them at its
own runtime boundary; the shared aliases do not add a blanket runtime check.

There is no shared scalar protocol at this stage. The current operations do not
demonstrate one stable scalar capability that would be both useful and more
accurate than the explicit built-in and NumPy families. Runtime duck typing
continues wherever an operation can consume a value by capability alone.

## Static types and runtime invariants

An annotation cannot express every runtime requirement. For example, a numeric
array annotation does not specify that a coordinate has exactly three values,
that a collection has a particular rank, or that indices are within bounds.
Such requirements remain part of the documented API contract and should be
checked only where the operation needs them.

The runtime-checkable `Coordinate` and `Coordinates` protocols predate the input
aliases and retain their existing structural `isinstance` behavior. The broader
input aliases are static annotations: they must not be passed to `isinstance`
and do not imply runtime validation.

## Static fixture convention

Static typing behavior is characterized by `tests/typing/accepted.py` and
`tests/typing/expected_errors.py`. The accepted fixture must produce no Pyright
diagnostics. Every diagnostic in the negative fixture is declared on the same
line with an exact rule marker:

```python
value: IntegralInput = 1.5  # expected-error: reportAssignmentType
```

The pytest harness compares the diagnostic file, line, and rule with these
markers. Missing, additional, or moved diagnostics therefore fail the tests.
