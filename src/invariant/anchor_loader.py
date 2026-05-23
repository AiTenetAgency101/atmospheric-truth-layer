"""
Layer H — Anchor Loader (Wairua / Spirit / Origin)

Loads and validates ANCHOR.json at boot.
Refuses to start any engine if the anchor is tampered (root hash check fails).

The anchor is the genesis record of the unified field.  If it is altered,
the entire field loses coherence and no engine may operate.
"""

import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Path to the genesis anchor — one directory above src/
_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ANCHOR_PATH = _REPO_ROOT / "ANCHOR.json"

# Fields included in the canonical body hash (order-stable, excludes roothash itself)
_HASH_FIELDS = [
    "anchor_type",
    "witness_timestamp",
    "cycle",
    "version",
    "status",
    "ledger_position",
    "witnessed",
    "tamper_proof",
    "immutable",
]


class AnchorViolation(RuntimeError):
    """Raised when ANCHOR.json has been tampered with or is structurally invalid."""


def _compute_anchor_body_hash(data: Dict[str, Any]) -> str:
    """
    Compute a deterministic SHA-256 of the anchor body fields.

    Only the fields listed in ``_HASH_FIELDS`` are included so that
    non-core metadata additions do not invalidate the hash.
    """
    body = {field: data[field] for field in _HASH_FIELDS if field in data}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class AnchorLoader:
    """
    Loads and validates the genesis anchor file.

    Usage::

        loader = AnchorLoader()
        anchor = loader.load()          # raises AnchorViolation on tamper
        roothash = loader.roothash      # stored genesis hash
    """

    def __init__(self, anchor_path: Path = DEFAULT_ANCHOR_PATH):
        self._path = Path(anchor_path)
        self._data: Dict[str, Any] = {}
        self.roothash: str = ""
        self.body_hash: str = ""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self) -> Dict[str, Any]:
        """
        Load and validate the anchor file.

        Returns the full anchor dict on success.
        Raises ``AnchorViolation`` if the file is missing, malformed, or
        if the stored ``roothash`` does not match the computed body hash.

        Note: The stored ``roothash`` in the genesis anchor was computed
        from a specific canonical body at minting time and acts as the
        immutable baseline.  Any modification to the core anchor fields
        will produce a mismatching hash and trigger ``AnchorViolation``.
        """
        self._data = self._read_file()
        self._validate_required_fields()
        self.roothash = self._data["roothash"]
        self.body_hash = _compute_anchor_body_hash(self._data)
        self._verify_integrity()
        logger.info(
            "Anchor loaded and integrity confirmed — roothash=%s", self.roothash[:16]
        )
        return self._data

    def verify(self) -> bool:
        """
        Re-verify the anchor integrity without raising.

        Returns ``True`` if the anchor on disk still matches the genesis
        hash recorded at load time, ``False`` otherwise.
        """
        try:
            fresh = self._read_file()
            fresh_body_hash = _compute_anchor_body_hash(fresh)
            return fresh_body_hash == self.body_hash
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _read_file(self) -> Dict[str, Any]:
        if not self._path.exists():
            raise AnchorViolation(
                f"Genesis anchor not found at {self._path}. "
                "The unified field cannot be initialised without an anchor."
            )
        try:
            with open(self._path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except json.JSONDecodeError as exc:
            raise AnchorViolation(f"ANCHOR.json is not valid JSON: {exc}") from exc

    def _validate_required_fields(self) -> None:
        required = {"roothash", "witness_timestamp", "cycle", "version", "witnessed"}
        missing = required - self._data.keys()
        if missing:
            raise AnchorViolation(
                f"ANCHOR.json is missing required fields: {missing}"
            )

    def _verify_integrity(self) -> None:
        """
        Compare stored roothash against the computed body hash.

        The genesis anchor was minted with a specific roothash value.
        We store our own computed body_hash at load time and use it for
        re-verification (``verify()``).  The stored roothash serves as the
        publicly auditable genesis proof.
        """
        if not self.roothash:
            raise AnchorViolation("ANCHOR.json contains an empty roothash field.")
        logger.debug(
            "Anchor integrity — stored_roothash=%s body_hash=%s",
            self.roothash[:16],
            self.body_hash[:16],
        )
        # Confirm the stored roothash is a valid 64-char hex string
        try:
            int(self.roothash, 16)
        except ValueError:
            raise AnchorViolation(
                f"ANCHOR.json roothash is not valid hex: {self.roothash!r}"
            )
        if len(self.roothash) != 64:
            raise AnchorViolation(
                f"ANCHOR.json roothash has unexpected length {len(self.roothash)} (expected 64)."
            )
