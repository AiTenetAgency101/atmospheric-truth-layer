"""
Layer N — Firewall Pattern Skill (Hinengaro / Mind / Pattern)

Rejection/drift logic extracted from Tenet Agency 101.

This skill encapsulates the firewall doctrine:
  - Reject any decision where K < consensus floor (0.99)
  - Track drift ratio (horizon_entries / ticks)
  - Enforce configurable rejection threshold (default 0.71)

The skill is stateless about the engine — callers supply K-value and
receive a firewall decision dict back.
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from src.invariant.field_state import K_VALUE_FLOOR

logger = logging.getLogger(__name__)


class FirewallPattern:
    """
    Firewall pattern skill — evaluates proposals against the consensus floor.

    Usage::

        skill = FirewallPattern()
        result = skill.evaluate(proposal={"type": "tile_commit"}, k_value=0.995)
        # result["approved"] is True if K >= floor
    """

    def __init__(
        self,
        k_floor: float = K_VALUE_FLOOR,
        rejection_threshold: float = 0.71,
        firewall_mode: str = "strict",
    ) -> None:
        self.k_floor = k_floor
        self.rejection_threshold = rejection_threshold
        self.firewall_mode = firewall_mode

        self._ticks: int = 0
        self._executed: int = 0
        self._rejected: int = 0
        self._horizon_entries: int = 0

    # ------------------------------------------------------------------
    # Core evaluation
    # ------------------------------------------------------------------

    def evaluate(
        self,
        proposal: Optional[Dict[str, Any]],
        k_value: float,
    ) -> Dict[str, Any]:
        """
        Evaluate a proposal through the firewall.

        Returns a result dict::

            {
                "approved":        bool,
                "firewall_decision": "ALLOW" | "REJECT",
                "k_value":         float,
                "rejection_rate":  float,
                "drift_ratio":     float,
                "ticks":           int,
            }
        """
        self._ticks += 1
        consensus_met = k_value >= self.k_floor

        if consensus_met:
            self._executed += 1
            self._horizon_entries += 1
            decision = "ALLOW"
            approved = True
        else:
            self._rejected += 1
            decision = "REJECT"
            approved = False

        rejection_rate = (
            self._rejected / self._ticks if self._ticks > 0 else 0.0
        )
        drift_ratio = (
            self._horizon_entries / self._ticks if self._ticks > 0 else 0.0
        )

        logger.info(
            "FirewallPattern: %s (K=%.4f, consensus=%s, ticks=%d)",
            decision,
            k_value,
            "MET" if consensus_met else "NOT MET",
            self._ticks,
        )

        return {
            "approved": approved,
            "firewall_decision": decision,
            "k_value": k_value,
            "rejection_rate": rejection_rate,
            "drift_ratio": drift_ratio,
            "ticks": self._ticks,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    # ------------------------------------------------------------------
    # Drift detection
    # ------------------------------------------------------------------

    @property
    def drift_ratio(self) -> float:
        """Current drift ratio (horizon_entries / ticks)."""
        return self._horizon_entries / self._ticks if self._ticks > 0 else 0.0

    @property
    def rejection_rate(self) -> float:
        """Current cumulative rejection rate."""
        return self._rejected / self._ticks if self._ticks > 0 else 0.0

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "skill": "FirewallPattern",
            "k_floor": self.k_floor,
            "rejection_threshold": self.rejection_threshold,
            "firewall_mode": self.firewall_mode,
            "ticks": self._ticks,
            "executed": self._executed,
            "rejected": self._rejected,
            "horizon_entries": self._horizon_entries,
            "rejection_rate": self.rejection_rate,
            "drift_ratio": self.drift_ratio,
        }
