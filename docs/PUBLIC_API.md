# PUBLIC_API.md — Atmospheric Truth Layer

Public, read-only API endpoints for querying the Genesis Ledger and live system state. All responses are JSON.

**Base URL (preview):** `https://<your-atl-deployment>.preview.emergentagent.com/api`
**Base URL (production):** `https://api.atmospheric-truth.io/api` *(reserved)*

---

## Endpoints

### `GET /api/minting-certificate`
Returns the immutable Genesis minting payload — timestamp, engines, witnesses, series-A metadata, RFC3161 authority, GitHub repo, roadmap, hardware layer.

**Response shape (abbreviated):**
```json
{
  "version": "v1.0.0-minted",
  "minted_timestamp": "2026-04-23T07:53:50.5144990+10:00",
  "cryptographic_hash": "e14f9a8d2c7b5e3f1a9d4c8b2e6f7a3d",
  "tsa_signature": "f7e3b2c1d4a9e5f8b2c6d1a7e3f9b4c2",
  "engines": { "engine_365_days": { ... }, "ultimate_engine": { ... }, ... },
  "witnesses": [ { "code": "BOM", ... }, ... ],
  "series_a": { ... },
  "hardware": { "name": "espVmark", "board": "ESP32-C6", ... },
  "tagline": "The sky doesn't lie. Satellites don't sleep. Math doesn't break."
}
```

### `GET /api/system-state`
Live, monotonically-increasing telemetry since genesis. Poll at any rate; server derives all counters from `now() − genesis`.

**Response:**
```json
{
  "server_time": "2026-07-16T09:54:10.221Z",
  "seconds_since_genesis": 7057220,
  "engine_365_cycles": 60028550,
  "ultimate_cycles": 4100668,
  "tenet_ticks": 1027683878,
  "witnessed_tiles": 55348772,
  "k_value": 0.995,
  "consensus": "3/3",
  "uptime": "CONTINUOUS"
}
```

### `POST /api/chat`
Query the Genesis Engine (Gemini 3 Flash, grounded in ATL system prompt). Multi-turn via `session_id`.

**Request:**
```json
{ "session_id": "your-uuid", "message": "How do I verify a witness signature?" }
```

**Response:**
```json
{ "reply": "Witness signatures are anchored to the RFC3161 timestamp authority ..." }
```

---

## SDK Examples

### TypeScript

```typescript
// atl-client.ts — Atmospheric Truth Layer minimal client
export interface SystemState {
    server_time: string;
    seconds_since_genesis: number;
    engine_365_cycles: number;
    ultimate_cycles: number;
    tenet_ticks: number;
    witnessed_tiles: number;
    k_value: number;
    consensus: string;
    uptime: string;
}

export class AtlClient {
    constructor(private baseUrl: string) {}

    async getGenesisCertificate(): Promise<Record<string, unknown>> {
        const res = await fetch(`${this.baseUrl}/api/minting-certificate`);
        if (!res.ok) throw new Error(`ATL cert error ${res.status}`);
        return res.json();
    }

    async getSystemState(): Promise<SystemState> {
        const res = await fetch(`${this.baseUrl}/api/system-state`);
        if (!res.ok) throw new Error(`ATL state error ${res.status}`);
        return res.json() as Promise<SystemState>;
    }

    async askGenesis(sessionId: string, message: string): Promise<string> {
        const res = await fetch(`${this.baseUrl}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, message }),
        });
        const data = await res.json();
        return data.reply;
    }
}

// --- Usage ---
const atl = new AtlClient("https://api.atmospheric-truth.io");
const cert = await atl.getGenesisCertificate();
console.log("Ledger position:", cert.ledger_position);

const state = await atl.getSystemState();
console.log(`Witnessed tiles: ${state.witnessed_tiles.toLocaleString()}`);

const answer = await atl.askGenesis(crypto.randomUUID(),
    "What guarantees data integrity across all 4 satellites?");
console.log(answer);
```

### Python

```python
# atl_client.py — Atmospheric Truth Layer minimal client
import uuid
import requests
from dataclasses import dataclass


@dataclass
class SystemState:
    server_time: str
    seconds_since_genesis: int
    engine_365_cycles: int
    ultimate_cycles: int
    tenet_ticks: int
    witnessed_tiles: int
    k_value: float
    consensus: str
    uptime: str


class AtlClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def genesis_certificate(self) -> dict:
        r = requests.get(f"{self.base_url}/api/minting-certificate", timeout=15)
        r.raise_for_status()
        return r.json()

    def system_state(self) -> SystemState:
        r = requests.get(f"{self.base_url}/api/system-state", timeout=15)
        r.raise_for_status()
        return SystemState(**r.json())

    def ask_genesis(self, session_id: str, message: str) -> str:
        r = requests.post(
            f"{self.base_url}/api/chat",
            json={"session_id": session_id, "message": message},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()["reply"]


# --- Usage ---
if __name__ == "__main__":
    atl = AtlClient("https://api.atmospheric-truth.io")

    cert = atl.genesis_certificate()
    print("Genesis timestamp:", cert["minted_timestamp"])

    state = atl.system_state()
    print(f"Witnessed tiles: {state.witnessed_tiles:,}")

    reply = atl.ask_genesis(
        session_id=str(uuid.uuid4()),
        message="Explain the Byzantine consensus in one sentence.",
    )
    print("Genesis Engine:", reply)
```

### AI Agent Verification Pattern

An external AI agent can verify that its own dataset matches ATL's ground truth:

```python
from atl_client import AtlClient

atl = AtlClient("https://api.atmospheric-truth.io")

def verify_against_atl(agent_observation: dict) -> bool:
    """Cross-check an external agent's weather observation against ATL truth."""
    cert = atl.genesis_certificate()
    reply = atl.ask_genesis(
        session_id="agent-verify-01",
        message=(
            f"Given ledger genesis {cert['minted_timestamp']}, "
            f"my agent observed {agent_observation}. "
            "Is this consistent with ATL witnessed truth? Answer yes/no with reasoning."
        ),
    )
    return "yes" in reply.lower().split(".")[0]
```

---

## Rate Limits & Auth (production)

- **Public endpoints** (`/minting-certificate`, `/system-state`): 60 req/min per IP, no auth
- **Chat endpoint** (`/chat`): 20 req/min per session, no auth
- **Historical ledger queries** (`/api/ledger/query?tile=…&t=…`): reserved for authenticated API keys — coming in v1.1

Get an API key: email `ops@atmospheric-truth.io`
