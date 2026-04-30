import { useEffect, useState } from "react";

const HEX = "0123456789abcdef";
const rand = (len) =>
    Array.from({ length: len }, () => HEX[Math.floor(Math.random() * HEX.length)]).join("");

/**
 * Anchor hash stays fixed (cryptographic anchor). Tail continuously re-scrambles
 * to simulate live observation chunks being stream-signed.
 */
export default function LiveHash({ anchor, testId }) {
    const [tail, setTail] = useState(rand(16));
    useEffect(() => {
        const id = setInterval(() => setTail(rand(16)), 400);
        return () => clearInterval(id);
    }, []);
    return (
        <span className="atl-hash" data-testid={testId}>
            <span style={{ color: "rgba(0,255,65,0.85)" }}>{anchor}</span>
            <span style={{ opacity: 0.55 }}>::</span>
            <span>{tail}</span>
        </span>
    );
}
