import { useEffect, useRef, useState } from "react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * Matrix-styled "Ask the Genesis Engine" chat widget.
 * Streams responses via SSE from /api/chat.
 */
export default function GenesisChat() {
    const [open, setOpen] = useState(false);
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([
        { role: "assistant", text: "⟨⟩ Genesis Engine online. Ask me anything about ATL — satellites, engines, Series A, hardware." },
    ]);
    const [busy, setBusy] = useState(false);
    const sessionRef = useRef(null);
    const scrollRef = useRef(null);

    const SUGGESTIONS = [
        "How is K=0.995 computed?",
        "Explain the espVmark hardware root of trust.",
        "Show me the assistive-tech use case.",
        "What is the Series A ask?",
    ];

    if (!sessionRef.current) {
        sessionRef.current =
            (typeof crypto !== "undefined" && crypto.randomUUID)
                ? crypto.randomUUID()
                : `s-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    }

    useEffect(() => {
        if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }, [messages, open]);

    const send = async (overrideText) => {
        const text = (overrideText ?? input).trim();
        if (!text || busy) return;
        setInput("");
        setMessages((m) => [...m, { role: "user", text }, { role: "assistant", text: "…" }]);
        setBusy(true);
        try {
            const res = await fetch(`${API}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionRef.current, message: text }),
            });
            const data = await res.json();
            const reply = (data && data.reply) || "⚠ empty response";
            setMessages((m) => {
                const copy = [...m];
                copy[copy.length - 1] = { role: "assistant", text: reply };
                return copy;
            });
        } catch (err) {
            if (process.env.NODE_ENV !== "production") console.error("[GenesisChat]", err);
            setMessages((m) => {
                const copy = [...m];
                copy[copy.length - 1] = { role: "assistant", text: "⚠ SIGNAL LOSS · engine unreachable" };
                return copy;
            });
        } finally {
            setBusy(false);
        }
    };

    return (
        <>
            {/* Floating toggle */}
            <button
                onClick={() => setOpen((v) => !v)}
                className="atl-btn"
                data-testid="genesis-chat-toggle"
                style={{
                    position: "fixed",
                    bottom: "1.25rem",
                    right: "1.25rem",
                    zIndex: 60,
                    boxShadow: "0 0 24px rgba(0,255,65,0.55)",
                }}
            >
                {open ? "▼ CLOSE" : "◉ ASK GENESIS ENGINE"}
            </button>

            {open && (
                <div
                    data-testid="genesis-chat-panel"
                    style={{
                        position: "fixed",
                        bottom: "5rem",
                        right: "1.25rem",
                        width: "min(420px, calc(100vw - 2.5rem))",
                        height: "min(560px, calc(100vh - 8rem))",
                        zIndex: 60,
                        background: "rgba(2,4,2,0.96)",
                        border: "1px solid rgba(0,255,65,0.55)",
                        boxShadow: "0 0 40px rgba(0,255,65,0.35), inset 0 0 40px rgba(0,255,65,0.05)",
                        display: "flex",
                        flexDirection: "column",
                    }}
                >
                    <div
                        className="atl-label"
                        style={{
                            padding: "0.8rem 1rem",
                            borderBottom: "1px solid rgba(0,255,65,0.25)",
                            display: "flex",
                            justifyContent: "space-between",
                        }}
                    >
                        <span>⟨⟩ Genesis Engine · Gemini 3 Flash</span>
                        <span className="atl-dot" />
                    </div>

                    <div
                        ref={scrollRef}
                        style={{ flex: 1, overflowY: "auto", padding: "1rem", fontSize: "0.85rem" }}
                        className="atl-mono"
                        data-testid="genesis-chat-messages"
                    >
                        {messages.map((m, i) => (
                            <div
                                key={i}
                                style={{
                                    marginBottom: "0.9rem",
                                    color: m.role === "user" ? "rgba(0,255,255,0.9)" : "rgba(0,255,65,0.9)",
                                }}
                            >
                                <div className="atl-label" style={{ fontSize: "0.58rem", marginBottom: "0.15rem" }}>
                                    {m.role === "user" ? "you@atl:~$" : "genesis@engine:~$"}
                                </div>
                                <div style={{ whiteSpace: "pre-wrap", lineHeight: 1.45 }}>
                                    {m.text || (busy && i === messages.length - 1 ? "▌" : "")}
                                </div>
                            </div>
                        ))}

                        {messages.length <= 1 && !busy && (
                            <div className="mt-4" data-testid="genesis-chat-suggestions">
                                <div className="atl-label" style={{ fontSize: "0.58rem", marginBottom: "0.5rem" }}>
                                    ▸ suggested queries
                                </div>
                                <div style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
                                    {SUGGESTIONS.map((s, idx) => (
                                        <button
                                            key={s}
                                            data-testid={`genesis-chat-suggestion-${idx}`}
                                            onClick={() => send(s)}
                                            className="atl-mono"
                                            style={{
                                                textAlign: "left",
                                                padding: "0.5rem 0.7rem",
                                                background: "rgba(0,255,65,0.05)",
                                                border: "1px solid rgba(0,255,65,0.25)",
                                                color: "rgba(0,255,65,0.85)",
                                                fontSize: "0.72rem",
                                                cursor: "pointer",
                                                transition: "all 0.2s",
                                            }}
                                            onMouseOver={(e) => {
                                                e.currentTarget.style.background = "rgba(0,255,65,0.15)";
                                                e.currentTarget.style.borderColor = "rgba(0,255,65,0.6)";
                                            }}
                                            onMouseOut={(e) => {
                                                e.currentTarget.style.background = "rgba(0,255,65,0.05)";
                                                e.currentTarget.style.borderColor = "rgba(0,255,65,0.25)";
                                            }}
                                        >
                                            → {s}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>

                    <form
                        onSubmit={(e) => { e.preventDefault(); send(); }}
                        style={{ borderTop: "1px solid rgba(0,255,65,0.25)", padding: "0.6rem", display: "flex", gap: "0.5rem" }}
                    >
                        <input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="> ask about ATL…"
                            disabled={busy}
                            data-testid="genesis-chat-input"
                            className="atl-mono"
                            style={{
                                flex: 1,
                                background: "rgba(0,255,65,0.05)",
                                border: "1px solid rgba(0,255,65,0.3)",
                                color: "var(--atl-primary)",
                                padding: "0.55rem 0.7rem",
                                fontSize: "0.85rem",
                                outline: "none",
                            }}
                        />
                        <button
                            type="submit"
                            disabled={busy || !input.trim()}
                            data-testid="genesis-chat-send"
                            className="atl-btn"
                            style={{ padding: "0.55rem 0.9rem", fontSize: "0.72rem", opacity: busy ? 0.5 : 1 }}
                        >
                            {busy ? "…" : "SEND"}
                        </button>
                    </form>
                </div>
            )}
        </>
    );
}
