"""
Layer N — Hash Fabric Module (Hinengaro / Mind / Pattern)

Composable SHA-256 / HMAC-SHA-256 tile hashing used by all engines.

All tile hashing MUST go through this module to ensure consistency
across the engine ring.
"""

import hashlib
import hmac
import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Default HMAC key — override via HMAC_SECRET environment variable in production
import os

_DEFAULT_HMAC_KEY = b"atl-default-hmac-key-change-in-production"
_hmac_secret = os.environ.get("HMAC_SECRET", "")
_HMAC_KEY = _hmac_secret.encode("utf-8") if _hmac_secret else _DEFAULT_HMAC_KEY


class HashFabric:
    """
    Composable tile hashing module.

    Produces:
    - ``pixel_hash``     — SHA-256 of raw pixel data
    - ``metadata_hash``  — SHA-256 of canonical JSON metadata
    - ``integrity_hash`` — SHA-256 of (pixel_hash + metadata_hash)
    - ``witness_sig``    — HMAC-SHA-256 of integrity_hash

    Usage::

        fabric = HashFabric()
        result = fabric.hash_tile(
            pixel_data="<raw bytes string>",
            metadata={"satellite": "BOM", "region": "SouthPacific", ...},
        )
        # result["integrity_hash"] is the tile's cryptographic fingerprint
    """

    def hash_pixels(self, pixel_data: str) -> str:
        """SHA-256 of raw pixel data string."""
        return hashlib.sha256(pixel_data.encode("utf-8")).hexdigest()

    def hash_metadata(self, metadata: Dict[str, Any]) -> str:
        """SHA-256 of canonical (sorted-key) JSON metadata."""
        canonical = json.dumps(metadata, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def hash_integrity(self, pixel_hash: str, metadata_hash: str) -> str:
        """SHA-256 of the concatenation of pixel_hash and metadata_hash."""
        combined = pixel_hash + metadata_hash
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def sign_witness(self, integrity_hash: str) -> str:
        """HMAC-SHA-256 witness signature over the integrity hash."""
        sig = hmac.new(_HMAC_KEY, integrity_hash.encode("utf-8"), hashlib.sha256)
        return sig.hexdigest()

    def hash_tile(
        self,
        pixel_data: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        Compute all four hashes for a tile in one call.

        Returns::

            {
                "pixel_hash":     "<sha256>",
                "metadata_hash":  "<sha256>",
                "integrity_hash": "<sha256>",
                "witness_sig":    "<hmac-sha256>",
            }
        """
        pixel_hash = self.hash_pixels(pixel_data)
        metadata_hash = self.hash_metadata(metadata)
        integrity_hash = self.hash_integrity(pixel_hash, metadata_hash)
        witness_sig = self.sign_witness(integrity_hash)

        logger.debug(
            "HashFabric: pixel=%s metadata=%s integrity=%s",
            pixel_hash[:8],
            metadata_hash[:8],
            integrity_hash[:8],
        )
        return {
            "pixel_hash": pixel_hash,
            "metadata_hash": metadata_hash,
            "integrity_hash": integrity_hash,
            "witness_sig": witness_sig,
        }

    @staticmethod
    def verify_integrity(
        pixel_hash: str, metadata_hash: str, claimed_integrity: str
    ) -> bool:
        """
        Re-derive the integrity hash and compare to the claimed value.

        Returns True if the tile has not been tampered with.
        """
        expected = hashlib.sha256(
            (pixel_hash + metadata_hash).encode("utf-8")
        ).hexdigest()
        return expected == claimed_integrity
