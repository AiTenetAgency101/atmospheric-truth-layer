from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")


class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StatusCheckCreate(BaseModel):
    client_name: str


# ============================================================================
# Atmospheric Truth Layer — Genesis data endpoints
# ============================================================================

GENESIS_TIMESTAMP = "2026-04-23T07:53:50.5144990+10:00"

MINTING_CERTIFICATE: Dict[str, Any] = {
    "version": "v1.0.0-minted",
    "minted_timestamp": GENESIS_TIMESTAMP,
    "timezone_offset": "+10:00 (Australian Eastern Standard Time)",
    "ledger_position": 0,
    "entry_type": "genesis_minting",
    "cryptographic_hash": "e14f9a8d2c7b5e3f1a9d4c8b2e6f7a3d",
    "tsa_signature": "f7e3b2c1d4a9e5f8b2c6d1a7e3f9b4c2",
    "lock_id": "7f4a9e2c-8d3b-47e1-9f6c-2a5d8e1b4f7a",
    "status": "PRODUCTION_READY",
    "immutable": True,
    "tamper_evident": True,
    "engines": {
        "engine_365_days": {
            "name": "Engine 365-Days",
            "subtitle": "Decomposition Validator",
            "cycles": 37445846,
            "tiles_verified": 3510223,
            "tiles_rejected": 8593985,
            "validator_health": 1.0,
            "validators": {"circle": 1.0, "monotonic": 1.0, "range": 1.0},
            "consensus": "3/3",
            "status": "HEALTHY",
        },
        "ultimate_engine": {
            "name": "Ultimate Engine",
            "subtitle": "Byzantine Consensus",
            "cycles": 2548079,
            "decisions_executed": 993625,
            "decisions_rejected": 1554454,
            "sovereignty_orders": 10,
            "byzantine_layers": 12,
            "k_value": 0.995,
            "status": "HEALTHY",
        },
        "tenet_agency_101": {
            "name": "Tenet Agency 101",
            "subtitle": "Firewall Doctrine",
            "ticks": 641642364,
            "decisions_rejected": 641642364,
            "drift_ratio": "1:2",
            "horizon_entries": 320821187,
            "status": "HEALTHY",
        },
        "witness_ledger": {
            "name": "Witness Ledger",
            "subtitle": "XYO Bound-Witness",
            "witnessed_tiles": 37000000,
            "multi_satellite": True,
            "rfc3161": True,
            "status": "ACTIVE",
        },
    },
    "witnesses": [
        {
            "code": "BOM",
            "name": "Bureau of Meteorology",
            "region": "Australia",
            "node": "witness-bom-australia",
            "signature": "7f3e2b1a4d9c6f2e5b8a1d7c4f9e2b6a",
            "observation": GENESIS_TIMESTAMP,
            "verified": True,
        },
        {
            "code": "HIMAWARI-8",
            "name": "Himawari-8",
            "region": "Japan",
            "node": "witness-himawari-japan",
            "signature": "8g4f3c2b5e0d7g3f6c9b2e8d5g0f3c7b",
            "observation": GENESIS_TIMESTAMP,
            "verified": True,
        },
        {
            "code": "GOES-16",
            "name": "GOES-16",
            "region": "USA",
            "node": "witness-goes-usa",
            "signature": "9h5g4d3c6f1e8h4g7d0c3f9e6h1g4d8c",
            "observation": GENESIS_TIMESTAMP,
            "verified": True,
        },
        {
            "code": "METEOSAT",
            "name": "Meteosat",
            "region": "Europe",
            "node": "witness-meteosat-europe",
            "signature": "0i6h5e4d7g2f9i5h8e1d4g0i5h2i5e9d",
            "observation": GENESIS_TIMESTAMP,
            "verified": True,
        },
    ],
    "wobble_constants": {"SUU": 0.05, "AHA": 0.075, "RERE": 0.15},
    "series_a": {
        "funding_ask_usd": 2500000,
        "post_money_valuation_usd": 12500000,
        "year_1_revenue_usd": 3180000,
        "year_2_revenue_usd": 26350000,
        "year_3_revenue_usd": 55100000,
        "market_tam_usd": 155000000000,
        "exit_range_usd": "300M - 500M",
        "status": "READY_TO_LAUNCH",
    },
    "tagline": "The sky doesn't lie. Satellites don't sleep. Math doesn't break.",
}


@api_router.get("/")
async def root():
    return {"message": "Atmospheric Truth Layer :: Genesis online"}


@api_router.get("/minting-certificate")
async def minting_certificate():
    return MINTING_CERTIFICATE


@api_router.get("/system-state")
async def system_state():
    """Live system state — cycles increment since genesis to simulate a running ledger."""
    genesis = datetime.fromisoformat(GENESIS_TIMESTAMP)
    elapsed = (datetime.now(timezone.utc) - genesis.astimezone(timezone.utc)).total_seconds()
    # post-minting drift: engines keep ticking
    return {
        "server_time": datetime.now(timezone.utc).isoformat(),
        "seconds_since_genesis": int(elapsed),
        "engine_365_cycles": 37445846 + int(elapsed * 3.2),
        "ultimate_cycles": 2548079 + int(elapsed * 0.22),
        "tenet_ticks": 641642364 + int(elapsed * 54.7),
        "witnessed_tiles": 37000000 + int(elapsed * 2.6),
        "k_value": 0.995,
        "consensus": "3/3",
        "uptime": "CONTINUOUS",
    }


@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(payload: StatusCheckCreate):
    status_obj = StatusCheck(**payload.model_dump())
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    await db.status_checks.insert_one(doc)
    return status_obj


@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    return status_checks


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
