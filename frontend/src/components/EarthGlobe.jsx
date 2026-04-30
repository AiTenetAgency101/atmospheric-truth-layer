import { useEffect, useRef } from "react";
import * as THREE from "three";

/**
 * Vanilla Three.js globe — avoids R3F + babel plugin conflicts that inject
 * attributes like x-line-number into Three objects.
 */
export default function EarthGlobe() {
    const mountRef = useRef(null);

    useEffect(() => {
        const mount = mountRef.current;
        if (!mount) return;

        const width = mount.clientWidth;
        const height = mount.clientHeight;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 100);
        camera.position.set(0, 1.3, 4.8);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setClearColor(0x000000, 0);
        mount.appendChild(renderer.domElement);

        // Starfield
        const starGeo = new THREE.BufferGeometry();
        const starCount = 1500;
        const positions = new Float32Array(starCount * 3);
        for (let i = 0; i < starCount; i++) {
            const r = 25 + Math.random() * 25;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
            positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
            positions[i * 3 + 2] = r * Math.cos(phi);
        }
        starGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
        const starMat = new THREE.PointsMaterial({
            color: 0xaaffbb,
            size: 0.04,
            transparent: true,
            opacity: 0.75,
        });
        scene.add(new THREE.Points(starGeo, starMat));

        // Inner filled sphere (backdrop)
        scene.add(
            new THREE.Mesh(
                new THREE.SphereGeometry(1.6, 48, 48),
                new THREE.MeshBasicMaterial({ color: 0x010701 })
            )
        );

        // Wireframe Earth (primary)
        const earth = new THREE.Mesh(
            new THREE.SphereGeometry(1.62, 48, 32),
            new THREE.MeshBasicMaterial({
                color: 0x00ff41,
                wireframe: true,
                transparent: true,
                opacity: 0.85,
            })
        );
        scene.add(earth);

        // Outer atmosphere (cyan wireframe)
        const atmos = new THREE.Mesh(
            new THREE.SphereGeometry(1.85, 24, 16),
            new THREE.MeshBasicMaterial({
                color: 0x00ffff,
                wireframe: true,
                transparent: true,
                opacity: 0.2,
            })
        );
        scene.add(atmos);

        // Equator-style highlight rings around the globe
        const equatorMat = new THREE.MeshBasicMaterial({
            color: 0x00ff41,
            transparent: true,
            opacity: 0.5,
            side: THREE.DoubleSide,
        });
        [0, Math.PI / 3, -Math.PI / 3].forEach((tilt) => {
            const ring = new THREE.Mesh(new THREE.TorusGeometry(1.63, 0.005, 8, 96), equatorMat);
            ring.rotation.x = Math.PI / 2;
            ring.rotation.z = tilt;
            scene.add(ring);
        });

        // Orbit rings
        const orbitConfigs = [
            { radius: 2.4, tilt: 0.0, color: 0x00ff41 },
            { radius: 2.7, tilt: 0.35, color: 0x00ffff },
            { radius: 3.0, tilt: -0.4, color: 0x00ff41 },
            { radius: 3.3, tilt: 0.7, color: 0x00ffff },
        ];
        orbitConfigs.forEach(({ radius, tilt, color }) => {
            const mesh = new THREE.Mesh(
                new THREE.TorusGeometry(radius, 0.006, 6, 128),
                new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.45 })
            );
            mesh.rotation.x = Math.PI / 2 + tilt;
            scene.add(mesh);
        });

        // Satellites
        const satellites = [
            { radius: 2.4, speed: 0.75, tilt: 0.0, color: 0x00ff41, offset: 0 },
            { radius: 2.7, speed: -0.55, tilt: 0.35, color: 0x00ffff, offset: 1.2 },
            { radius: 3.0, speed: 0.45, tilt: -0.4, color: 0x00ff41, offset: 2.8 },
            { radius: 3.3, speed: -0.35, tilt: 0.7, color: 0x00ffff, offset: 4.1 },
        ].map((cfg) => {
            const group = new THREE.Group();
            group.rotation.x = cfg.tilt;
            const core = new THREE.Mesh(
                new THREE.BoxGeometry(0.14, 0.14, 0.14),
                new THREE.MeshBasicMaterial({ color: cfg.color })
            );
            const glow = new THREE.Mesh(
                new THREE.SphereGeometry(0.25, 14, 14),
                new THREE.MeshBasicMaterial({ color: cfg.color, transparent: true, opacity: 0.2 })
            );
            group.add(core);
            group.add(glow);
            scene.add(group);
            return { group, ...cfg };
        });

        // Resize handler
        const onResize = () => {
            const w = mount.clientWidth;
            const h = mount.clientHeight;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        };
        window.addEventListener("resize", onResize);

        let frameId;
        const clock = new THREE.Clock();
        const animate = () => {
            const dt = clock.getDelta();
            const t = clock.getElapsedTime();

            earth.rotation.y += dt * 0.18;
            atmos.rotation.y -= dt * 0.08;
            atmos.rotation.x += dt * 0.03;

            satellites.forEach((s) => {
                const angle = t * s.speed + s.offset;
                s.group.position.set(
                    Math.cos(angle) * s.radius,
                    Math.sin(angle * 0.6) * 0.25,
                    Math.sin(angle) * s.radius
                );
                // apply tilt by rotating position vector around X axis
                const y = s.group.position.y;
                const z = s.group.position.z;
                s.group.position.y = y * Math.cos(s.tilt) - z * Math.sin(s.tilt);
                s.group.position.z = y * Math.sin(s.tilt) + z * Math.cos(s.tilt);
            });

            renderer.render(scene, camera);
            frameId = requestAnimationFrame(animate);
        };
        animate();

        return () => {
            cancelAnimationFrame(frameId);
            window.removeEventListener("resize", onResize);
            renderer.dispose();
            if (renderer.domElement && renderer.domElement.parentNode === mount) {
                mount.removeChild(renderer.domElement);
            }
            scene.traverse((obj) => {
                if (obj.geometry) obj.geometry.dispose();
                if (obj.material) {
                    if (Array.isArray(obj.material)) obj.material.forEach((m) => m.dispose());
                    else obj.material.dispose();
                }
            });
        };
    }, []);

    return (
        <div
            ref={mountRef}
            style={{ width: "100%", height: "100%" }}
            data-testid="earth-globe-3d"
        />
    );
}
