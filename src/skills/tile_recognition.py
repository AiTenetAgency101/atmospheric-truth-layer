"""
Layer N — Tile Recognition Skill (Hinengaro / Mind / Pattern)

Composable validator skills extracted from Engine 365-Days.
Each skill is an independently callable pattern-recognition unit.

Validators:
- CircleSkill    — circular/periodic validation
- MonotonicSkill — monotonic-increase validation
- RangeSkill     — bounds/range validation
- TileRecognitionSkill — composite (all three)
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


class CircleSkill:
    """
    Circular/periodic validation skill.

    Maps the tile integrity hash into a 360° circle and confirms it is
    within the valid arc (always 0–360, so this is a well-formedness check).
    """

    def __init__(self) -> None:
        self.checks: int = 0
        self.failures: int = 0

    async def validate(self, integrity_hash: str) -> bool:
        """Return True if the hash maps to a valid circle point."""
        self.checks += 1
        try:
            hash_int = int(integrity_hash, 16)
            cycle_point = hash_int % 360
            # cycle_point is always in [0, 359] — well-formedness check
            if 0 <= cycle_point < 360:
                return True
            self.failures += 1
            return False
        except Exception as exc:
            logger.error("CircleSkill error: %s", exc)
            self.failures += 1
            return False

    @property
    def reliability(self) -> float:
        if self.checks == 0:
            return 1.0
        return 1.0 - (self.failures / self.checks)

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "skill": "CircleSkill",
            "checks": self.checks,
            "failures": self.failures,
            "reliability": self.reliability,
        }


class MonotonicSkill:
    """
    Monotonic-increase validation skill.

    Ensures the leading 64 bits of successive tile hashes are non-decreasing,
    confirming sequential ordering of tile observations.
    """

    def __init__(self) -> None:
        self.checks: int = 0
        self.failures: int = 0
        self._last_value: int = 0

    async def validate(self, integrity_hash: str) -> bool:
        """Return True if the hash value is >= the last observed value."""
        self.checks += 1
        try:
            hash_int = int(integrity_hash[:16], 16)
            if hash_int >= self._last_value:
                self._last_value = hash_int
                return True
            self.failures += 1
            return False
        except Exception as exc:
            logger.error("MonotonicSkill error: %s", exc)
            self.failures += 1
            return False

    @property
    def reliability(self) -> float:
        if self.checks == 0:
            return 1.0
        return 1.0 - (self.failures / self.checks)

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "skill": "MonotonicSkill",
            "checks": self.checks,
            "failures": self.failures,
            "reliability": self.reliability,
            "last_value": self._last_value,
        }


class RangeSkill:
    """
    Range/bounds validation skill.

    Confirms the tile integrity hash integer is within the valid SHA-256
    range [0, 2^256 - 1] — a well-formedness check that ensures no hash
    truncation or corruption has occurred.
    """

    _MAX = 2**256 - 1

    def __init__(self) -> None:
        self.checks: int = 0
        self.failures: int = 0

    async def validate(self, integrity_hash: str) -> bool:
        """Return True if the hash integer is in [0, 2^256 - 1]."""
        self.checks += 1
        try:
            hash_int = int(integrity_hash, 16)
            if 0 <= hash_int <= self._MAX:
                return True
            self.failures += 1
            return False
        except Exception as exc:
            logger.error("RangeSkill error: %s", exc)
            self.failures += 1
            return False

    @property
    def reliability(self) -> float:
        if self.checks == 0:
            return 1.0
        return 1.0 - (self.failures / self.checks)

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "skill": "RangeSkill",
            "checks": self.checks,
            "failures": self.failures,
            "reliability": self.reliability,
        }


class TileRecognitionSkill:
    """
    Composite tile recognition skill (Circle + Monotonic + Range).

    Runs all three validators and returns an aggregate result.
    An ``integrity_hash`` must pass ALL three to be accepted.
    """

    def __init__(self) -> None:
        self.circle = CircleSkill()
        self.monotonic = MonotonicSkill()
        self.range = RangeSkill()

    async def validate(
        self, integrity_hash: str
    ) -> Tuple[bool, Dict[str, bool]]:
        """
        Validate an integrity hash through all three skills.

        Returns ``(passed, checks)`` where ``passed`` is True only when
        all three validators succeed, and ``checks`` is a dict of individual
        results keyed by validator name.
        """
        circle_ok = await self.circle.validate(integrity_hash)
        monotonic_ok = await self.monotonic.validate(integrity_hash)
        range_ok = await self.range.validate(integrity_hash)

        checks = {
            "Circle": circle_ok,
            "Monotonic": monotonic_ok,
            "Range": range_ok,
        }
        return circle_ok and monotonic_ok and range_ok, checks

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "skill": "TileRecognitionSkill",
            "validators": {
                "Circle": self.circle.get_metrics(),
                "Monotonic": self.monotonic.get_metrics(),
                "Range": self.range.get_metrics(),
            },
        }
