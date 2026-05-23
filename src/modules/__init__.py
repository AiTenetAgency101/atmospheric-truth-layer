"""
Layer N — Modules (Hinengaro / Mind / Pattern)

Shared library modules imported by all engines.

H → N → C → O
Modules are the shared cognitive substrate.
"""

from .satellite_decoder import SatelliteDecoder, SatelliteSource, NormalisedFrame
from .hash_fabric import HashFabric
from .cycle_clock import CycleClock

__all__ = [
    "SatelliteDecoder",
    "SatelliteSource",
    "NormalisedFrame",
    "HashFabric",
    "CycleClock",
]
