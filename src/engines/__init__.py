"""
Layer C — Engine Ring Registry (Tinana / Body / Structure)

ENGINE_RING is the single registry of all 14 engines in the E14 Oracle.
Currently E01, E02, and E03 are fully implemented.
E04–E14 are registered as stubs that return their reserved slot identity.

Every engine registers itself with the H-layer invariant at import time,
establishing that C (structure) is always grounded in H (origin).

H → N → C → O
"""

import logging
from typing import Any, Dict

from src.invariant.field_state import H_INVARIANT

logger = logging.getLogger(__name__)


def _stub_engine(engine_id: int) -> Dict[str, Any]:
    """Return a stub identity dict for a reserved engine slot."""
    return {
        "engine_id": engine_id,
        "label": f"E{engine_id:02d}",
        "status": "reserved",
        "lattice_layer": "C",
        "H_coherence_hash": H_INVARIANT.get("coherence_hash", "")[:16],
    }


# ============================================================================
# ENGINE RING — 14-engine registry
# E01 — Engine 365-Days   (Temporal Anchor & Tile Decomposition)
# E02 — Ultimate Engine   (Byzantine Consensus Coordinator / ENGINE2)
# E03 — Tenet Agency 101  (Firewall & Validation)
# E04–E14 — Reserved (stubs)
# ============================================================================

ENGINE_RING: Dict[int, Dict[str, Any]] = {
    1: {
        "engine_id": 1,
        "label": "E01",
        "name": "Engine 365-Days",
        "role": "Temporal Anchor & Tile Decomposition",
        "status": "active",
        "module": "src.engines.engine_365_days",
        "lattice_layer": "C",
        "N_skills": ["TileRecognitionSkill", "CycleClock"],
        "H_coherence_hash": H_INVARIANT.get("coherence_hash", "")[:16],
    },
    2: {
        "engine_id": 2,
        "label": "E02",
        "name": "Ultimate Engine (ENGINE2)",
        "role": "Byzantine Consensus Coordinator — C-layer trunk",
        "status": "active",
        "module": "src.engines.ultimate_engine",
        "lattice_layer": "C",
        "N_skills": ["ConsensusPattern"],
        "H_coherence_hash": H_INVARIANT.get("coherence_hash", "")[:16],
    },
    3: {
        "engine_id": 3,
        "label": "E03",
        "name": "Tenet Agency 101",
        "role": "Firewall & Validation",
        "status": "active",
        "module": "src.engines.tenet_agency_101",
        "lattice_layer": "C",
        "N_skills": ["FirewallPattern"],
        "H_coherence_hash": H_INVARIANT.get("coherence_hash", "")[:16],
    },
    **{i: _stub_engine(i) for i in range(4, 15)},
}


def get_engine(engine_id: int) -> Dict[str, Any]:
    """Return the registry entry for a given engine ID (1-based)."""
    entry = ENGINE_RING.get(engine_id)
    if entry is None:
        raise KeyError(f"Engine {engine_id} is not in the E14 ring (valid: 1–14)")
    return entry


def active_engines() -> Dict[int, Dict[str, Any]]:
    """Return only the active (non-stub) engines."""
    return {eid: e for eid, e in ENGINE_RING.items() if e["status"] == "active"}


def ring_summary() -> Dict[str, Any]:
    """Return a summary of the engine ring state."""
    active = active_engines()
    return {
        "total_engines": len(ENGINE_RING),
        "active_engines": len(active),
        "reserved_engines": len(ENGINE_RING) - len(active),
        "lattice_layer": "C",
        "H_coherence_hash": H_INVARIANT.get("coherence_hash", "")[:16],
        "engines": {str(eid): e.get("name", e.get("label", f"E{eid:02d}")) for eid, e in ENGINE_RING.items()},
    }


logger.info(
    "ENGINE_RING initialised — %d total, %d active, H_coherence=%s",
    len(ENGINE_RING),
    len(active_engines()),
    H_INVARIANT.get("coherence_hash", "")[:16],
)
