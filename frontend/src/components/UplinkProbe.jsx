import { useEffect, useRef, useState } from "react";

// --- status → visual mapping helpers (extracted from nested ternaries)
const STATUS_COLOR = {
    LOCKED: "var(--atl-primary)",
    DEGRADED: "var(--atl-secondary)",
    PROBING: "rgba(255,255,255,0.7)",
    SIGNAL_LOSS: "var(--atl-glitch)",
};
const STATUS_LABEL = {
    LOCKED: "SIGNAL LOCKED",
    DEGRADED: "SIGNAL DEGRADED",
    PROBING: "PROBING UPLINK…",
    SIGNAL_LOSS: "SIGNAL LOSS · UPLINK OFFLINE",
};
const isAnimated = (s) => s === "LOCKED" || s === "PROBING";

/**
 * Client-side uplink probe. Polls the given URL from the visitor's browser.
 * Works when visitor is on the same machine broadcasting the port (demos, local dev).
 * Fails gracefully with "SIGNAL LOSS" indicator when unreachable.
 */
export default function UplinkProbe({ url = "http://localhost:5555", intervalMs = 3000 }) {
    const [state, setState] = useState({ status: "PROBING", latency: null, payload: null, lastSeen: null });
    const timerRef = useRef(null);

    useEffect(() => {
        let cancelled = false;

        const probe = async () => {
            const t0 = performance.now();
            const ctrl = new AbortController();
            const timeout = setTimeout(() => ctrl.abort(), 2000);
            try {
                const res = await fetch(url, { signal: ctrl.signal, cache: "no-store" });
                clearTimeout(timeout);
                const latency = Math.round(performance.now() - t0);
                let payload = null;
                try {
                    const text = await res.text();
                    try { payload = JSON.parse(text); }
                    catch { payload = text.slice(0, 120); }
                } catch { /* ignore parse errors */ }
                if (!cancelled) {
                    setState({
                        status: res.ok ? "LOCKED" : "DEGRADED",
                        latency,
                        payload,
                        lastSeen: new Date(),
                    });
                }
            } catch {
                clearTimeout(timeout);
                if (!cancelled) {
                    setState((s) => ({ ...s, status: "SIGNAL_LOSS", latency: null }));
                }
            }
        };

        probe();
        timerRef.current = setInterval(probe, intervalMs);
        return () => {
            cancelled = true;
            clearInterval(timerRef.current);
        };
    }, [url, intervalMs]);

    const color = STATUS_COLOR[state.status] || STATUS_COLOR.SIGNAL_LOSS;
    const dotAnim = isAnimated(state.status) ? "atl-pulse 1.4s ease-in-out infinite" : "none";
    const label = STATUS_LABEL[state.status] || STATUS_LABEL.SIGNAL_LOSS;

    const displayUrl = url.replace(/^https?:\/\//, "");

    return (
        <div
            className="atl-card"
            style={{ padding: "1rem 1.15rem" }}
            data-testid="uplink-probe"
        >
            <div className="flex items-center justify-between mb-2 gap-3">
                <div className="atl-label" style={{ fontSize: "0.6rem" }}>
                    espVmark Uplink · {displayUrl}
                </div>
                <span
                    className="inline-block w-2 h-2 rounded-full shrink-0"
                    style={{
                        background: color,
                        boxShadow: `0 0 8px ${color}`,
                        animation: dotAnim,
                    }}
                />
            </div>

            <div
                className="atl-mono uppercase tracking-widest text-sm"
                style={{ color, textShadow: `0 0 8px ${color}55` }}
                data-testid="uplink-status"
            >
                {label}
            </div>

            <div className="mt-2 grid grid-cols-2 gap-2 atl-mono text-[0.65rem] text-white/70">
                <div>
                    <span className="text-white/40">latency: </span>
                    <span style={{ color }}>
                        {state.latency == null ? "—" : `${state.latency}ms`}
                    </span>
                </div>
                <div className="text-right">
                    <span className="text-white/40">last: </span>
                    <span style={{ color }}>
                        {state.lastSeen ? state.lastSeen.toLocaleTimeString([], { hour12: false }) : "—"}
                    </span>
                </div>
            </div>

            {state.status === "SIGNAL_LOSS" && (
                <div className="mt-2 atl-mono text-[0.6rem] text-white/40 leading-snug">
                    &gt; visitor not on same host · CORS or firewall · start espVmark on {displayUrl}
                </div>
            )}
            {state.status === "LOCKED" && state.payload && (
                <div
                    className="mt-2 atl-mono text-[0.6rem] text-[color:var(--atl-primary)] leading-snug break-all overflow-hidden"
                    style={{ maxHeight: "3.6em" }}
                >
                    &gt; {typeof state.payload === "string" ? state.payload : JSON.stringify(state.payload).slice(0, 120)}
                </div>
            )}
        </div>
    );
}
