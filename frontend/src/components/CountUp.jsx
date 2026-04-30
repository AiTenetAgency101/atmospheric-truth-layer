import { useEffect, useRef, useState } from "react";

/**
 * Live-ticking counter that:
 *  1. animates from a low seed to the provided target on mount
 *  2. then increments every tick by `ratePerSec` to simulate a running engine
 */
export default function CountUp({ target, ratePerSec = 1, duration = 1400, testId }) {
    const [value, setValue] = useState(Math.max(0, target - Math.floor(target * 0.002)));
    const startRef = useRef(null);
    const baseRef = useRef(value);

    // phase 1: animate to target
    useEffect(() => {
        const from = baseRef.current;
        const to = target;
        startRef.current = performance.now();
        let raf;
        const step = (now) => {
            const p = Math.min(1, (now - startRef.current) / duration);
            const eased = 1 - Math.pow(1 - p, 3);
            setValue(Math.floor(from + (to - from) * eased));
            if (p < 1) raf = requestAnimationFrame(step);
        };
        raf = requestAnimationFrame(step);
        return () => cancelAnimationFrame(raf);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [target]);

    // phase 2: continuous live tick
    useEffect(() => {
        const interval = setInterval(() => {
            setValue((v) => v + Math.max(1, Math.round(ratePerSec * (0.6 + Math.random() * 0.8))));
        }, 1000);
        return () => clearInterval(interval);
    }, [ratePerSec]);

    return (
        <span data-testid={testId} className="atl-value">
            {value.toLocaleString("en-US")}
        </span>
    );
}
