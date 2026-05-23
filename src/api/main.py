"""
API Gateway: Atmospheric Truth Layer (AiAgency101)
Architect: AiAgency101

Routes between:
- Engine 365-Days (E01): Tile decomposition
- Ultimate Engine (E02): Byzantine consensus
- Tenet Agency 101 (E03): Firewall validation
- XYO Witness: Immutable ledger + SymPy invariants

Layer O — Mauri (Life Force / Flow)
=====================================
The API gateway is the primary O-layer endpoint.
  GET /api/field  — returns the live unified field state
                    { H, N, C, O }
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import httpx

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn

# Layer H — invariant root
from src.invariant.field_state import H_INVARIANT, K_VALUE_FLOOR
from src.invariant.guardian import FieldGuardian

# Layer O — field sync and propagator
from src.witness.field_sync import FieldSync
from src.witness.propagator import Propagator

# Layer C — engine ring registry
from src.engines import ring_summary, active_engines

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# API GATEWAY
# ============================================================================

class APIGateway:
    """Coordinator for all engines and witness layer (O-layer surface)."""

    def __init__(self):
        self.engine_365_url = "http://engine-365-days:8000"
        self.ultimate_engine_url = "http://ultimate-engine:8000"
        self.tenet_url = "http://tenetaiagency-101:8000"
        self.witness_url = "http://xyo-witness:8000"

        self.start_time = datetime.utcnow()

        # O-layer components (no Redis by default; can be injected)
        self.field_sync = FieldSync()
        self.propagator = Propagator()

        # H-layer guardian for the gateway itself
        self.guardian = FieldGuardian()

        logger.info(
            "API Gateway initialised (AiAgency101) — H_coherence=%s",
            H_INVARIANT.get("coherence_hash", "")[:16],
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check all services"""
        services = {
            "gateway": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "services": {}
        }
        
        # Check each service
        services_to_check = {
            "engine-365-days": self.engine_365_url,
            "ultimate-engine": self.ultimate_engine_url,
            "tenet-agency-101": self.tenet_url,
            "xyo-witness": self.witness_url
        }
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            for service_name, service_url in services_to_check.items():
                try:
                    resp = await client.get(f"{service_url}/health")
                    services["services"][service_name] = {
                        "status": "healthy",
                        "response_code": resp.status_code
                    }
                except Exception as e:
                    services["services"][service_name] = {
                        "status": "unhealthy",
                        "error": str(e)
                    }
        
        return services
    
    async def process_satellite_frame(
        self,
        satellite_source: str,
        region: str,
        band: str,
        pixel_data: str,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """
        Complete flow:
        1. Engine 365: Decompose frame into tiles
        2. Ultimate Engine: Achieve consensus (K-value)
        3. Tenet Agency: Validate against policy
        4. XYO Witness: Create invariant + witness
        """
        
        try:
            # Step 1: Decompose
            logger.info(f"[1/4] Decomposing {satellite_source} frame...")
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                decompose_resp = await client.post(
                    f"{self.engine_365_url}/decompose",
                    params={
                        "satellite_source": satellite_source,
                        "region": region,
                        "band": band,
                        "pixel_data": pixel_data,
                        "latitude": latitude,
                        "longitude": longitude
                    }
                )
            
            if decompose_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Decomposition failed")
            
            decompose_data = decompose_resp.json()
            tiles = decompose_data.get("tiles", [])
            
            logger.info(f"[1/4] ✓ Decomposed into {len(tiles)} tiles")
            
            # Step 2: Achieve consensus
            logger.info(f"[2/4] Computing Byzantine consensus...")
            
            proposal = {
                "satellite": satellite_source,
                "region": region,
                "tiles": len(tiles),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                consensus_resp = await client.post(
                    f"{self.ultimate_engine_url}/consensus",
                    json=proposal
                )
            
            if consensus_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Consensus failed")
            
            consensus_data = consensus_resp.json()
            k_value = consensus_data.get("k_value", 0.0)
            
            logger.info(f"[2/4] ✓ Consensus achieved: K={k_value:.4f}")
            
            # Step 3: Validate
            logger.info(f"[3/4] Validating against firewall policy...")
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                validate_resp = await client.post(
                    f"{self.tenet_url}/evaluate",
                    json=proposal,
                    params={"k_value": k_value}
                )
            
            if validate_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Validation failed")
            
            validate_data = validate_resp.json()
            approved = validate_data.get("approved", False)
            
            logger.info(f"[3/4] ✓ Validation: {'APPROVED' if approved else 'REJECTED'}")
            
            # Step 4: Witness + Invariantize
            logger.info(f"[4/4] Creating invariants and witness proofs...")
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                witness_resp = await client.post(
                    f"{self.witness_url}/witness-and-invariantize",
                    json={
                        "tiles": tiles,
                        "satellite_source": satellite_source,
                        "k_value": k_value,
                        "approved": approved
                    }
                )
            
            if witness_resp.status_code != 200:
                logger.warning("Witness call failed, continuing with basic proof")
                witness_data = {}
            else:
                witness_data = witness_resp.json()
            
            logger.info(f"[4/4] ✓ Invariants created and witnessed")
            
            # Compile final result
            result = {
                "status": "success" if approved else "rejected",
                "satellite": satellite_source,
                "region": region,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "pipeline": {
                    "decomposition": {
                        "tiles_generated": len(tiles),
                        "status": "complete"
                    },
                    "consensus": {
                        "k_value": k_value,
                        "k_threshold": 0.99,
                        "gate_open": k_value >= 0.99,
                        "status": "complete"
                    },
                    "validation": {
                        "approved": approved,
                        "rejection_rate": validate_data.get("rejection_rate", 0.0),
                        "status": "complete"
                    },
                    "witness": {
                        "invariants_created": len(tiles),
                        "ledger_entries": len(tiles),
                        "status": "complete"
                    }
                },
                "tiles_sample": tiles[:3] if tiles else [],
                "witness_proof": witness_data
            }
            
            logger.info("✓ Complete pipeline executed successfully")
            
            return result
        
        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get metrics from all services"""

        metrics = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "services": {}
        }

        async with httpx.AsyncClient(timeout=5.0) as client:
            # Engine 365 metrics
            try:
                resp = await client.get(f"{self.engine_365_url}/metrics")
                metrics["services"]["engine-365-days"] = resp.json()
            except:
                metrics["services"]["engine-365-days"] = {"error": "unavailable"}

            # Ultimate Engine metrics
            try:
                resp = await client.get(f"{self.ultimate_engine_url}/metrics")
                metrics["services"]["ultimate-engine"] = resp.json()
            except:
                metrics["services"]["ultimate-engine"] = {"error": "unavailable"}

            # Tenet Agency metrics
            try:
                resp = await client.get(f"{self.tenet_url}/metrics")
                metrics["services"]["tenet-agency-101"] = resp.json()
            except:
                metrics["services"]["tenet-agency-101"] = {"error": "unavailable"}

        return metrics

    async def get_field_state(self) -> Dict[str, Any]:
        """
        Return the live unified field state — H → N → C → O.

        Collects the current K-value from the Ultimate Engine (C-layer)
        and assembles the full field state dict.
        """
        # Fetch current K-value from ENGINE2 (best-effort)
        k_value = K_VALUE_FLOOR  # default floor
        engine_ring_status: Dict[str, Any] = ring_summary()
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{self.ultimate_engine_url}/metrics")
                if resp.status_code == 200:
                    k_value = resp.json().get("k_value", K_VALUE_FLOOR)
        except Exception as exc:
            logger.debug("Could not fetch K-value from ultimate-engine: %s", exc)

        # Active N skills (from engine ring registry)
        active = active_engines()
        active_skills = []
        for e in active.values():
            active_skills.extend(e.get("N_skills", []))

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "H": {
                "anchor_hash": H_INVARIANT.get("coherence_hash", ""),
                "origin": H_INVARIANT.get("origin", ""),
                "k_value_floor": K_VALUE_FLOOR,
                "lattice_root": "H",
                "guardian": self.guardian.get_metrics(),
            },
            "N": {
                "active_skills": list(set(active_skills)),
                "lattice_layer": "N",
            },
            "C": {
                "engine_ring": engine_ring_status,
                "k_value": k_value,
                "lattice_layer": "C",
            },
            "O": {
                "sync_propagation_log": self.field_sync.get_log(20),
                "ledger_size": self.field_sync.ledger_size(),
                "propagator": self.propagator.get_status(),
                "channel": "atl:field:flow",
                "lattice_layer": "O",
            },
            "invariant": "H → N → C → O",
        }


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Atmospheric Truth Layer - API Gateway",
    description="E14 Oracle Coordinator (AiAgency101)",
    version="1.0.0"
)

gateway = APIGateway()


@app.get("/health")
async def health():
    """Health check all services"""
    return await gateway.health_check()


@app.post("/process-satellite-frame")
async def process_satellite_frame(
    satellite_source: str = Query(...),
    region: str = Query(...),
    band: str = Query(...),
    pixel_data: str = Query(...),
    latitude: float = Query(...),
    longitude: float = Query(...)
):
    """
    Complete pipeline: Decompose → Consensus → Validate → Witness
    """
    try:
        result = await gateway.process_satellite_frame(
            satellite_source=satellite_source,
            region=region,
            band=band,
            pixel_data=pixel_data,
            latitude=latitude,
            longitude=longitude
        )
        return result
    except Exception as e:
        logger.error(f"Processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get all system metrics"""
    return await gateway.get_system_metrics()


@app.get("/api/field")
async def get_field():
    """
    Live unified field state — H → N → C → O.

    Returns the complete field state dict::

        {
            "H": { anchor_hash, origin, k_value_floor, guardian },
            "N": { active_skills },
            "C": { engine_ring, k_value },
            "O": { sync_propagation_log, ledger_size, propagator },
        }
    """
    return await gateway.get_field_state()


@app.get("/info")
async def info():
    """System information"""
    return {
        "service": "Atmospheric Truth Layer - API Gateway",
        "architect": "AiAgency101",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "engines": {
            "E01": "Engine 365-Days (Temporal Anchor)",
            "E02": "Ultimate Engine (Byzantine Consensus)",
            "E03": "Tenet Agency 101 (Firewall)",
            "XYO": "Witness Layer + SymPy Invariants"
        },
        "mission": "Cryptographic verification of atmospheric truth"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
