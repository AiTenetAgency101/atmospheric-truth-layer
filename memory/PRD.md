# Atmospheric Truth Layer — Showcase Site (PRD)

## Original Problem Statement
User shared a "MINTING CERTIFICATE" document for **Atmospheric Truth Layer v1.0.0-minted** — a Series-A-ready cryptographically verified atmospheric data integrity system.
- Genesis Timestamp: `2026-04-23T07:53:50.5144990+10:00`
- 4 engines: Engine 365-Days (37M+ cycles), Ultimate Engine (Byzantine K=0.995), Tenet Agency 101 (641M ticks), Witness Ledger (37M+ tiles)
- 4 satellite witnesses: BOM (AUS), Himawari-8 (JPY), GOES-16 (USA), Meteosat (EU)
- Series A: $2.5M ask, $12.5M post-money, $3.18M Y1 revenue, $300–500M exit
- Tagline: "The sky doesn't lie. Satellites don't sleep. Math doesn't break."

## User Preference
- `matrix 3d style`

## Architecture
- **Frontend**: React 19 + CRA/Craco, Tailwind, vanilla Three.js for 3D globe, HTML5 Canvas for Matrix rain, JetBrains Mono + VT323 + Share Tech Mono fonts
- **Backend**: FastAPI, exposes read-only genesis data; MongoDB retained for legacy `/api/status`
- **Theme**: Cyberpunk terminal — #00FF41 primary, #00FFFF secondary, #FF0055 glitch, deep black background; CRT scanlines + grid bg + corner brackets + glitch title

## Implemented (2026-04-30)
- `/api/minting-certificate` — full genesis payload (engines, witnesses, wobble constants, series_a, tagline)
- `/api/system-state` — live-incrementing cycle counts since genesis
- Hero with glitch-animated title + vanilla Three.js wireframe Earth + 4 orbiting satellites + starfield
- Top status bar (K-value, 3/3 consensus, UTC clock, uptime), status ticker marquee
- 4 engine cards with live-ticking counters + progress bars + sweep animation
- 4 satellite witness cards (VERIFIED badges, live-scrambling hashes anchored to real signatures)
- Genesis minting certificate card (timestamp, crypto hash, TSA signature, lock ID, wobble constants)
- Byzantine consensus matrix (14 pulsing engine nodes, decisions stats)
- Series A readout in terminal-style financial panel
- Footer with glitch tagline

## Testing
- `testing_agent_v3` iteration 1: 100% backend + 100% frontend pass
- Pytest suite: `/app/backend/tests/test_atl_backend.py`

## Next Action Items / Backlog (P1/P2)
- P1: Add a "verify this timestamp" widget that recomputes the SHA-256 of the certificate client-side
- P2: Add a historical ledger scroll (fake / paginated) showing cycles-over-time
- P2: Add dark/light theme toggle (purely stylistic)
- P2: Animate satellite witness signatures into the globe (connecting lines from orbit dots → globe)
- Future: Hook up a real WebSocket feed to `/api/system-state` for sub-second ticking

## Personas
- **Investor** visiting during Series A roadshow → needs impressive, trust-building visual proof of production-readiness
- **Technical reviewer / DD** → needs the raw hashes, timestamps, consensus metrics visible
- **GitHub visitor** → needs a memorable landing that matches the MINTED.md vibe
