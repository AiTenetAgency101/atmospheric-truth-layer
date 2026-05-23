"""
Layer O — Propagator (Mauri / Life Force / Flow)

Broadcasts K-value and lattice state to registered downstream consumers
via webhook callbacks and the Redis ``atl:field:flow`` pub/sub channel.

The Propagator subscribes to the Redis channel and re-broadcasts to all
registered webhooks, making O the living sap of the lattice tree.
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import httpx

from src.invariant.field_state import H_INVARIANT, K_VALUE_FLOOR
from src.witness.field_sync import FIELD_FLOW_CHANNEL

logger = logging.getLogger(__name__)


class Propagator:
    """
    O-layer propagator — subscribes to the field-flow channel and
    re-broadcasts to all registered downstream webhooks.

    Usage::

        propagator = Propagator(redis_client=redis)
        propagator.register_webhook("https://example.com/hook")
        asyncio.create_task(propagator.run())   # background task

    Without Redis the propagator can still be used to manually broadcast
    via ``await propagator.broadcast(entry)``.
    """

    def __init__(self, redis_client=None) -> None:
        self._redis = redis_client
        self._webhooks: List[str] = []
        self._broadcast_log: List[Dict[str, Any]] = []
        self._running: bool = False

    # ------------------------------------------------------------------
    # Webhook registration
    # ------------------------------------------------------------------

    def register_webhook(self, url: str) -> None:
        """Register a downstream webhook URL."""
        if url not in self._webhooks:
            self._webhooks.append(url)
            logger.info("Propagator: registered webhook %s", url)

    def unregister_webhook(self, url: str) -> None:
        """Unregister a webhook URL."""
        self._webhooks = [w for w in self._webhooks if w != url]

    # ------------------------------------------------------------------
    # Redis subscription loop
    # ------------------------------------------------------------------

    async def run(self) -> None:
        """
        Subscribe to the Redis ``atl:field:flow`` channel and broadcast
        every received entry to all registered webhooks.

        No-op if Redis is unavailable.
        """
        if self._redis is None:
            logger.info("Propagator: no Redis client — subscription loop idle")
            return

        self._running = True
        logger.info(
            "Propagator: subscribing to Redis channel %s", FIELD_FLOW_CHANNEL
        )
        try:
            pubsub = self._redis.pubsub()
            await pubsub.subscribe(FIELD_FLOW_CHANNEL)
            async for message in pubsub.listen():
                if not self._running:
                    break
                if message.get("type") == "message":
                    try:
                        entry = json.loads(message["data"])
                        await self.broadcast(entry)
                    except Exception as exc:
                        logger.warning("Propagator: failed to parse message: %s", exc)
        except Exception as exc:
            logger.error("Propagator: subscription error: %s", exc)
        finally:
            self._running = False

    def stop(self) -> None:
        """Signal the subscription loop to stop."""
        self._running = False

    # ------------------------------------------------------------------
    # Manual broadcast
    # ------------------------------------------------------------------

    async def broadcast(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Broadcast a field-flow entry to all registered webhooks.

        Returns a broadcast summary dict.
        """
        timestamp = datetime.utcnow().isoformat() + "Z"
        results: Dict[str, Any] = {}

        async with httpx.AsyncClient(timeout=5.0) as client:
            for url in list(self._webhooks):
                try:
                    resp = await client.post(url, json=entry)
                    results[url] = {
                        "status": "delivered",
                        "response_code": resp.status_code,
                    }
                    logger.debug("Propagator: delivered to %s (%d)", url, resp.status_code)
                except Exception as exc:
                    results[url] = {"status": "failed", "error": str(exc)}
                    logger.warning("Propagator: delivery to %s failed: %s", url, exc)

        summary = {
            "timestamp": timestamp,
            "entry_hash": entry.get("entry_hash", ""),
            "webhooks_attempted": len(self._webhooks),
            "results": results,
            "H_state": H_INVARIANT.get("coherence_hash", "")[:16],
            "O_flow": FIELD_FLOW_CHANNEL,
        }
        self._broadcast_log.append(summary)
        return summary

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Return propagator status including recent broadcast log."""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "running": self._running,
            "registered_webhooks": len(self._webhooks),
            "broadcasts_sent": len(self._broadcast_log),
            "recent_broadcasts": self._broadcast_log[-10:],
            "channel": FIELD_FLOW_CHANNEL,
            "O_flow": FIELD_FLOW_CHANNEL,
        }
