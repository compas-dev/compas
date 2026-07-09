"""Serialization benchmark harness for COMPAS core (PRD-serialization.md, phase 1).

This package builds the measurement instrument the serialization PRD is decided
against: deterministic ``Mesh``/``Pointcloud`` fixtures at several sizes, a
pluggable registry of serialization formats, and metrics (size, serialize /
deserialize time, peak memory, round-trip fidelity).

New formats (safe protobuf, Arrow/columnar) plug into ``formats.py`` without
touching the fixtures or the runner, so results stay comparable across phases.
"""
