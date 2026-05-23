"""
Layer N — Consensus Pattern Skill (Hinengaro / Mind / Pattern)

K-value consensus pattern logic extracted from Ultimate Engine.

This skill encapsulates the Byzantine phase-space computation:
  dX/dt = -λ(X - X_ref)

and returns a K-value representing field coherence across N engine states.
The skill is stateless with respect to the engine ring — callers supply
the engine states and receive K back.
"""

import logging
import math
from typing import Any, Dict, List, Tuple

from src.invariant.field_state import K_VALUE_FLOOR

logger = logging.getLogger(__name__)

# Convergence constant for the Euler integration step
_LAMBDA = 0.1

# Reference equilibrium point (phase=0, power=0, coherence=0)
_X_REF = (0.0, 0.0, 0.0)


def _distance(phase: float, power: float, coherence: float) -> float:
    """Euclidean distance from the reference equilibrium point."""
    return math.sqrt(
        (phase - _X_REF[0]) ** 2
        + (power - _X_REF[1]) ** 2
        + (coherence - _X_REF[2]) ** 2
    )


def evolve_state(
    phase: float, power: float, coherence: float
) -> Tuple[float, float, float]:
    """
    Apply one Euler integration step toward equilibrium.

    Returns the updated (phase, power, coherence) tuple.
    """
    new_phase = (phase - _LAMBDA * (phase - _X_REF[0])) % (2 * math.pi)
    new_power = max(-1.0, min(1.0, power - _LAMBDA * (power - _X_REF[1])))
    new_coherence = max(-1.0, min(1.0, coherence - _LAMBDA * (coherence - _X_REF[2])))
    return new_phase, new_power, new_coherence


class ConsensusPattern:
    """
    Byzantine K-value consensus pattern skill.

    Usage::

        skill = ConsensusPattern()
        k_value = skill.compute_k(engine_states)
        gate_open = skill.execution_gate_open(k_value)
    """

    def __init__(self, k_floor: float = K_VALUE_FLOOR) -> None:
        self.k_floor = k_floor
        self._runs: int = 0

    def compute_k(
        self, engine_states: Dict[int, Dict[str, float]]
    ) -> float:
        """
        Compute the K-value (coherence metric) from the provided engine states.

        ``engine_states`` is a dict mapping engine_id → {phase, power, coherence}.

        K = 1 / (1 + mean_distance_from_equilibrium)

        A K-value of 1.0 means perfect coherence; 0.0 means total divergence.
        """
        if not engine_states:
            logger.warning("ConsensusPattern.compute_k called with empty engine_states")
            return 0.0

        distances = [
            _distance(
                state.get("phase", 0.0),
                state.get("power", 0.0),
                state.get("coherence", 0.0),
            )
            for state in engine_states.values()
        ]
        avg_distance = sum(distances) / len(distances)
        k_value = 1.0 / (1.0 + avg_distance)
        self._runs += 1
        logger.debug(
            "ConsensusPattern: K=%.4f (avg_dist=%.4f, n=%d engines)",
            k_value,
            avg_distance,
            len(engine_states),
        )
        return k_value

    def execution_gate_open(self, k_value: float) -> bool:
        """Return True if the K-value meets the consensus floor."""
        return k_value >= self.k_floor

    def evolve_all(
        self, engine_states: Dict[int, Dict[str, float]]
    ) -> Dict[int, Dict[str, float]]:
        """
        Apply one Euler integration step to every engine state.

        Returns a new dict with evolved states (does not mutate input).
        """
        evolved = {}
        for engine_id, state in engine_states.items():
            new_phase, new_power, new_coherence = evolve_state(
                state.get("phase", 0.0),
                state.get("power", 0.0),
                state.get("coherence", 0.0),
            )
            evolved[engine_id] = {
                "phase": new_phase,
                "power": new_power,
                "coherence": new_coherence,
                "engine_id": engine_id,
            }
        return evolved

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "skill": "ConsensusPattern",
            "k_floor": self.k_floor,
            "runs": self._runs,
            "lambda_convergence": _LAMBDA,
        }
