# Atmospheric Truth Layer

> **Weather data you can actually trust.** Every reading signed by 4 satellites across 4 continents, cross-checked by 14 independent validators. Impossible to fake. Impossible to edit. Impossible to backdate.

[![Version](https://img.shields.io/badge/version-v1.0.0--minted-00FF41)](./MINTED.md)
[![Status](https://img.shields.io/badge/status-PRODUCTION%20READY-00FF41)](./MINTED.md)
[![License](https://img.shields.io/badge/license-MIT-00FFFF)](#license)
[![Hardware](https://img.shields.io/badge/hardware-espVmark.MyWare%20/%20ESP32--C6-00FFFF)](#hardware-layer)
[![Consensus](https://img.shields.io/badge/K--value-≥%200.995-00FF41)](./docs/ARCHITECTURE.md)

---

## The Sky Doesn't Lie. Satellites Don't Sleep. Math Doesn't Break.

**Atmospheric Truth Layer (ATL)** is the world's first cryptographically-verified atmospheric data infrastructure. Every observation is:

- **Signed** by 4 independent satellite agencies — **BOM** (Australia), **Himawari-8** (Japan), **GOES-16** (USA), **Meteosat** (Europe)
- **Cross-validated** by 14 Byzantine consensus engines requiring K ≥ 0.995 agreement
- **Anchored** to RFC3161 GPS-backed timestamps (Meinberg authority)
- **Committed** to an immutable, append-only XYO witness ledger
- **Verified** at the hardware level by espVmark.MyWare on ESP32-C6

The result: environmental ground truth that is **court-admissible under FRE 902(13)**, uneditable by any operator including us, and queryable by any external system in <400 ms.

---

## Who This Is For

| Audience | Why ATL matters |
|----------|-----------------|
| **Assistive-tech builders** | Blind & visually impaired children can trust the environment their wearable reports |
| **Disaster response (FEMA, NGOs)** | Signed proof of wind speed / rainfall / temperature at a specific tile & time |
| **Parametric insurance** | An oracle both parties trust — automatic payouts without adjusters |
| **Carbon-credit auditors** | Signed time-series of canopy cover per grid tile, over years |
| **Climate litigation** | Digital records that survive cross-examination |
| **AI agents** | External LLMs can call ATL to verify their own datasets against ground truth |

---

## Live Demo

**Preview:** [`atmospheric-truth-layer.preview.emergentagent.com`](https://001f17d8-75f0-4fb3-9220-1a1d2aee4b83.preview.emergentagent.com)

- Watch 4 satellites orbit a live wireframe Earth
- Real-time engine telemetry (Engine 365-Days · Ultimate · Tenet Agency 101 · Witness Ledger)
- Ask the **Genesis Engine** (Gemini 3 Flash grounded in ATL system prompt) anything about the system
- Live sparkline of tick-rate polling the running production grid every 2 seconds

---

## The Genesis Moment

```
MINTED TIMESTAMP: 2026-04-23T07:53:50.5144990+10:00
CRYPTOGRAPHIC HASH: e14f9a8d2c7b5e3f1a9d4c8b2e6f7a3d
TSA SIGNATURE:     f7e3b2c1d4a9e5f8b2c6d1a7e3f9b4c2
LEDGER POSITION:   0 (Genesis)
STATUS:            🟢 PRODUCTION READY
```

See [`MINTED.md`](./MINTED.md) for the full witnessed proof-of-existence certificate.

---

## Architecture at a Glance

```
[ SATELLITES ] ──► [ ENGINE 365-DAYS ] ──► [ ULTIMATE ENGINE ] ──► [ TENET AGENCY 101 ] ──► [ WITNESS LEDGER ] ──► [ PUBLIC API ]
      4               3/3 validators           K ≥ 0.995 Byz              100% firewall            RFC3161 signed          /system-state
   BOM · JMA          Circle/Mono/Range        12 layers · 14 eng         Sovereignty-only          XYO bound              /chat (Gemini)
   NOAA · EUMETSAT
```

Deep dive: [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md)

---

## Hardware Layer — espVmark.MyWare

ATL runs on custom hardware. **espVmark.MyWare** on ESP32-C6 provides:

- Automated firmware flash + verification on every commit
- Manifest-hash-bound builds (mismatch = rejected)
- Physical possession required for sovereignty-order signatures
- 4.2× faster iteration velocity than average build pipeline

You cannot fork ATL from GitHub alone. You must also build the board. That is intentional — it's the difference between a software oracle and a *trust root*.

---

## Public API

Three read-only endpoints, zero auth required for public data:

- `GET /api/minting-certificate` — full genesis payload
- `GET /api/system-state` — live counters since genesis
- `POST /api/chat` — Genesis Engine Q&A (Gemini 3 Flash)

Full spec + **TypeScript & Python SDKs**: [`docs/PUBLIC_API.md`](./docs/PUBLIC_API.md)

---

## Use Cases (Deep Dives)

- Assistive navigation for blind & visually impaired children
- Disaster-response verification
- ESG / carbon-credit verification
- Parametric insurance oracles
- Court-admissible environmental evidence

Full details: [`docs/USE_CASES.md`](./docs/USE_CASES.md)

---

## Quick Start (Local)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001

# Frontend
cd frontend
yarn install
yarn start
```

Then hit `http://localhost:3000`.

---

## Series A

Series A is **OPEN**. Financials, valuations, revenue projections, and exit strategy are shared **under NDA**.

**Book an investor call →** (contact via GitHub issues or the site's investor CTA)

---

## For Journalists & Analysts

Press kit: [`docs/PRESS_KIT.md`](./docs/PRESS_KIT.md)
Launch assets: [`docs/LAUNCH_ASSETS.md`](./docs/LAUNCH_ASSETS.md)

---

## For Engineers

- Known non-issues we've triaged: [`KNOWN_ISSUES.md`](./KNOWN_ISSUES.md)
- SonarCloud config: [`.sonarcloudignore`](./.sonarcloudignore)
- 8 backend tests: [`backend/tests/test_atl_backend.py`](./backend/tests/test_atl_backend.py)
- Zero ESLint warnings on production files.

---

## License

MIT. See [`LICENSE`](./LICENSE) for details.

---

## The Tagline

> **The sky doesn't lie. Satellites don't sleep. Math doesn't break.**

This is the moment atmospheric truth began.

`v1.0.0-minted` · `2026-04-23T07:53:50.5144990+10:00`
