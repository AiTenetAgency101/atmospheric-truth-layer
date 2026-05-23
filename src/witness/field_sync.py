"""
Layer O — Field Sync (Mauri / Life Force / Flow)

Emits consensus state to the XYO ledger after every engine decision cycle.

After each cycle the field sync module:
1. Builds a ledger entry combining H/N/C/O state.
2. Writes it to the in-memory witnessed ledger (append-only).
3. Publishes the entry to the Redis pub/sub channel ``atl:field:flow``
   (if Redis is available).

This makes O the living sap of the lattice tree.
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.invariant.field_state import H_INVARIANT, K_VALUE_FLOOR

logger = logging.getLogger(__name__)

# Redis pub/sub channel name
FIELD_FLOW_CHANNEL = "atl:field:flow"


class FieldSync:
    """
    O-layer sync module — emits consensus state to ledger and Redis.

    Usage::

        sync = FieldSync(redis_client=redis)   # redis_client is optional
        entry = await sync.emit(
            engine_id=2,
            k_value=0.995,
            n_pattern="ConsensusPattern",
            c_structure="UltimateEngine/ENGINE2",
            decision="ACCEPTED",
            proposal={"type": "tile_commit"},
        )
    """

    def __init__(self, redis_client=None) -> None:
        self._redis = redis_client
        self._ledger: List[Dict[str, Any]] = []  # append-only in-memory ledger

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def emit(
        self,
        engine_id: int,
        k_value: float,
        n_pattern: str,
        c_structure: str,
        decision: str,
        proposal: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Build, record, and broadcast a field-flow ledger entry.

        Returns the ledger entry dict.
        """
        entry = self._build_entry(
            engine_id=engine_id,
            k_value=k_value,
            n_pattern=n_pattern,
            c_structure=c_structure,
            decision=decision,
            proposal=proposal,
        )

        # Append-only ledger (O-layer immutable record)
        self._ledger.append(entry)

        # Publish to Redis if available
        await self._publish(entry)

        logger.info(
            "FieldSync emitted: engine_id=%d decision=%s k=%.4f entry_hash=%s",
            engine_id,
            decision,
            k_value,
            entry["entry_hash"][:16],
        )
        return entry

    def get_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Return the most recent ``limit`` ledger entries."""
        return self._ledger[-limit:]

    def ledger_size(self) -> int:
        return len(self._ledger)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_entry(
        self,
        engine_id: int,
        k_value: float,
        n_pattern: str,
        c_structure: str,
        decision: str,
        proposal: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        timestamp = datetime.utcnow().isoformat() + "Z"
        entry_body = {
            "timestamp": timestamp,
            "engine_id": engine_id,
            "decision": decision,
            "k_value": k_value,
            "H_state": {
                "coherence_hash": H_INVARIANT.get("coherence_hash", "")[:16],
                "k_value_floor": K_VALUE_FLOOR,
                "lattice_root": "H",
            },
            "N_pattern": n_pattern,
            "C_structure": c_structure,
            "O_flow": FIELD_FLOW_CHANNEL,
            "proposal": proposal or {},
        }
        canonical = json.dumps(entry_body, sort_keys=True, separators=(",", ":"))
        entry_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return {**entry_body, "entry_hash": entry_hash, "immutable": True}

    async def _publish(self, entry: Dict[str, Any]) -> None:
        """Publish entry to Redis pub/sub (no-op if Redis unavailable)."""
        if self._redis is None:
            return
        try:
            message = json.dumps(entry, separators=(",", ":"))
            await self._redis.publish(FIELD_FLOW_CHANNEL, message)
        except Exception as exc:
            logger.warning("FieldSync Redis publish failed: %s", exc)
