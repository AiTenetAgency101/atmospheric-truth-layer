"""
Layer H — Field State (Wairua / Spirit / Origin)

Singleton that holds the unified field state derived from the genesis anchor.

H_INVARIANT is the read-only field state dict::

    {
        "origin":          <witness_timestamp from ANCHOR.json>,
        "coherence_hash":  <roothash from ANCHOR.json>,
        "lattice_root":    "H",
        "k_value_floor":   0.99,
        "minted_version":  <version from ANCHOR.json>,
        "ledger_position": 0,
    }

All engines and layers reference ``H_INVARIANT`` and ``K_VALUE_FLOOR``
as their authoritative source of coherence.
"""

import logging
import os
from typing import Any, Dict

from .anchor_loader import AnchorLoader, AnchorViolation

logger = logging.getLogger(__name__)

# K-value floor — the minimum consensus coherence required for execution gates to open
K_VALUE_FLOOR: float = 0.99


def _build_invariant(anchor_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "origin": anchor_data.get("witness_timestamp", ""),
        "coherence_hash": anchor_data.get("roothash", ""),
        "lattice_root": "H",
        "k_value_floor": K_VALUE_FLOOR,
        "minted_version": anchor_data.get("version", ""),
        "ledger_position": anchor_data.get("ledger_position", 0),
        "witnessed": anchor_data.get("witnessed", False),
        "tamper_proof": anchor_data.get("tamper_proof", False),
        "immutable": anchor_data.get("immutable", False),
    }


class _FieldState:
    """
    Singleton field-state holder.

    Call ``initialise()`` once at application startup (or let it initialise
    lazily on first access via ``H_INVARIANT``).
    """

    def __init__(self) -> None:
        self._invariant: Dict[str, Any] = {}
        self._initialised: bool = False
        self._loader: AnchorLoader = AnchorLoader()

    def initialise(self) -> None:
        """Load the anchor and build the invariant dict.  Idempotent."""
        if self._initialised:
            return
        anchor_path_override = os.environ.get("ANCHOR_PATH")
        if anchor_path_override:
            from pathlib import Path

            self._loader = AnchorLoader(Path(anchor_path_override))
        anchor_data = self._loader.load()
        self._invariant = _build_invariant(anchor_data)
        self._initialised = True
        logger.info(
            "Field state initialised — origin=%s coherence_hash=%s",
            self._invariant["origin"],
            self._invariant["coherence_hash"][:16],
        )

    @property
    def invariant(self) -> Dict[str, Any]:
        if not self._initialised:
            self.initialise()
        return dict(self._invariant)  # return a copy to preserve read-only semantics

    @property
    def coherence_hash(self) -> str:
        return self.invariant["coherence_hash"]

    @property
    def origin(self) -> str:
        return self.invariant["origin"]

    @property
    def loader(self) -> AnchorLoader:
        return self._loader


# Module-level singleton
_field_state = _FieldState()


def _get_invariant() -> Dict[str, Any]:
    """Lazy-initialise and return H_INVARIANT."""
    return _field_state.invariant


class _InvariantProxy(dict):
    """
    A dict subclass that populates itself from the field state on first access.
    This allows ``H_INVARIANT`` to be imported at module level without
    triggering anchor I/O immediately.
    """

    def __missing__(self, key: str) -> Any:
        self.update(_field_state.invariant)
        return super().__getitem__(key)

    def __repr__(self) -> str:  # pragma: no cover
        self.update(_field_state.invariant)
        return f"H_INVARIANT({super().__repr__()})"


# Public read-only interface to the H-layer invariant
H_INVARIANT: Dict[str, Any] = _InvariantProxy()

# Expose the singleton for direct access when needed
FieldState = _field_state
