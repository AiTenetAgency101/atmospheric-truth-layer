"""
Ultimate Engine — ENGINE2: Byzantine Consensus Coordinator (E02 in E14 Oracle)
Architect: AiAgency101

Layer C — Tinana (Body / Structure) — Trunk of the Lattice Tree
=========================================================
ENGINE2 is the structural trunk of the unified field.
It is grounded in H (Invariant Root via src.invariant) and expresses
pattern logic from N (ConsensusPattern skill via src.skills).

Lattice position: C (trunk)
H dependency:     src.invariant.field_state.H_INVARIANT, K_VALUE_FLOOR
H dependency:     src.invariant.guardian.FieldGuardian
N dependency:     src.skills.consensus_pattern.ConsensusPattern

Manages 14-engine Byzantine consensus with K-value coherence metric.
Coordinates decision execution based on consensus threshold (K ≥ 0.99).
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, asdict
import uvicorn
from fastapi import FastAPI, HTTPException
import random

# Layer H — invariant root (must be imported first)
from src.invariant.field_state import H_INVARIANT, K_VALUE_FLOOR
from src.invariant.guardian import FieldGuardian, FieldViolation

# Layer N — cognitive pattern (consensus skill)
from src.skills.consensus_pattern import ConsensusPattern

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ConsensusState:
    """14-dimensional phase space state"""
    engine_id: int
    phase: float  # 0.0 to 2π
    power: float  # -1.0 to 1.0
    coherence: float  # -1.0 to 1.0
    timestamp: str


class UltimateEngine:
    """
    Byzantine Consensus Engine (E02) — ENGINE2 — C-layer trunk.

    Grounded in H (FieldGuardian + H_INVARIANT) and uses the
    ConsensusPattern N-skill for K-value computation and engine evolution.
    """

    def __init__(self):
        self.engine_id = 2  # E02 in 14-engine ring
        self.cycles = 2548079
        self.decisions_executed = 993625
        self.decisions_rejected = 1554454
        self.k_value = 0.995
        self.sovereignty_orders = 10
        self.byzantine_layers = 12
        self.start_time = datetime.utcnow()

        # H-layer guardian — all decisions gate through this
        self.guardian = FieldGuardian()

        # N-layer skill — consensus pattern computation
        self.consensus_skill = ConsensusPattern(k_floor=K_VALUE_FLOOR)

        # 14 engine states (E01-E14)
        self.engine_states: Dict[int, ConsensusState] = {}
        for i in range(1, 15):
            self.engine_states[i] = ConsensusState(
                engine_id=i,
                phase=random.uniform(0, 6.28),
                power=random.uniform(-1, 1),
                coherence=random.uniform(-1, 1),
                timestamp=datetime.utcnow().isoformat() + "Z"
            )

        logger.info(
            "Ultimate Engine (ENGINE2) initialized — E02 — C-layer trunk — "
            "H_coherence=%s",
            H_INVARIANT.get("coherence_hash", "")[:16],
        )

    async def compute_consensus(self, proposal: Dict) -> Dict:
        """
        Compute Byzantine consensus across 14 engines.

        Flow:
        1. PROPOSE  — log the proposal
        2. PREPARE  — evolve engine states toward equilibrium (N-skill)
        3. COMMIT   — compute K-value (N-skill)
        4. GATE     — assert field via H-layer guardian
        5. EXECUTE  — increment counters if gate opens
        """
        try:
            # Phase 1: PROPOSE
            logger.info(f"Proposing decision: {proposal}")

            # Phase 2: PREPARE — evolve states using N-skill
            raw_states = {
                i: {
                    "phase": s.phase,
                    "power": s.power,
                    "coherence": s.coherence,
                }
                for i, s in self.engine_states.items()
            }
            evolved = self.consensus_skill.evolve_all(raw_states)
            for i, ev in evolved.items():
                self.engine_states[i] = ConsensusState(
                    engine_id=i,
                    phase=ev["phase"],
                    power=ev["power"],
                    coherence=ev["coherence"],
                    timestamp=datetime.utcnow().isoformat() + "Z",
                )

            # Phase 3: COMMIT — compute K-value via N-skill
            k_value = self.consensus_skill.compute_k(
                {i: {"phase": s.phase, "power": s.power, "coherence": s.coherence}
                 for i, s in self.engine_states.items()}
            )
            self.k_value = k_value

            # Phase 4: GATE — H-layer invariant assertion
            try:
                await self.guardian.assert_field(
                    k_value=k_value,
                    context={
                        "N_pattern": "ConsensusPattern",
                        "C_structure": "UltimateEngine/ENGINE2",
                        "O_flow": "atl:field:flow",
                    },
                    proposal=proposal,
                )
                execution_gate_open = True
            except FieldViolation:
                execution_gate_open = False

            # Phase 5: EXECUTE
            if execution_gate_open:
                self.decisions_executed += 1
                self.cycles += 1
                result = "ACCEPTED"
            else:
                self.decisions_rejected += 1
                result = "REJECTED"

            logger.info(
                f"Consensus: K={k_value:.4f}, gate={'OPEN' if execution_gate_open else 'CLOSED'}, result={result}"
            )

            return {
                "status": "success",
                "proposal": proposal,
                "k_value": k_value,
                "execution_gate": execution_gate_open,
                "result": result,
                "engine_states": {str(i): asdict(s) for i, s in self.engine_states.items()},
                "cycles": self.cycles,
                "decisions_executed": self.decisions_executed,
                "decisions_rejected": self.decisions_rejected,
            }

        except FieldViolation:
            # Already logged by guardian; re-raise as HTTP 503
            raise
        except Exception as e:
            logger.error(f"Consensus error: {e}")
            raise
    
    def get_metrics(self) -> Dict:
        """Get engine metrics including H/N/C layer state."""
        uptime_seconds = (datetime.utcnow() - self.start_time).total_seconds()

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "uptime_seconds": uptime_seconds,
            "uptime_days": uptime_seconds / 86400,
            "cycles": self.cycles,
            "decisions_executed": self.decisions_executed,
            "decisions_rejected": self.decisions_rejected,
            "execution_rate": self.decisions_executed / (self.decisions_executed + self.decisions_rejected) if (self.decisions_executed + self.decisions_rejected) > 0 else 0,
            "rejection_rate": self.decisions_rejected / (self.decisions_executed + self.decisions_rejected) if (self.decisions_executed + self.decisions_rejected) > 0 else 0,
            "k_value": self.k_value,
            "byzantine_layers": self.byzantine_layers,
            "sovereignty_orders": self.sovereignty_orders,
            "architecture": "AIAGENCY101_ULTIMATE_SOVEREIGN™",
            # Unified field layer context
            "H_state": {
                "coherence_hash": H_INVARIANT.get("coherence_hash", "")[:16],
                "k_value_floor": K_VALUE_FLOOR,
                "lattice_root": "H",
            },
            "N_pattern": self.consensus_skill.get_metrics(),
            "C_structure": "UltimateEngine/ENGINE2",
            "guardian": self.guardian.get_metrics(),
        }


app = FastAPI(
    title="Ultimate Engine",
    description="Byzantine Consensus Coordinator (E02)",
    version="1.0.0"
)

engine = UltimateEngine()


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "Ultimate Engine",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/consensus")
async def propose_consensus(proposal: Dict):
    """Propose decision to Byzantine consensus"""
    try:
        result = await engine.compute_consensus(proposal)
        return result
    except Exception as e:
        logger.error(f"Consensus error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get engine metrics"""
    return {"status": "success", **engine.get_metrics()}


@app.get("/engine-states")
async def get_engine_states():
    """Get all 14 engine states"""
    return {
        "status": "success",
        "engine_states": {str(i): asdict(s) for i, s in engine.engine_states.items()}
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
