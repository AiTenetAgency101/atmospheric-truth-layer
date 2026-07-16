import { useEffect, useRef, useState } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * Live telemetry dashboard — polls /api/system-state every 2s and
 * renders a rolling sparkline of tenet_ticks/sec + node grid + K-gauge.
 */
export default function LiveTelemetry() {
    const [state, setState] = useState(null);
    const [history, setHistory] = useState([]); // recent tenet_ticks values
    const prevRef = useRef(null);

    useEffect(() => {
        let cancelled = false;
        const poll = async () => {
            try {
                const res = await axios.get(`${API}/system-state`, { timeout: 5000 });
                if (cancelled) return;
                setState(res.data);
                const prev = prevRef.current;
                const delta = prev ? Math.max(0, res.data.tenet_ticks - prev.tenet_ticks) : 0;
                const dtSec = prev
                    ? Math.max(0.1, (Date.parse(res.data.server_time) - Date.parse(prev.server_time)) / 1000)
                    : 1;
                setHistory((h) => {
                    const rate = delta / dtSec;
                    const next = [...h, rate].slice(-40);
                    return next;
                });
                prevRef.current = res.data;
            } catch (err) {
                if (process.env.NODE_ENV !== "production") console.debug("[LiveTelemetry]", err?.message);
            }
        };
        poll();
        const id = setInterval(poll, 2000);
        return () => { cancelled = true; clearInterval(id); };
    }, []);

    const maxRate = history.length ? Math.max(...history, 1) : 1;
    const nodes = [
        { id: "XyoNode01", role: "Bound-Witness Hyper-V", region: "Primary" },
        { id: "E14-Oracle", role: "Consensus Cycle", region: "Byzantine" },
        { id: "tron-grid-01", role: "Production Node", region: "Grid-A" },
        { id: "tron-grid-02", role: "Production Node", region: "Grid-B" },
        { id: "witness-bom", role: "Witness Uplink", region: "AUS" },
        { id: "witness-himawari", role: "Witness Uplink", region: "JPN" },
        { id: "witness-goes", role: "Witness Uplink", region: "USA" },
        { id: "witness-meteosat", role: "Witness Uplink", region: "EUR" },
    ];

    return (
        <section
            className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 mt-28"
            data-testid="live-telemetry-section"
        >
            <div className="atl-divider mb-3">
                <span>[06] // Live Grid Telemetry · Real-Time</span>
            </div>
            <p className="atl-mono text-xs sm:text-sm text-white/60 mb-8 max-w-3xl">
                <span className="text-[color:var(--atl-secondary)]">In plain English → </span>
                Live view of the production grid. Ticks per second, node status, K-value convergence — everything updates every 2 seconds from the running system.
            </p>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                {/* Sparkline card */}
                <div className="lg:col-span-2 atl-card" data-testid="tick-rate-card">
                    <div className="flex items-center justify-between mb-4">
                        <div>
                            <div className="atl-label">Tenet Ticks / Sec · Live Feed</div>
                            <div className="atl-value mt-1" style={{ fontSize: "2rem" }} data-testid="tick-rate-value">
                                {history.length ? Math.round(history[history.length - 1]).toLocaleString() : "—"}
                            </div>
                        </div>
                        <span className="atl-dot" />
                    </div>
                    <svg
                        viewBox="0 0 400 90"
                        preserveAspectRatio="none"
                        style={{ width: "100%", height: 110, background: "rgba(0,0,0,0.35)", border: "1px solid rgba(0,255,65,0.15)" }}
                        data-testid="tick-rate-sparkline"
                    >
                        {history.map((v, i) => {
                            const x = (i / Math.max(1, history.length - 1)) * 400;
                            const y = 90 - (v / maxRate) * 82 - 4;
                            const nextV = history[i + 1];
                            if (nextV == null) return null;
                            const x2 = ((i + 1) / Math.max(1, history.length - 1)) * 400;
                            const y2 = 90 - (nextV / maxRate) * 82 - 4;
                            return (
                                <line
                                    key={i}
                                    x1={x}
                                    y1={y}
                                    x2={x2}
                                    y2={y2}
                                    stroke="#00FF41"
                                    strokeWidth="1.5"
                                    strokeOpacity="0.85"
                                />
                            );
                        })}
                        {history.map((v, i) => {
                            const x = (i / Math.max(1, history.length - 1)) * 400;
                            const y = 90 - (v / maxRate) * 82 - 4;
                            return <circle key={`d${i}`} cx={x} cy={y} r="1.2" fill="#00FF41" />;
                        })}
                    </svg>
                    <div className="mt-3 grid grid-cols-3 gap-3 atl-mono text-xs text-white/70">
                        <div>
                            <span className="text-white/40">tiles: </span>
                            <span className="text-[color:var(--atl-primary)]">
                                {state?.witnessed_tiles?.toLocaleString() ?? "—"}
                            </span>
                        </div>
                        <div>
                            <span className="text-white/40">K-value: </span>
                            <span className="text-[color:var(--atl-primary)]">{state?.k_value ?? "—"}</span>
                        </div>
                        <div className="text-right">
                            <span className="text-white/40">uptime: </span>
                            <span className="text-[color:var(--atl-secondary)]">{state?.uptime ?? "—"}</span>
                        </div>
                    </div>
                </div>

                {/* Node grid */}
                <div className="atl-card" data-testid="node-grid-card">
                    <div className="atl-label mb-4">Node Grid · tron-grid + XyoNode01</div>
                    <div className="grid grid-cols-2 gap-2">
                        {nodes.map((n) => (
                            <div
                                key={n.id}
                                data-testid={`node-${n.id}`}
                                className="atl-mono text-[0.62rem] p-2 border"
                                style={{
                                    background: "rgba(0,255,65,0.04)",
                                    borderColor: "rgba(0,255,65,0.25)",
                                }}
                            >
                                <div className="flex items-center gap-2">
                                    <span className="atl-dot" />
                                    <span className="text-white/85 truncate">{n.id}</span>
                                </div>
                                <div className="text-white/45 mt-1">{n.role}</div>
                                <div className="text-[color:var(--atl-primary)]">{n.region}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
