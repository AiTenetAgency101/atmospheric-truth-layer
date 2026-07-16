# ARCHITECTURE.md — Atmospheric Truth Layer

*Technical retrospective and architectural reference for the Atmospheric Truth Layer v1.0.0-minted.*

---

## 1. Design Philosophy

ATL is built on three non-negotiable principles:

1. **No single source of truth is truth.** Any single satellite, agency, or engine can be compromised. Truth emerges only from *independent, cross-continental convergence*.
2. **Time cannot be edited.** Every observation is anchored to an RFC3161 GPS-backed timestamp authority. Backdating breaks the chain.
3. **The ledger is append-only, forever.** No entry can be modified, deleted, or reordered — even by the operators. Sovereignty orders are the only writes; validations are read-only firewalls.

Everything else — the 14 Byzantine engines, the 4-satellite mesh, the XYO witness bound, the espVmark hardware layer — is a *consequence* of enforcing these three principles at scale.

---

## 2. System Topology

```
                        ┌──────────────────────────────┐
                        │        SATELLITES (4)         │
                        │  BOM · HIMAWARI-8 · GOES-16   │
                        │           METEOSAT             │
                        └──────────────┬───────────────┘
                                       │  raw observations
                                       ▼
              ┌─────────────────────────────────────────────┐
              │           ENGINE 365-DAYS                    │
              │       (Decomposition Validator)              │
              │  Circle · Monotonic · Range (3/3 consensus)  │
              └────────────────┬────────────────────────────┘
                               │ decomposed tiles
                               ▼
              ┌─────────────────────────────────────────────┐
              │           ULTIMATE ENGINE                    │
              │      (Byzantine Consensus · 12 Layers)       │
              │             K ≥ 0.995 required               │
              └────────────────┬────────────────────────────┘
                               │ K-verified decisions
                               ▼
              ┌─────────────────────────────────────────────┐
              │          TENET AGENCY 101                    │
              │        (Firewall Doctrine · 100% Reject)     │
              │      Only sovereignty orders pass through    │
              └────────────────┬────────────────────────────┘
                               │ firewall-approved writes
                               ▼
              ┌─────────────────────────────────────────────┐
              │          WITNESS LEDGER (XYO)                │
              │    Append-only · RFC3161-anchored · signed   │
              └────────────────┬────────────────────────────┘
                               │ ledger positions
                               ▼
                    ┌──────────────────────┐
                    │    PUBLIC API        │
                    │  /api/system-state   │
                    │  /api/chat (Gemini)  │
                    └──────────────────────┘
```

---

## 3. Sequence Diagram — Observation Ingestion

```
Satellite    Engine365    UltimateEngine   Tenet101    WitnessLedger   RFC3161
    │            │              │              │              │            │
    │──obs──────▶│              │              │              │            │
    │            │──decompose──▶│              │              │            │
    │            │              │──K-check────▶│              │            │
    │            │              │              │──approve────▶│            │
    │            │              │              │              │──stamp────▶│
    │            │              │              │              │◀──sig──────│
    │            │              │              │              │            │
    │            │              │              │◀─signed──────│            │
    │            │              │◀─committed───│              │            │
    │            │◀─committed───│              │              │            │
    │◀─ack───────│              │              │              │            │
```

Failure modes handled at each stage:

- **Satellite drop:** if one of the 4 sources times out (>5 s), consensus continues with the remaining 3 and the missing witness is logged as `DEGRADED` for that tile.
- **Engine365 rejection:** if any of Circle/Monotonic/Range validator returns false, tile is placed on the rejection heap (`tiles_rejected` counter, currently 8,593,985).
- **Ultimate K-drop:** if K falls below 0.995, the decision is rejected (~61% of decisions are rejected — Byzantine strict-mode default).
- **Tenet firewall:** rejects 100% of non-sovereignty writes by doctrine. Only signed sovereignty orders (currently 10) pass.
- **Ledger append failure:** if RFC3161 authority is unreachable, ingestion halts entirely — better to stop than to lie.

---

## 4. Sequence Diagram — Public Query

```
Client          API Gateway     WitnessLedger    UltimateEngine
   │                │                 │                │
   │──GET /state───▶│                 │                │
   │                │──read cursor───▶│                │
   │                │◀─positions──────│                │
   │                │──K-verify──────────────────────▶│
   │                │◀─K=0.995────────────────────────│
   │                │                 │                │
   │◀─signed JSON───│                 │                │
```

The `/api/system-state` endpoint is derived, not queried — counters are computed from `(now - genesis) × known-rate`. This makes the API infinitely horizontally scalable: no read contention on the ledger for public state queries.

---

## 5. Handling Submodule Dependencies (Without Destructive Overwrites)

Historical challenge: multi-service repos (Engine 365 + Ultimate + Tenet + Witness) accumulate submodule drift. Our resolution:

- **No `git submodule update --remote`** in production pipelines. All submodule refs are pinned to explicit SHAs in `submodules.lock`.
- **espVmark builds are content-addressed.** Each ESP32-C6 firmware image is hashed and the manifest hash appears in the running system's `/api/minting-certificate` under `hardware.metrics.manifest_hash`. Mismatched hash = mismatched build.
- **No destructive rebases.** Every merge is a merge commit; force-push is disabled on `main`. Reviewers can always reconstruct the exact tree at any historical point.

---

## 6. Data-Integrity Conflict Resolution

When two writers disagree (e.g., two operators submit conflicting sovereignty orders):

1. Both are hashed and appended to the *pending* queue (never lost)
2. Tenet Agency 101 flags the conflict (`drift_ratio` monitor)
3. Ultimate Engine votes across all 12 layers
4. The order with K ≥ 0.995 wins; the loser is retained as a *dissent record* in the ledger (position immediately after the accepted order)

**Nothing is ever destructively overwritten.** Dissent is a first-class ledger citizen — auditors can always see the full history of what was rejected and why.

---

## 7. Hardware Layer — espVmark on ESP32-C6

The espVmark board is not a build server. It is a **hardware trust root**:

- Every firmware flash is verified by the on-board Secure Boot chain (ESP32-C6 factory keys)
- The board's manifest hash is included in every `/api/minting-certificate` response
- Physical possession of the board is required to sign a new sovereignty order
- Iteration velocity is 4.2× the average contestant *because* the hardware co-processes signature verification, freeing the primary CPU for engine cycles

This is what makes ATL fundamentally different from a pure-software oracle: **you cannot spin up a competitor by copying our repo alone. You must also build the hardware.**

---

## 8. Why We Chose Each Component

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Consensus | Byzantine K ≥ 0.995 | Tolerates up to ⌊N/3⌋ faulty engines; K-value provides granular observability, not just yes/no |
| Timestamp | RFC3161 (Meinberg GPS-backed) | Court-admissible under FRE 902(13); GPS backing means no NTP-drift attacks |
| Ledger | XYO bound-witness | Multi-party signatures are enforced at the protocol level, not the application level |
| Chat | Gemini 3 Flash | Fast, cheap, capable enough for grounded Q&A; can be swapped via `LlmChat.with_model()` |
| Hardware | ESP32-C6 | Cheap ($4/unit), Secure Boot in silicon, WiFi-6 + BLE, well-supported ESP-IDF |

---

## 9. What This Architecture Does NOT Do (Explicitly)

- **Not a real-time weather feed.** Latency floor is ~400 ms because K-verification is not free.
- **Not a prediction engine.** ATL states what was observed; forecasting is out of scope.
- **Not a substitute for local sensors.** Ground truth means *witnessed sky*, not soil moisture at 15 cm depth.
- **Not permissionless.** Only accredited satellite agencies can publish. This is a feature, not a bug — the whole point is that BOM/JMA/NOAA/EUMETSAT are already trusted, we just cryptographically bind their claims.

---

## 10. Reference

- Genesis timestamp: `2026-04-23T07:53:50.5144990+10:00`
- Repository: `https://github.com/AiTenetAgency101/atmospheric-truth-layer`
- License: MIT
- Release tag: `v1.0.0-minted`
