import { useEffect, useRef } from "react";

/**
 * Classic Matrix digital rain — pure canvas, no deps.
 * Runs behind everything at low opacity (controlled via CSS class `atl-rain`).
 */
export default function MatrixRain() {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        let animationId;

        const glyphs = "ｦｱｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉ0123456789ATLATMOSPHERICTRUTH$%#@?!".split("");
        const fontSize = 16;
        let columns = 0;
        let drops = [];

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            columns = Math.floor(canvas.width / fontSize);
            drops = new Array(columns).fill(0).map(() => Math.random() * -100);
        };
        resize();
        window.addEventListener("resize", resize);

        const draw = () => {
            ctx.fillStyle = "rgba(2, 4, 2, 0.08)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.font = `${fontSize}px "Share Tech Mono", monospace`;

            for (let i = 0; i < drops.length; i++) {
                const text = glyphs[Math.floor(Math.random() * glyphs.length)];
                const x = i * fontSize;
                const y = drops[i] * fontSize;

                // brightest at the head, dimmer trail is handled by the fade above
                ctx.fillStyle = Math.random() > 0.975 ? "#CFFFD4" : "#00FF41";
                ctx.fillText(text, x, y);

                if (y > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
            animationId = requestAnimationFrame(draw);
        };
        draw();

        return () => {
            cancelAnimationFrame(animationId);
            window.removeEventListener("resize", resize);
        };
    }, []);

    return <canvas ref={canvasRef} className="atl-rain" data-testid="matrix-rain-canvas" />;
}
