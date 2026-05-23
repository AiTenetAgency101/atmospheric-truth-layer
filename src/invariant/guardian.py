"""
Layer H — Guardian (Kaitiakitanga / Guardian State)

Watchdog coroutine that enforces the unified field invariant at runtime.

Every engine MUST call ``await guardian.assert_field(k_value, context)``
before executing any decision.  If the K-value falls below the floor
(H_INVARIANT["k_value_floor"] = 0.99) the guardian raises ``FieldViolation``
and the execution gate remains closed.

All decisions are logged with the full H→N→C→O context block so the
audit trail mirrors the field structure.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from .field_state import H_INVARIANT, K_VALUE_FLOOR, FieldState

logger = logging.getLogger(__name__)


class FieldViolation(RuntimeError):
    """
    Raised when the unified field invariant is breached.

    The engine MUST NOT execute the decision that triggered this exception.
    """

    def __init__(self, message: str, k_value: float, floor: float) -> None:
        super().__init__(message)
        self.k_value = k_value
        self.floor = floor


class FieldGuardian:
    """
    Runtime guardian of the H-layer invariant.

    Usage (inside an engine main loop)::

        guardian = FieldGuardian()

        # Before any decision:
        await guardian.assert_field(
            k_value=self.k_value,
            context={
                "N_pattern": "consensus_pattern",
                "C_structure": "ultimate_engine",
                "O_flow": "atl:field:flow",
            },
        )
        # Only reaches here if K >= 0.99 and anchor is intact.
    """

    def __init__(self) -> None:
        self._violation_count: int = 0
        self._assertion_count: int = 0

    # ------------------------------------------------------------------
    # Core assertion
    # ------------------------------------------------------------------

    async def assert_field(
        self,
        k_value: float,
        context: Optional[Dict[str, Any]] = None,
        proposal: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Assert that the unified field is coherent.

        Checks:
        1. The genesis anchor is still intact (``AnchorLoader.verify()``).
        2. The provided ``k_value`` meets the K_VALUE_FLOOR.

        Raises ``FieldViolation`` if either check fails.
        Logs a structured ``{ H_state, N_pattern, C_structure, O_flow }``
        context block for every call (pass or fail).
        """
        self._assertion_count += 1
        floor = H_INVARIANT["k_value_floor"]

        # Build structured log context
        log_ctx = self._build_log_context(k_value, floor, context, proposal)

        # Check 1 — K-value floor
        if k_value < floor:
            self._violation_count += 1
            log_ctx["gate"] = "CLOSED"
            log_ctx["reason"] = f"k_value={k_value:.4f} < floor={floor}"
            logger.warning("FieldViolation — %s", log_ctx)
            raise FieldViolation(
                f"Field coherence below floor: k_value={k_value:.4f} < floor={floor}",
                k_value=k_value,
                floor=floor,
            )

        # Check 2 — anchor integrity (lightweight re-verify)
        if not FieldState.loader.verify():
            self._violation_count += 1
            log_ctx["gate"] = "CLOSED"
            log_ctx["reason"] = "anchor integrity check failed"
            logger.error("FieldViolation — anchor tampered — %s", log_ctx)
            raise FieldViolation(
                "Genesis anchor integrity check failed — unified field compromised.",
                k_value=k_value,
                floor=floor,
            )

        log_ctx["gate"] = "OPEN"
        logger.info("Field assertion PASSED — %s", log_ctx)

    # ------------------------------------------------------------------
    # Continuous watchdog (optional background task)
    # ------------------------------------------------------------------

    async def watch(
        self,
        k_value_provider,
        interval_seconds: float = 30.0,
    ) -> None:
        """
        Continuously watch the field state.

        ``k_value_provider`` must be a zero-argument async callable that
        returns the current K-value float.  The watchdog logs warnings
        whenever K dips below floor but does **not** raise — it is
        informational only (engines self-gate via ``assert_field``).
        """
        logger.info("FieldGuardian watchdog started (interval=%.1fs)", interval_seconds)
        while True:
            await asyncio.sleep(interval_seconds)
            try:
                k_value = await k_value_provider()
                floor = H_INVARIANT["k_value_floor"]
                if k_value < floor:
                    logger.warning(
                        "Watchdog: K-value below floor (k=%.4f < floor=%.2f)",
                        k_value,
                        floor,
                    )
                else:
                    logger.debug(
                        "Watchdog: field coherent (k=%.4f >= floor=%.2f)",
                        k_value,
                        floor,
                    )
            except Exception as exc:
                logger.error("FieldGuardian watchdog error: %s", exc)

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------

    def get_metrics(self) -> Dict[str, Any]:
        """Return guardian health metrics."""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "assertion_count": self._assertion_count,
            "violation_count": self._violation_count,
            "k_value_floor": H_INVARIANT["k_value_floor"],
            "coherence_hash": H_INVARIANT["coherence_hash"],
            "lattice_root": H_INVARIANT["lattice_root"],
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_log_context(
        k_value: float,
        floor: float,
        context: Optional[Dict[str, Any]],
        proposal: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        ctx = context or {}
        return {
            "H_state": {
                "coherence_hash": H_INVARIANT.get("coherence_hash", "")[:16],
                "origin": H_INVARIANT.get("origin", ""),
                "k_value_floor": floor,
            },
            "N_pattern": ctx.get("N_pattern", ""),
            "C_structure": ctx.get("C_structure", ""),
            "O_flow": ctx.get("O_flow", ""),
            "k_value": round(k_value, 6),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "proposal": proposal,
        }
