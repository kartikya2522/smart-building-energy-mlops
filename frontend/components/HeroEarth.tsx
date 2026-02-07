'use client';

import React, { useRef, useMemo, Suspense } from 'react';
import { Canvas, useFrame, useLoader } from '@react-three/fiber';
import * as THREE from 'three';

// --- SUB-COMPONENTS --- //

function EarthMesh() {
    const earthRef = useRef<THREE.Mesh>(null);
    const cloudsRef = useRef<THREE.Mesh>(null);

    // Load textures
    const [colorMap, specularMap, normalMap, cloudsMap] = useLoader(THREE.TextureLoader, [
        '/textures/earth_daymap.jpg',
        '/textures/earth_specular.jpg',
        '/textures/earth_normal.jpg',
        '/textures/earth_clouds.png',
    ]);

    useFrame((_, delta) => {
        // Rotate Earth
        if (earthRef.current) {
            earthRef.current.rotation.y += delta * 0.05;
        }
        // Rotate Clouds slightly faster for parallax effect
        if (cloudsRef.current) {
            cloudsRef.current.rotation.y += delta * 0.07;
        }
    });

    return (
        <group>
            {/* EARTH SURFACE */}
            <mesh ref={earthRef} rotation={[0, 0, 0.4]}> {/* Tilt axis */}
                <sphereGeometry args={[2.5, 64, 64]} />
                <meshPhongMaterial
                    map={colorMap}
                    specularMap={specularMap}
                    normalMap={normalMap}
                    normalScale={new THREE.Vector2(0.8, 0.8)}
                    specular={new THREE.Color(0x333333)}
                    shininess={15}
                />
            </mesh>

            {/* CLOUD LAYER */}
            <mesh ref={cloudsRef} rotation={[0, 0, 0.4]} scale={[1.015, 1.015, 1.015]}>
                <sphereGeometry args={[2.5, 64, 64]} />
                <meshLambertMaterial
                    map={cloudsMap}
                    transparent={true}
                    opacity={0.8}
                    blending={THREE.AdditiveBlending}
                    depthWrite={false} // Prevents z-fighting with transparency
                />
            </mesh>

            {/* ATMOSPHERE GLOW (Simple Fresnel-ish Effect) */}
            <mesh scale={[1.15, 1.15, 1.15]} position={[0, 0, -1]}>
                <sphereGeometry args={[2.5, 32, 32]} />
                <meshBasicMaterial
                    color="#4ade80" // Green-ish atmospheric taint for coherence with site theme
                    transparent
                    opacity={0.05}
                    side={THREE.BackSide}
                    blending={THREE.AdditiveBlending}
                />
            </mesh>
        </group>
    );
}

// Reusable Star Layer Component
function StarLayer({ count, radiusRange, size, opacity, parallaxFactor, color = "#ffffff" }: { count: number, radiusRange: [number, number], size: number, opacity: number, parallaxFactor: number, color?: string }) {
    const points = useRef<THREE.Points>(null);

    const positions = useMemo(() => {
        const pos = new Float32Array(count * 3);
        for (let i = 0; i < count; i++) {
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            const r = radiusRange[0] + Math.random() * (radiusRange[1] - radiusRange[0]);

            const x = r * Math.sin(phi) * Math.cos(theta);
            const y = r * Math.sin(phi) * Math.sin(theta);
            const z = r * Math.cos(phi);

            pos[i * 3] = x;
            pos[i * 3 + 1] = y;
            pos[i * 3 + 2] = z;
        }
        return pos;
    }, [count, radiusRange]);

    useFrame((state) => {
        if (points.current) {
            const targetX = state.mouse.x * parallaxFactor;
            const targetY = state.mouse.y * parallaxFactor;
            points.current.rotation.x += (targetY - points.current.rotation.x) * 0.05;
            points.current.rotation.y += (targetX - points.current.rotation.y) * 0.05;
        }
    });

    return (
        <points ref={points}>
            <bufferGeometry>
                <bufferAttribute
                    attach="attributes-position"
                    count={positions.length / 3}
                    array={positions}
                    itemSize={3}
                    args={[positions, 3]}
                />
            </bufferGeometry>
            <pointsMaterial
                size={size}
                color={color}
                transparent
                opacity={opacity}
                sizeAttenuation
                depthWrite={false}
            />
        </points>
    );
}

function EnergySatellites({ count = 30 }) {
    const groupRef = useRef<THREE.Group>(null);

    useFrame((state, delta) => {
        if (groupRef.current) {
            // Slow independent orbit for satellites
            groupRef.current.rotation.y -= delta * 0.02;
            groupRef.current.rotation.z += delta * 0.005;
        }
    });

    // Generate satellites further out
    return (
        <group ref={groupRef}>
            <StarLayer
                count={count}
                radiusRange={[5, 8]}
                size={0.08}
                opacity={0.8}
                parallaxFactor={0.02}
                color="#60a5fa" // Blue-ish satellites
            />
        </group>
    );
}

function EnergyArcs() {
    return (
        <group rotation={[0.4, 0, 0.2]}> {/* Tilted orbit plane */}
            {/* Arc 1 */}
            <mesh rotation={[Math.PI / 2, 0, 0]}>
                <torusGeometry args={[5, 0.01, 16, 100]} />
                <meshBasicMaterial color="#ffffff" transparent opacity={0.05} />
            </mesh>
            {/* Arc 2 */}
            <mesh rotation={[Math.PI / 1.8, 0, 0.5]}>
                <torusGeometry args={[6.5, 0.015, 16, 100]} />
                <meshBasicMaterial color="#4ade80" transparent opacity={0.03} />
            </mesh>
        </group>
    );
}

function LoadingFallback() {
    return (
        <mesh>
            <sphereGeometry args={[2.5, 16, 16]} />
            <meshBasicMaterial color="#111" wireframe />
        </mesh>
    );
}

// --- MAIN COMPONENT --- //

export default function HeroEarth() {
    return (
        <div className="absolute inset-0 z-0 bg-black">
            <Canvas
                camera={{ position: [0, 0, 7], fov: 40 }}
                dpr={[1, 2]}
                gl={{ antialias: true, toneMapping: THREE.ACESFilmicToneMapping, outputColorSpace: THREE.SRGBColorSpace }}
            >
                <color attach="background" args={['#020202']} />

                {/* Lighting */}
                <ambientLight intensity={0.1} color="#4ade80" />
                <directionalLight position={[10, 5, 5]} intensity={3.5} color="#ffffff" />

                {/* Layered Starfield */}
                {/* 1. Deep Background - Small, faint, very slow */}
                <StarLayer count={4000} radiusRange={[20, 60]} size={0.02} opacity={0.4} parallaxFactor={0.02} />

                {/* 2. Foreground - Larger, fewer, more responsive for depth */}
                <StarLayer count={200} radiusRange={[10, 30]} size={0.04} opacity={0.6} parallaxFactor={0.08} />

                {/* 3. Energy System Elements */}
                <EnergySatellites />
                <EnergyArcs />

                <Suspense fallback={<LoadingFallback />}>
                    <EarthMesh />
                </Suspense>
            </Canvas>
        </div>
    );
}
