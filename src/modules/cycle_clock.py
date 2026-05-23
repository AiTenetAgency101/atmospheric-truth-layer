"""
Layer N — Cycle Clock Module (Hinengaro / Mind / Pattern)

365-day cycle lock logic extracted from Engine 365-Days.

The cycle clock governs the temporal anchor of the entire field.
All engines share one inception timestamp (from ANCHOR.json) and one
expiry (inception + 365 days).  The wobble constants (SUU, AHA, RERE)
define the three strata of temporal tolerance.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from src.invariant.field_state import H_INVARIANT

logger = logging.getLogger(__name__)

# Inception timestamp — mirrors what is in ANCHOR.json / CycleLock
_INCEPTION_ISO = "2026-04-23T07:53:50.514499+10:00"

# Wobble constants — three strata of temporal tolerance
SUU = 0.05    # Foundation layer
AHA = 0.075   # Harmonic layer
RERE = 0.15   # Resonance layer


class CycleClock:
    """
    365-day cycle lock module.

    Usage::

        clock = CycleClock()
        print(clock.is_valid())     # True while within 365-day window
        print(clock.get_state())    # full state dict
    """

    def __init__(self) -> None:
        self.lock_id = "7f4a9e2c-8d3b-47e1-9f6c-2a5d8e1b4f7a"

        # Parse inception from ANCHOR.json origin if available, else default
        origin = H_INVARIANT.get("origin", _INCEPTION_ISO)
        try:
            self.inception = datetime.fromisoformat(origin)
        except ValueError:
            logger.warning(
                "CycleClock: cannot parse origin %r — using default", origin
            )
            self.inception = datetime.fromisoformat(_INCEPTION_ISO)

        self.expiry = self.inception + timedelta(days=365)

        logger.info(
            "CycleClock initialised — inception=%s expiry=%s",
            self.inception.isoformat(),
            self.expiry.isoformat(),
        )

    def is_valid(self) -> bool:
        """Return True while the current time is before expiry."""
        now = datetime.now(tz=self.inception.tzinfo)
        return now < self.expiry

    def remaining_days(self) -> float:
        """Number of days remaining in the cycle (may be negative if expired)."""
        now = datetime.now(tz=self.inception.tzinfo)
        delta = self.expiry - now
        return delta.total_seconds() / 86400.0

    def elapsed_days(self) -> float:
        """Days elapsed since inception."""
        now = datetime.now(tz=self.inception.tzinfo)
        delta = now - self.inception
        return max(0.0, delta.total_seconds() / 86400.0)

    def get_state(self) -> Dict[str, Any]:
        """Return the full cycle clock state dict."""
        return {
            "lock_id": self.lock_id,
            "inception": self.inception.isoformat(),
            "expiry": self.expiry.isoformat(),
            "valid": self.is_valid(),
            "elapsed_days": round(self.elapsed_days(), 4),
            "remaining_days": round(self.remaining_days(), 4),
            "wobble_constants": {
                "SUU": SUU,
                "AHA": AHA,
                "RERE": RERE,
            },
            "lattice_layer": "H",
        }
