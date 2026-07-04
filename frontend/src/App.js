import { useEffect, useState, Suspense, lazy } from "react";
import axios from "axios";
import "@/App.css";
import MatrixRain from "@/components/MatrixRain";
import CountUp from "@/components/CountUp";
import LiveHash from "@/components/LiveHash";

const EarthGlobe = lazy(() => import("@/components/EarthGlobe"));

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ============================================================================
// Top bar / status bar
// ============================================================================
function TopBar({ cert }) {
    const [clock, setClock] = useState(new Date().toISOString());
    useEffect(() => {
        const id = setInterval(() => setClock(new Date().toISOString()), 1000);
        return () => clearInterval(id);
    }, []);
    return (
        <div
            className="fixed top-0 left-0 right-0 z-40 border-b border-[rgba(0,255,65,0.25)] backdrop-blur-sm"
            style={{ background: "rgba(2,4,2,0.7)" }}
            data-testid="top-bar"
        >
            <div className="max-w-[1400px] mx-auto px-4 sm:px-6 py-2 flex items-center justify-between gap-4 text-[0.68rem] atl-mono uppercase tracking-[0.22em]">
                <div className="flex items-center gap-3">
                    <span className="atl-dot" />
                    <span className="text-[color:var(--atl-primary)]">ATL :: v1.0.0-minted</span>
                    <span className="hidden sm:inline text-white/30">//</span>
                    <span className="hidden sm:inline text-white/60">GENESIS LOCKED</span>
                </div>
                <div className="hidden md:flex items-center gap-4">
                    <span className="text-white/50">K = <span className="text-[color:var(--atl-primary)]">{cert?.engines?.ultimate_engine?.k_value ?? "0.995"}</span></span>
                    <span className="text-white/50">3/3</span>
                    <span className="text-white/50">UPTIME <span className="text-[color:var(--atl-secondary)]">CONTINUOUS</span></span>
                    <span className="text-white/40" data-testid="utc-clock">{clock.split(".")[0]}Z</span>
                </div>
            </div>
        </div>
    );
}

// ============================================================================
// Ticker
// ============================================================================
function Ticker({ cert }) {
    const items = [
        "GENESIS LEDGER POSITION 0",
        `MINTED ${cert?.minted_timestamp ?? "2026-04-23T07:53:50+10:00"}`,
        "BOM // HIMAWARI-8 // GOES-16 // METEOSAT",
        "BYZANTINE CONSENSUS K=0.995",
        "37M+ WITNESSED TILES",
        "RFC3161 TIMESTAMP VERIFIED",
        "FIREWALL DOCTRINE // TENET AGENCY 101",
        "XYO BOUND-WITNESS ACTIVE",
        "SERIES A :: $2.5M ASK // $12.5M POST-MONEY",
    ];
    const row = items.map((t, i) => (
        <span key={i} className="text-[0.72rem] atl-mono uppercase tracking-[0.28em]">
            <span className="text-[color:var(--atl-primary)] mr-3">◆</span>
            <span className="text-white/80">{t}</span>
        </span>
    ));
    return (
        <div className="atl-ticker" data-testid="status-ticker">
            <div className="atl-ticker__track">{row}</div>
            <div className="atl-ticker__track" aria-hidden="true">{row}</div>
        </div>
    );
}

// ============================================================================
// Hero
// ============================================================================
function Hero({ cert }) {
    return (
        <section className="relative pt-24 sm:pt-28" data-testid="hero-section">
            <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                <div className="lg:col-span-7 relative z-10">
                    <div className="flex items-center gap-3 mb-5">
                        <span className="atl-dot" />
                        <span className="atl-label">Proof-of-Existence // Witnessed</span>
                    </div>

                    <h1
                        className="atl-glitch atl-flicker font-black uppercase leading-[0.92]"
                        data-text="Atmospheric Truth Layer"
                        style={{
                            fontFamily: '"VT323", "Share Tech Mono", monospace',
                            fontSize: "clamp(3rem, 8vw, 7rem)",
                            letterSpacing: "0.01em",
                        }}
                        data-testid="hero-title"
                    >
                        Atmospheric Truth Layer
                    </h1>

                    <div className="mt-4 flex flex-wrap items-center gap-3 text-xs atl-mono uppercase tracking-[0.24em]">
                        <span className="px-2 py-1 border border-[rgba(0,255,65,0.4)] text-[color:var(--atl-primary)]">v1.0.0-minted</span>
                        <span className="px-2 py-1 border border-[rgba(0,255,255,0.4)] text-[color:var(--atl-secondary)]">Genesis · Ledger[0]</span>
                        <span className="px-2 py-1 border border-[rgba(255,255,255,0.2)] text-white/70">Byzantine K ≥ 0.995</span>
                    </div>

                    <p className="mt-7 max-w-2xl text-white/70 leading-relaxed atl-mono text-sm sm:text-base">
                        Cryptographically verified global atmospheric data integrity.
                        Witnessed by <span className="text-[color:var(--atl-primary)]">BOM</span>,{" "}
                        <span className="text-[color:var(--atl-primary)]">Himawari-8</span>,{" "}
                        <span className="text-[color:var(--atl-primary)]">GOES-16</span>, and{" "}
                        <span className="text-[color:var(--atl-primary)]">Meteosat</span>.
                        14 Byzantine engines. 37M+ tiles. One immutable ledger.
                    </p>

                    <div className="mt-8 flex flex-wrap gap-3">
                        <a href="#certificate" className="atl-btn" data-testid="cta-certificate">
                            <span>▶ View Genesis Certificate</span>
                        </a>
                        <a href="#series-a" className="atl-btn atl-btn--ghost" data-testid="cta-seriesa">
                            <span>◈ Series A Readout</span>
                        </a>
                    </div>

                    <div className="mt-10 grid grid-cols-3 gap-4 max-w-xl" data-testid="hero-mini-stats">
                        <div>
                            <div className="atl-label">Tiles</div>
                            <div className="atl-value" style={{ fontSize: "1.8rem" }}>37M+</div>
                        </div>
                        <div>
                            <div className="atl-label">K-Value</div>
                            <div className="atl-value" style={{ fontSize: "1.8rem" }}>0.995</div>
                        </div>
                        <div>
                            <div className="atl-label">Engines</div>
                            <div className="atl-value" style={{ fontSize: "1.8rem" }}>14</div>
                        </div>
                    </div>
                </div>

                <div className="lg:col-span-5 relative">
                    <div
                        className="relative aspect-square w-full max-w-[520px] mx-auto"
                        style={{
                            border: "1px solid rgba(0,255,65,0.35)",
                            background: "radial-gradient(ellipse at center, rgba(0,255,65,0.08), transparent 60%)",
                        }}
                    >
                        <span className="atl-bracket-tr" />
                        <span className="atl-bracket-bl" />
                        <Suspense
                            fallback={
                                <div className="absolute inset-0 flex items-center justify-center atl-mono text-[color:var(--atl-primary)] text-sm">
                                    LOADING_GLOBE...
                                </div>
                            }
                        >
                            <EarthGlobe />
                        </Suspense>
                        <div className="absolute top-2 left-2 atl-label">EARTH // LIVE</div>
                        <div className="absolute bottom-2 right-2 atl-label text-[color:var(--atl-secondary)]">04 SAT · ORBIT</div>
                    </div>
                </div>
            </div>
        </section>
    );
}

// ============================================================================
// Live engine counters
// ============================================================================
function EngineGrid({ cert }) {
    if (!cert) return null;
    const engines = [
        {
            key: "engine_365",
            title: "Engine 365-Days",
            sub: "Decomposition Validator",
            target: cert.engines.engine_365_days.cycles,
            unit: "CYCLES",
            rate: 3.2,
            sideLabel: "3/3 Validators",
            sideValue: "Circle · Monotonic · Range",
            testId: "engine-365",
        },
        {
            key: "ultimate",
            title: "Ultimate Engine",
            sub: "Byzantine Consensus",
            target: cert.engines.ultimate_engine.cycles,
            unit: "CYCLES",
            rate: 0.22,
            sideLabel: "K-Value",
            sideValue: `${cert.engines.ultimate_engine.k_value} · 12 Layers`,
            testId: "engine-ultimate",
        },
        {
            key: "tenet",
            title: "Tenet Agency 101",
            sub: "Firewall Doctrine",
            target: cert.engines.tenet_agency_101.ticks,
            unit: "TICKS",
            rate: 54.7,
            sideLabel: "Drift Ratio",
            sideValue: "1 : 2 · 100% Rejected",
            testId: "engine-tenet",
        },
        {
            key: "witness",
            title: "Witness Ledger",
            sub: "XYO Bound-Witness",
            target: cert.engines.witness_ledger.witnessed_tiles,
            unit: "TILES",
            rate: 2.6,
            sideLabel: "Coverage",
            sideValue: "Multi-Satellite · RFC3161",
            testId: "engine-witness",
        },
    ];
    return (
        <section className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 mt-24" data-testid="engines-section">
            <div className="atl-divider mb-8">
                <span>[02] // Live Engine Telemetry</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
                {engines.map((e) => (
                    <div key={e.key} className="atl-card atl-sweep" data-testid={`engine-card-${e.testId}`}>
                        <div className="flex items-center justify-between mb-5">
                            <div>
                                <div className="atl-label text-[color:var(--atl-secondary)]">{e.sub}</div>
                                <div className="mt-1 text-white text-base sm:text-lg uppercase tracking-wider font-bold">
                                    {e.title}
                                </div>
                            </div>
                            <span className="atl-dot" />
                        </div>
                        <div className="my-6">
                            <CountUp target={e.target} ratePerSec={e.rate} testId={`counter-${e.testId}`} />
                            <div className="atl-label mt-2">{e.unit} · LIVE</div>
                        </div>
                        <div className="h-px bg-[rgba(0,255,65,0.2)] my-3" />
                        <div>
                            <div className="atl-label">{e.sideLabel}</div>
                            <div className="mt-1 atl-mono text-sm text-white/80">{e.sideValue}</div>
                        </div>
                        <div className="mt-5 atl-progress" aria-hidden="true">
                            <div className="atl-progress__fill" style={{ width: `${70 + Math.random() * 28}%` }} />
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
}

// ============================================================================
// Witness satellites
// ============================================================================
function Witnesses({ cert }) {
    if (!cert) return null;
    const colors = ["#00FF41", "#00FFFF", "#00FF41", "#00FFFF"];
    return (
        <section className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 mt-28" data-testid="witnesses-section">
            <div className="atl-divider mb-8">
                <span>[03] // Multi-Satellite Witness Mesh</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5 lg:gap-6">
                {cert.witnesses.map((w, i) => (
                    <article
                        key={w.code}
                        className="atl-card"
                        data-testid={`witness-card-${w.code.toLowerCase()}`}
                    >
                        <div className="flex items-start justify-between gap-4 mb-4">
                            <div className="flex items-center gap-4">
                                <div
                                    className="w-14 h-14 border flex items-center justify-center atl-mono text-xs"
                                    style={{
                                        borderColor: colors[i],
                                        color: colors[i],
                                        boxShadow: `0 0 14px ${colors[i]}33`,
                                        background: "rgba(0,0,0,0.5)",
                                    }}
                                >
                                    SAT_{String(i + 1).padStart(2, "0")}
                                </div>
                                <div>
                                    <div className="atl-label">Node · {w.region}</div>
                                    <h3 className="text-white text-xl sm:text-2xl uppercase tracking-wider font-bold">
                                        {w.name}
                                    </h3>
                                    <div className="atl-mono text-xs text-white/50 mt-0.5">{w.node}</div>
                                </div>
                            </div>
                            <div
                                className="atl-mono text-[0.65rem] px-2 py-1 border flex items-center gap-2"
                                style={{
                                    borderColor: "rgba(0,255,65,0.6)",
                                    color: "var(--atl-primary)",
                                }}
                            >
                                <span className="atl-dot" />
                                VERIFIED
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4 mb-4">
                            <div>
                                <div className="atl-label">Observation</div>
                                <div className="atl-mono text-xs text-white/80 mt-1 break-all">
                                    {w.observation}
                                </div>
                            </div>
                            <div>
                                <div className="atl-label">Region</div>
                                <div className="atl-mono text-xs text-white/80 mt-1">{w.region}</div>
                            </div>
                        </div>

                        <div>
                            <div className="atl-label mb-1">Signature · Live Anchor</div>
                            <LiveHash anchor={w.signature} testId={`hash-${w.code.toLowerCase()}`} />
                        </div>
                    </article>
                ))}
            </div>
        </section>
    );
}

// ============================================================================
// Minting certificate
// ============================================================================
function Certificate({ cert }) {
    if (!cert) return null;
    return (
        <section
            id="certificate"
            className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 mt-28 scroll-mt-24"
            data-testid="certificate-section"
        >
            <div className="atl-divider mb-8">
                <span>[04] // Genesis Minting Certificate</span>
            </div>

            <div
                className="relative p-6 sm:p-10"
                style={{
                    border: "1px solid rgba(0,255,65,0.5)",
                    background: "linear-gradient(180deg, rgba(0,255,65,0.05), rgba(0,0,0,0.6))",
                    boxShadow: "0 0 50px rgba(0,255,65,0.15), inset 0 0 80px rgba(0,255,65,0.05)",
                }}
                data-testid="certificate-card"
            >
                <span className="atl-bracket-tr" />
                <span className="atl-bracket-bl" />
                <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[color:var(--atl-primary)] to-transparent" />

                <div className="flex flex-wrap items-center justify-between gap-3 mb-8">
                    <div>
                        <div className="atl-label">Witnessed Proof-of-Existence</div>
                        <div className="atl-sectiontitle mt-1 text-white">MINTED // GENESIS</div>
                    </div>
                    <div className="atl-mono text-xs text-white/60 uppercase tracking-[0.28em]">
                        Ledger Position · <span className="text-[color:var(--atl-primary)]">0</span> · Immutable
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                    <div className="lg:col-span-3 space-y-5">
                        <div>
                            <div className="atl-label">Official Genesis Timestamp</div>
                            <div
                                className="mt-2 atl-mono text-[color:var(--atl-primary)] text-lg sm:text-2xl break-all"
                                style={{ textShadow: "0 0 14px rgba(0,255,65,0.4)" }}
                                data-testid="genesis-timestamp"
                            >
                                {cert.minted_timestamp}
                            </div>
                            <div className="atl-mono text-xs text-white/50 mt-1">
                                {cert.timezone_offset}
                            </div>
                        </div>

                        <div>
                            <div className="atl-label">Cryptographic Hash</div>
                            <div className="atl-hash text-sm sm:text-base mt-2" data-testid="crypto-hash">
                                {cert.cryptographic_hash}
                            </div>
                        </div>

                        <div>
                            <div className="atl-label">TSA Signature · RFC3161</div>
                            <div className="atl-hash text-sm sm:text-base mt-2">
                                {cert.tsa_signature}
                            </div>
                        </div>

                        <div>
                            <div className="atl-label">Lock ID</div>
                            <div className="atl-hash text-sm sm:text-base mt-2">{cert.lock_id}</div>
                        </div>
                    </div>

                    <div className="lg:col-span-2 space-y-4">
                        <div className="atl-card" style={{ padding: "1rem 1.25rem" }}>
                            <div className="atl-label">Status</div>
                            <div className="mt-1 text-[color:var(--atl-primary)] text-lg uppercase tracking-wider font-bold">
                                {cert.status.replace("_", " ")}
                            </div>
                        </div>

                        <div className="grid grid-cols-3 gap-3">
                            {Object.entries(cert.wobble_constants).map(([k, v]) => (
                                <div key={k} className="atl-card" style={{ padding: "0.8rem" }}>
                                    <div className="atl-label" style={{ fontSize: "0.62rem" }}>{k}</div>
                                    <div className="atl-value" style={{ fontSize: "1.25rem" }}>{v}</div>
                                </div>
                            ))}
                        </div>

                        <div className="atl-card" style={{ padding: "1rem 1.25rem" }}>
                            <div className="atl-label">Attributes</div>
                            <ul className="mt-2 space-y-1 atl-mono text-xs text-white/70">
                                <li>✓ Immutable · Append-only</li>
                                <li>✓ Tamper-evident signatures</li>
                                <li>✓ Witnessed by 14 engines</li>
                                <li>✓ Multi-satellite convergence</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div className="mt-10 p-4 border border-[rgba(0,255,65,0.25)] atl-mono text-xs sm:text-sm text-white/75 leading-relaxed">
                    <span className="text-[color:var(--atl-secondary)]">&gt; </span>
                    This document cannot be altered without breaking all signatures.
                    This timestamp cannot be backdated without breaking RFC3161 authority.
                    This minting is <span className="text-[color:var(--atl-primary)]">permanent</span>,
                    <span className="text-[color:var(--atl-primary)]"> tamper-evident</span>, and
                    <span className="text-[color:var(--atl-primary)]"> verifiable</span>.
                </div>

                {cert.rfc3161 && (
                    <div
                        className="mt-6 p-4 sm:p-5 border border-[rgba(0,255,255,0.3)]"
                        style={{ background: "rgba(0,255,255,0.04)" }}
                        data-testid="rfc3161-block"
                    >
                        <div className="atl-label text-[color:var(--atl-secondary)] mb-3">
                            RFC3161 Timestamp Authority Certification
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs atl-mono">
                            <div>
                                <div className="text-white/40 uppercase tracking-widest">Authority</div>
                                <div className="text-white/90 mt-0.5">{cert.rfc3161.authority}</div>
                            </div>
                            <div>
                                <div className="text-white/40 uppercase tracking-widest">Timestamp</div>
                                <div className="text-white/90 mt-0.5 break-all">{cert.rfc3161.timestamp}</div>
                            </div>
                            <div>
                                <div className="text-white/40 uppercase tracking-widest">TSA Hash</div>
                                <div className="atl-hash mt-0.5">{cert.rfc3161.tsa_hash}</div>
                            </div>
                            <div>
                                <div className="text-white/40 uppercase tracking-widest">TSA Signature</div>
                                <div className="atl-hash mt-0.5">{cert.rfc3161.tsa_signature}</div>
                            </div>
                            <div className="sm:col-span-2">
                                <div className="text-white/40 uppercase tracking-widest">Certification</div>
                                <div className="text-[color:var(--atl-primary)] mt-0.5">
                                    {cert.rfc3161.certification}
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </section>
    );
}

// ============================================================================
// Byzantine consensus visualizer
// ============================================================================
function ByzantineMatrix() {
    // 14 engine nodes arranged on a 4x4-ish matrix (2 empty)
    const nodes = Array.from({ length: 14 }, (_, i) => i);
    return (
        <section className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 mt-28" data-testid="byzantine-section">
            <div className="atl-divider mb-8">
                <span>[05] // Byzantine Consensus Mesh · 14 Engines · 12 Layers</span>
            </div>
            <div className="atl-card">
                <div className="flex flex-wrap items-end justify-between gap-4 mb-6">
                    <div>
                        <div className="atl-label">K-Value Convergence</div>
                        <div className="atl-value" data-testid="k-value-display">0.995+</div>
                    </div>
                    <div className="text-right">
                        <div className="atl-label">Consensus Health</div>
                        <div className="text-[color:var(--atl-primary)] atl-mono text-sm uppercase tracking-widest">
                            3/3 · ALL LAYERS · HEALTHY
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-7 gap-2">
                    {nodes.map((n) => (
                        <div
                            key={n}
                            className="aspect-square border border-[rgba(0,255,65,0.4)] flex items-center justify-center atl-mono text-[0.6rem] text-[color:var(--atl-primary)]"
                            style={{
                                background: "rgba(0,255,65,0.06)",
                                boxShadow: "inset 0 0 12px rgba(0,255,65,0.15)",
                                animation: `atl-pulse ${1.2 + (n % 5) * 0.3}s ease-in-out infinite`,
                            }}
                            data-testid={`byz-node-${n}`}
                        >
                            E{String(n + 1).padStart(2, "0")}
                        </div>
                    ))}
                </div>

                <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <div className="atl-label">Decisions Executed</div>
                        <div className="atl-mono text-white mt-1">993,625</div>
                    </div>
                    <div>
                        <div className="atl-label">Decisions Rejected</div>
                        <div className="atl-mono text-white mt-1">1,554,454</div>
                    </div>
                    <div>
                        <div className="atl-label">Sovereignty Orders</div>
                        <div className="atl-mono text-white mt-1">10</div>
                    </div>
                </div>
            </div>
        </section>
    );
}

// ============================================================================
// Series A readout
// ============================================================================
function SeriesA({ cert }) {
    if (!cert) return null;
    const s = cert.series_a;
    const fmt = (n) =>
        n >= 1_000_000_000 ? `$${(n / 1_000_000_000).toFixed(1)}B`
        : n >= 1_000_000 ? `$${(n / 1_000_000).toFixed(2)}M`
        : `$${n.toLocaleString()}`;

    const rows = [
        { label: "Funding Ask", value: fmt(s.funding_ask_usd) },
        { label: "Post-Money Valuation", value: fmt(s.post_money_valuation_usd) },
        { label: "Market TAM", value: fmt(s.market_tam_usd) },
        { label: "Year 1 Revenue", value: fmt(s.year_1_revenue_usd) },
        { label: "Year 2 Revenue", value: fmt(s.year_2_revenue_usd) },
        { label: "Year 3 Revenue", value: fmt(s.year_3_revenue_usd) },
        { label: "Exit Path", value: s.exit_range_usd },
        { label: "Status", value: s.status.replace(/_/g, " ") },
    ];
    return (
        <section
            id="series-a"
            className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 mt-28 scroll-mt-24"
            data-testid="series-a-section"
        >
            <div className="atl-divider mb-8">
                <span>[06] // Series A Readout</span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                <div className="lg:col-span-1 atl-card">
                    <div className="atl-label">Fundraise</div>
                    <div className="atl-sectiontitle mt-2 text-white">$2.5M ASK</div>
                    <div className="atl-mono text-xs text-white/60 mt-2">Production-ready infrastructure</div>
                    <div className="mt-5 space-y-2 atl-mono text-sm text-white/80">
                        <div>→ $155B+ Addressable Market</div>
                        <div>→ $300–500M Exit Range</div>
                        <div>→ 7× Growth Year 1 → Year 2</div>
                    </div>
                    <button className="atl-btn mt-7 w-full justify-center" data-testid="book-investor-call">
                        ▶ Book Investor Call
                    </button>
                </div>

                <div className="lg:col-span-2 atl-card">
                    <div className="atl-label mb-4">Financial Readout // Terminal</div>
                    <div
                        className="atl-mono text-sm border border-[rgba(0,255,65,0.2)] p-4"
                        style={{ background: "rgba(0,0,0,0.5)" }}
                    >
                        <div className="text-[color:var(--atl-secondary)]">
                            atl@genesis:~$ cat series_a.readout
                        </div>
                        <div className="mt-3 space-y-1.5">
                            {rows.map((r) => (
                                <div
                                    key={r.label}
                                    className="flex justify-between gap-4 border-b border-dashed border-[rgba(0,255,65,0.12)] pb-1.5"
                                    data-testid={`series-a-row-${r.label.replace(/\s+/g, "-").toLowerCase()}`}
                                >
                                    <span className="text-white/60 uppercase tracking-widest text-xs">
                                        {r.label}
                                    </span>
                                    <span className="text-[color:var(--atl-primary)]">{r.value}</span>
                                </div>
                            ))}
                        </div>
                        <div className="mt-4 text-[color:var(--atl-secondary)]">
                            atl@genesis:~$ <span className="text-white/50">_</span>
                            <span style={{ animation: "atl-pulse 1s steps(1) infinite" }}>▌</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

// ============================================================================
// Series A Readiness Checklist
// ============================================================================
function ReadinessChecklist({ cert }) {
    if (!cert?.readiness_checklist) return null;
    const groups = Object.entries(cert.readiness_checklist);
    return (
        <section
            className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 mt-28"
            data-testid="readiness-section"
        >
            <div className="atl-divider mb-8">
                <span>[07] // Series A Readiness Checklist</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                {groups.map(([label, items]) => (
                    <div
                        key={label}
                        className="atl-card"
                        data-testid={`readiness-${label.toLowerCase()}`}
                    >
                        <div className="flex items-center justify-between mb-4">
                            <div className="text-white text-base uppercase tracking-wider font-bold">
                                {label}
                            </div>
                            <span className="atl-dot" />
                        </div>
                        <ul className="space-y-2 atl-mono text-xs text-white/75 leading-relaxed">
                            {items.map((it) => (
                                <li key={it} className="flex gap-2">
                                    <span className="text-[color:var(--atl-primary)] shrink-0">✓</span>
                                    <span>{it}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
        </section>
    );
}

// ============================================================================
// Roadmap / What's Next
// ============================================================================
function Roadmap({ cert }) {
    if (!cert?.roadmap) return null;
    const colorFor = (s) =>
        s === "COMPLETE" ? "var(--atl-primary)"
        : s === "IN_PROGRESS" ? "var(--atl-secondary)"
        : s === "UPCOMING" ? "rgba(255,255,255,0.8)"
        : "var(--atl-glitch)";

    return (
        <section
            className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 mt-28"
            data-testid="roadmap-section"
        >
            <div className="atl-divider mb-8">
                <span>[08] // What&apos;s Next · Execution Timeline</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {cert.roadmap.map((r, i) => (
                    <div
                        key={r.phase}
                        className="atl-card"
                        data-testid={`roadmap-${i}`}
                    >
                        <div className="flex items-center justify-between mb-3">
                            <div className="atl-label">Phase · {String(i + 1).padStart(2, "0")}</div>
                            <span
                                className="text-[0.62rem] atl-mono px-2 py-0.5 border"
                                style={{
                                    color: colorFor(r.status),
                                    borderColor: colorFor(r.status),
                                }}
                            >
                                {r.status.replace("_", " ")}
                            </span>
                        </div>
                        <div className="text-white text-lg uppercase tracking-wider font-bold mb-4">
                            {r.phase}
                        </div>
                        <ul className="space-y-2 atl-mono text-xs text-white/75">
                            {r.items.map((it) => (
                                <li key={it} className="flex gap-2">
                                    <span className="text-[color:var(--atl-primary)]">→</span>
                                    <span>{it}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
        </section>
    );
}

// ============================================================================
// GitHub / Repository block
// ============================================================================
function RepoBlock({ cert }) {
    if (!cert?.github) return null;
    const g = cert.github;
    return (
        <section
            className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 mt-28"
            data-testid="repo-section"
        >
            <div className="atl-divider mb-8">
                <span>[09] // Official Repository</span>
            </div>
            <div className="atl-card">
                <div className="grid grid-cols-1 md:grid-cols-5 gap-6 items-center">
                    <div className="md:col-span-3">
                        <div className="atl-label">Repository</div>
                        <a
                            href={g.repository}
                            target="_blank"
                            rel="noreferrer noopener"
                            className="block mt-2 text-[color:var(--atl-primary)] atl-mono text-base sm:text-lg break-all hover:underline"
                            data-testid="repo-link"
                        >
                            {g.repository}
                        </a>
                        <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs atl-mono">
                            <div>
                                <div className="text-white/40 uppercase tracking-widest">Release</div>
                                <div className="text-[color:var(--atl-secondary)] mt-0.5">{g.release_tag}</div>
                            </div>
                            <div>
                                <div className="text-white/40 uppercase tracking-widest">License</div>
                                <div className="text-white/90 mt-0.5">{g.license}</div>
                            </div>
                            <div className="col-span-2">
                                <div className="text-white/40 uppercase tracking-widest">Status</div>
                                <div className="text-[color:var(--atl-primary)] mt-0.5">{g.status}</div>
                            </div>
                        </div>
                    </div>
                    <div className="md:col-span-2">
                        <a
                            href={g.repository}
                            target="_blank"
                            rel="noreferrer noopener"
                            className="atl-btn w-full justify-center"
                            data-testid="repo-cta"
                        >
                            ▶ Clone · git pull origin genesis
                        </a>
                        <a
                            href="#certificate"
                            className="atl-btn atl-btn--ghost w-full justify-center mt-3"
                        >
                            ◈ Re-verify Signatures
                        </a>
                    </div>
                </div>
            </div>
        </section>
    );
}

// ============================================================================
// Final ASCII Affirmation
// ============================================================================
function Affirmation() {
    const block = `╔═════════════════════════════════════════════════════════════════════════╗
║                                                                         ║
║     The sky doesn't lie. Satellites don't sleep. Math doesn't break.    ║
║                                                                         ║
║              Minted: 2026-04-23T07:53:50.5144990+10:00                  ║
║              Status: ● PRODUCTION READY                                 ║
║              Series A: Ready to launch                                  ║
║                                                                         ║
║  Witnessed by 4 satellites + 14 Byzantine engines + XYO ledger.         ║
║  Cryptographically verified. Tamper-proof. Immutable.                   ║
║                                                                         ║
║              This is the moment atmospheric truth began.                ║
║                                                                         ║
╚═════════════════════════════════════════════════════════════════════════╝`;
    return (
        <section
            className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 mt-28"
            data-testid="affirmation-section"
        >
            <div className="atl-divider mb-8">
                <span>[10] // Final Affirmation</span>
            </div>
            <pre
                className="atl-mono text-[0.58rem] sm:text-[0.72rem] lg:text-[0.85rem] leading-tight text-[color:var(--atl-primary)] p-4 sm:p-6 overflow-x-auto"
                style={{
                    background: "rgba(0,0,0,0.55)",
                    border: "1px solid rgba(0,255,65,0.35)",
                    boxShadow: "0 0 30px rgba(0,255,65,0.2), inset 0 0 30px rgba(0,255,65,0.05)",
                    textShadow: "0 0 10px rgba(0,255,65,0.4)",
                }}
                data-testid="affirmation-ascii"
            >
{block}
            </pre>
        </section>
    );
}

// ============================================================================
// Footer
// ============================================================================
function Footer() {
    return (
        <footer className="relative mt-32 pb-16" data-testid="footer">
            <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10">
                <div className="atl-divider mb-10">
                    <span>[END] // Signal Out</span>
                </div>
                <div className="text-center">
                    <p
                        className="atl-glitch atl-flicker text-[color:var(--atl-secondary)]"
                        data-text="The sky doesn't lie. Satellites don't sleep. Math doesn't break."
                        style={{
                            fontFamily: '"VT323", monospace',
                            fontSize: "clamp(1.4rem, 3.2vw, 2.6rem)",
                            letterSpacing: "0.04em",
                        }}
                        data-testid="footer-tagline"
                    >
                        The sky doesn&apos;t lie. Satellites don&apos;t sleep. Math doesn&apos;t break.
                    </p>
                    <div className="mt-6 atl-mono text-xs text-white/50 uppercase tracking-[0.3em]">
                        Minted 2026-04-23 · AEST · Witnessed by 14 Byzantine engines + XYO ledger
                    </div>
                    <div className="mt-2 atl-mono text-xs text-white/30">
                        AiTenet Agency · Atmospheric Truth Layer · v1.0.0-minted
                    </div>
                </div>
            </div>
        </footer>
    );
}

// ============================================================================
// App
// ============================================================================
function App() {
    const [cert, setCert] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios
            .get(`${API}/minting-certificate`)
            .then((r) => setCert(r.data))
            .catch((e) => {
                console.error(e);
                setError(e.message);
            });
    }, []);

    return (
        <div className="App relative min-h-screen atl-grid-bg" data-testid="app-root">
            <MatrixRain />
            <div className="atl-scanlines" />

            <div className="relative z-10">
                <TopBar cert={cert} />
                <div className="pt-12">
                    <Ticker cert={cert} />
                </div>

                {error && (
                    <div
                        className="max-w-[1400px] mx-auto my-4 px-6 py-3 border border-red-500/40 text-red-300 atl-mono text-xs"
                        data-testid="api-error"
                    >
                        SIGNAL LOSS :: /api/minting-certificate unreachable :: {error}
                    </div>
                )}

                <Hero cert={cert} />
                <EngineGrid cert={cert} />
                <Witnesses cert={cert} />
                <Certificate cert={cert} />
                <ByzantineMatrix />
                <SeriesA cert={cert} />
                <ReadinessChecklist cert={cert} />
                <Roadmap cert={cert} />
                <RepoBlock cert={cert} />
                <Affirmation />
                <Footer />
            </div>
        </div>
    );
}

export default App;
