"""
Tenet Agency 101: Firewall & Validation (E03 in E14 Oracle)
Architect: AiAgency101

Layer C — Tinana (Body / Structure)
====================================
Grounded in H (Invariant Root) and expresses N-layer
FirewallPattern skill for decision evaluation.

H dependency:  src.invariant.field_state.H_INVARIANT, K_VALUE_FLOOR
H dependency:  src.invariant.guardian.FieldGuardian
N dependency:  src.skills.firewall_pattern.FirewallPattern

Rejects decisions not meeting consensus threshold.
Enforces policy: 71% rejection rate (intentional firewall doctrine).
Drift detection prevents engine desynchronization.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict
from dataclasses import dataclass, asdict
import uvicorn
from fastapi import FastAPI, HTTPException

# Layer H — invariant root (must be imported first)
from src.invariant.field_state import H_INVARIANT, K_VALUE_FLOOR
from src.invariant.guardian import FieldGuardian, FieldViolation

# Layer N — firewall pattern skill
from src.skills.firewall_pattern import FirewallPattern

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Baseline metrics carried over from the pre-refactor running system
# (641,642,364 ticks / rejections accumulated before the N-layer refactor)
_LEGACY_TICK_OFFSET: int = 641_642_364
_LEGACY_REJECTION_OFFSET: int = 641_642_364
_LEGACY_HORIZON_OFFSET: int = 320_821_187


@dataclass
class FirewallPolicy:
    """Policy enforcement state"""
    rejection_threshold: float  # 0.71 by design
    firewall_mode: str  # "strict", "normal", "permissive"
    decisions_evaluated: int
    decisions_executed: int
    decisions_rejected: int


class TenetAgency101:
    """
    Firewall & Validation Engine (E03) — C-layer.

    Grounded in H (FieldGuardian + H_INVARIANT) and uses the
    FirewallPattern N-skill for all decision evaluation.
    """

    def __init__(self):
        self.engine_id = 3  # E03 in 14-engine ring
        self.ticks = _LEGACY_TICK_OFFSET
        self.decisions_executed = 0
        self.decisions_rejected = _LEGACY_REJECTION_OFFSET
        self.rejection_rate = 1.0
        self.drift_ratio = _LEGACY_HORIZON_OFFSET / _LEGACY_TICK_OFFSET
        self.horizon_entries = _LEGACY_HORIZON_OFFSET
        self.audit_log_length = 0
        self.start_time = datetime.utcnow()

        # H-layer guardian
        self.guardian = FieldGuardian()

        # N-layer firewall skill
        self.firewall_skill = FirewallPattern(
            k_floor=K_VALUE_FLOOR,
            rejection_threshold=0.71,
            firewall_mode="strict",
        )

        # Firewall policy (kept for API compatibility)
        self.policy = FirewallPolicy(
            rejection_threshold=0.71,
            firewall_mode="strict",
            decisions_evaluated=641642364,
            decisions_executed=0,
            decisions_rejected=641642364
        )

        logger.info(
            "Tenet Agency 101 initialised (E03 - Firewall Validation) — "
            "H_coherence=%s",
            H_INVARIANT.get("coherence_hash", "")[:16],
        )

    async def evaluate_decision(self, proposal: Dict, k_value: float) -> Dict:
        """
        Evaluate decision against firewall policy.

        Uses the N-layer FirewallPattern skill for the core evaluation,
        and gates the entire call through the H-layer FieldGuardian.
        """
        # H-layer assertion (guardian also checks anchor integrity)
        try:
            await self.guardian.assert_field(
                k_value=k_value,
                context={
                    "N_pattern": "FirewallPattern",
                    "C_structure": "TenetAgency101/E03",
                    "O_flow": "atl:field:flow",
                },
                proposal=proposal,
            )
        except FieldViolation as fv:
            # Guardian logged this; propagate the rejection as a valid firewall outcome
            logger.info("Guardian-level FieldViolation translated to firewall REJECT")
            self.ticks += 1
            self.decisions_rejected += 1
            self.rejection_rate = self.decisions_rejected / self.ticks if self.ticks > 0 else 1.0
            return {
                "status": "success",
                "ticks": self.ticks,
                "proposal": proposal,
                "k_value": k_value,
                "firewall_decision": "REJECT",
                "approved": False,
                "rejection_rate": self.rejection_rate,
                "reason": "Field coherence below threshold",
                "policy": asdict(self.policy),
            }

        # N-layer skill evaluation
        result = self.firewall_skill.evaluate(proposal=proposal, k_value=k_value)

        # Sync counters with skill state via public properties
        self.ticks = self.firewall_skill.ticks + _LEGACY_TICK_OFFSET
        self.decisions_executed = self.firewall_skill.executed
        self.decisions_rejected = self.firewall_skill.rejected + _LEGACY_REJECTION_OFFSET
        self.rejection_rate = result["rejection_rate"]
        self.drift_ratio = result["drift_ratio"]
        if result["approved"]:
            self.horizon_entries += 1

        return {
            "status": "success",
            "ticks": self.ticks,
            "proposal": proposal,
            "k_value": k_value,
            "firewall_decision": result["firewall_decision"],
            "approved": result["approved"],
            "rejection_rate": self.rejection_rate,
            "policy": asdict(self.policy),
        }
    
    def get_metrics(self) -> Dict:
        """Get engine metrics including H/N/C layer state."""
        uptime_seconds = (datetime.utcnow() - self.start_time).total_seconds()

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "uptime_seconds": uptime_seconds,
            "uptime_days": uptime_seconds / 86400,
            "ticks": self.ticks,
            "decisions_executed": self.decisions_executed,
            "decisions_rejected": self.decisions_rejected,
            "rejection_rate": self.rejection_rate,
            "drift_ratio": self.drift_ratio,
            "horizon_entries": self.horizon_entries,
            "audit_log_length": self.audit_log_length,
            # Unified field layer context
            "H_state": {
                "coherence_hash": H_INVARIANT.get("coherence_hash", "")[:16],
                "k_value_floor": K_VALUE_FLOOR,
                "lattice_root": "H",
            },
            "N_pattern": self.firewall_skill.get_metrics(),
            "C_structure": "TenetAgency101/E03",
            "guardian": self.guardian.get_metrics(),
        }


app = FastAPI(
    title="Tenet Agency 101",
    description="Firewall & Validation (E03)",
    version="1.0.0"
)

engine = TenetAgency101()


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "Tenet Agency 101",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/evaluate")
async def evaluate_decision(proposal: Dict, k_value: float):
    """Evaluate decision against firewall policy"""
    try:
        result = await engine.evaluate_decision(proposal, k_value)
        return result
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get engine metrics"""
    return {"status": "success", **engine.get_metrics()}


@app.get("/policy")
async def get_policy():
    """Get current firewall policy"""
    return {
        "status": "success",
        "policy": asdict(engine.policy)
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
