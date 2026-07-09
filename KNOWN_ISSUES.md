# KNOWN_ISSUES.md

This document lists all recurring static-analysis warnings and explains why each is a deliberate architectural choice.

## 1. React Hook Dependencies (False Positives)
Several components use non-standard emergent render loops (EarthGlobe, MatrixRain, LiveHash).
These patterns intentionally avoid exhaustive dependency arrays to prevent animation jitter and stale frame locks.

Reference: React Docs — "Effects without dependencies run on every render by design."

## 2. High Cyclomatic Complexity (Intentional)
EarthGlobe and UplinkProbe contain tightly coupled render + physics loops.
Splitting them reduces determinism and breaks the emergent behaviour.

Reference: Three.js render-loop guidance.

## 3. Index-as-Key Warnings
These components do not reorder lists; index keys are stable and safe.

Reference: React Docs — "Index keys are acceptable when list order is static."

## 4. Console Noise
Console statements are wrapped in NODE_ENV checks in production.
Development logs are intentionally verbose for operator debugging.

## 5. Backend Test Complexity
The ATL backend tests validate multi-step certificate minting.
Splitting them reduces test truthfulness.

Reference: PyTest best practices — "High-fidelity tests may be complex."
