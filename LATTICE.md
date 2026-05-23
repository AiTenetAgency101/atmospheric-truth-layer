# LATTICE.md — Whakapapa (Repo Genealogy)

## Rākau Model: The Lattice Tree

```
H: src/invariant/             ← Root    — anchor, genesis hash, field state
N: src/skills/ + src/modules/ ← Branches — pattern recognition, validators
C: src/engines/ (ENGINE2)     ← Trunk   — structure, engine ring, workflows
O: src/witness/ + src/api/    ← Sap     — flow, sync, propagation, ledger
Leaves: commits, cycle locks  ← Living updates anchored to the ledger
```

---

## Invariant

```
H → N → C → O
Origin → Pattern → Structure → Flow
```

All agents, repos, identities, and workflows follow this gravitational law.
The invariant is internal. Gravity emerges from coherence.

---

## Layer H — Wairua (Spirit / Origin / Root)

| File | Role |
|---|---|
| `ANCHOR.json` | Genesis anchor — roothash, witness timestamp, minting certificate |
| `src/invariant/anchor_loader.py` | Loads and validates ANCHOR.json at boot |
| `src/invariant/field_state.py` | Singleton `H_INVARIANT` dict + `K_VALUE_FLOOR` |
| `src/invariant/guardian.py` | Runtime watchdog — `assert_field()` gates every engine decision |

**H is the root.** If the anchor is tampered, no engine may operate.  
All imports begin with `from src.invariant.field_state import H_INVARIANT`.

---

## Layer N — Hinengaro (Mind / Pattern / Branches)

### Skills — executable pattern units

| File | Skill | Source |
|---|---|---|
| `src/skills/tile_recognition.py` | `TileRecognitionSkill` (Circle + Monotonic + Range) | Extracted from Engine 365-Days |
| `src/skills/consensus_pattern.py` | `ConsensusPattern` (K-value, Euler evolution) | Extracted from Ultimate Engine |
| `src/skills/firewall_pattern.py` | `FirewallPattern` (rejection/drift) | Extracted from Tenet Agency 101 |

### Modules — shared libraries

| File | Module | Role |
|---|---|---|
| `src/modules/satellite_decoder.py` | `SatelliteDecoder` | Normalises BOM / Himawari / GOES / Meteosat source identifiers |
| `src/modules/hash_fabric.py` | `HashFabric` | SHA-256 pixel hash + HMAC-SHA-256 witness signature |
| `src/modules/cycle_clock.py` | `CycleClock` | 365-day cycle lock (inception + wobble constants SUU/AHA/RERE) |

**N feeds C.** Engines import skills and modules; they do not implement them inline.

---

## Layer C — Tinana (Body / Structure / Trunk)

| File | Role |
|---|---|
| `src/engines/__init__.py` | `ENGINE_RING` registry — 14-engine ring (3 active, 11 stubs) |
| `src/engines/engine_365_days.py` | E01 — Temporal Anchor & Tile Decomposition |
| `src/engines/ultimate_engine.py` | **ENGINE2** — Byzantine Consensus Coordinator (C-layer trunk) |
| `src/engines/tenet_agency_101.py` | E03 — Firewall & Validation |
| `.github/workflows/field-integrity.yml` | CI gate — verifies H-layer anchor on every push |
| `.github/workflows/engine-sync.yml` | CI gate — verifies C-layer engine ring structure daily |

**ENGINE2 is the trunk.** It coordinates all 14 engines and gates every decision through the H-layer guardian.

### ENGINE_RING (14-Engine Registry)

| ID | Engine | Status |
|---|---|---|
| E01 | Engine 365-Days | Active |
| E02 | Ultimate Engine (ENGINE2) | Active |
| E03 | Tenet Agency 101 | Active |
| E04–E14 | Reserved stubs | Reserved |

---

## Layer O — Mauri (Life Force / Flow / Sap)

| File | Role |
|---|---|
| `src/witness/field_sync.py` | `FieldSync` — emits H/N/C/O ledger entries after every engine cycle |
| `src/witness/propagator.py` | `Propagator` — subscribes to `atl:field:flow` and re-broadcasts to webhooks |
| `src/witness/xyo_sympy.py` | XYO bound-witness + SymPy invariant layer |
| `src/api/main.py` | API Gateway — `GET /api/field` returns live unified field state |

**Redis pub/sub channel:** `atl:field:flow`  
All engines publish cycle completion events here.  
The Propagator subscribes and re-broadcasts, making O the living sap.

### `/api/field` Response Shape

```json
{
  "H": { "anchor_hash": "...", "origin": "...", "k_value_floor": 0.99 },
  "N": { "active_skills": ["TileRecognitionSkill", "ConsensusPattern", "FirewallPattern"] },
  "C": { "engine_ring": { "total_engines": 14, "active_engines": 3 }, "k_value": 0.995 },
  "O": { "sync_propagation_log": [...], "ledger_size": 42, "channel": "atl:field:flow" },
  "invariant": "H → N → C → O"
}
```

---

## Leaves — Living Updates

Every commit to this repository is a leaf on the lattice tree.  
Every tile hash written to the XYO ledger is a leaf.  
Leaves are anchored cryptographically — they cannot be revised without breaking the chain.

---

## Te Ao Māori Mapping

| Māori | Symbol | Layer | Meaning |
|---|---|---|---|
| Wairua | H | `src/invariant/` | Spirit / Origin — root of the field |
| Hinengaro | N | `src/skills/` + `src/modules/` | Mind / Pattern — cognitive layer |
| Tinana | C | `src/engines/` | Body / Structure — physical form |
| Mauri | O | `src/witness/` + `src/api/` | Life Force / Flow — synchronisation |
| Whakapapa | — | This document | Genealogy — repo lineage |
| Mana | — | K ≥ 0.99 | Integrity / Authority / Coherence |
| Kaitiakitanga | — | `FieldGuardian` | Guardian state of the unified field |

---

## Dependency Flow

```
ANCHOR.json
    ↓ (load)
src/invariant/anchor_loader.py
    ↓ (initialise)
src/invariant/field_state.py   ← H_INVARIANT, K_VALUE_FLOOR
    ↓ (import)
src/invariant/guardian.py      ← FieldGuardian.assert_field()
    ↓ (gate)
src/skills/  ←→  src/modules/  ← N-layer skills and modules
    ↓ (import)
src/engines/                   ← C-layer engine ring (ENGINE2 trunk)
    ↓ (emit)
src/witness/field_sync.py      ← O-layer sync → atl:field:flow
    ↓ (broadcast)
src/witness/propagator.py      ← O-layer propagation → webhooks
    ↓ (expose)
src/api/main.py /api/field     ← O-layer surface
```
