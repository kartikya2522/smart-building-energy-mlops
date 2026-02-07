'use client';

import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function Earth() {
    const meshRef = useRef<THREE.Mesh>(null);

    // Slow, continuous rotation
    useFrame((state, delta) => {
        if (meshRef.current) {
            meshRef.current.rotation.y += delta * 0.15;
        }
    });

    return (
        <mesh ref={meshRef}>
            <sphereGeometry args={[2.5, 64, 64]} />
            {/* 
        Using a physical material for a premium look.
        Dark color with high metalness creates a sleek "tech" feel.
        Green rim/sheen comes from the lighting.
      */}
            <meshPhysicalMaterial
                color="#080808"
                roughness={0.6}
                metalness={0.4}
                clearcoat={0.2}
                clearcoatRoughness={0.4}
            />
            {/* Wireframe overlay for 'tech' feel without heavy textures */}
            <mesh scale={[1.001, 1.001, 1.001]}>
                <sphereGeometry args={[2.5, 32, 32]} />
                <meshBasicMaterial color="#1a2e1d" wireframe transparent opacity={0.1} />
            </mesh>
        </mesh>
    );
}

function EnergyParticles({ count = 200 }) {
    const pointsRef = useRef<THREE.Points>(null);

    // Generate particles in a spherical shell around the earth
    const [positions, sizes] = useMemo(() => {
        const pos = new Float32Array(count * 3);
        const sz = new Float32Array(count);
        const radius = 3.5;

        for (let i = 0; i < count; i++) {
            // Random point on sphere surface * random radius variation
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            const r = radius + (Math.random() - 0.5) * 1.5;

            const x = r * Math.sin(phi) * Math.cos(theta);
            const y = r * Math.sin(phi) * Math.sin(theta);
            const z = r * Math.cos(phi);

            pos[i * 3] = x;
            pos[i * 3 + 1] = y;
            pos[i * 3 + 2] = z;

            sz[i] = Math.random();
        }
        return [pos, sz];
    }, [count]);

    useFrame((state, delta) => {
        if (pointsRef.current) {
            // Rotate particles slightly faster/differently than earth for depth
            pointsRef.current.rotation.y += delta * 0.05;
            pointsRef.current.rotation.z += delta * 0.01;
        }
    });

    return (
        <points ref={pointsRef}>
            <bufferGeometry>
                <bufferAttribute
                    attach="attributes-position"
                    count={positions.length / 3}
                    array={positions}
                    itemSize={3}
                    args={[positions, 3]}
                />
                <bufferAttribute
                    attach="attributes-size"
                    count={sizes.length}
                    array={sizes}
                    itemSize={1}
                    args={[sizes, 1]}
                />
            </bufferGeometry>
            {/* Custom shader-like look with standard material settings or basic material */}
            <pointsMaterial
                size={0.04}
                color="#4ade80" // Design token: green-400
                transparent
                opacity={0.6}
                sizeAttenuation
                blending={THREE.AdditiveBlending}
            />
        </points>
    );
}

export default function EarthScene() {
    return (
        <div className="absolute inset-0 z-0 opacity-80">
            <Canvas
                camera={{ position: [0, 0, 8], fov: 45 }}
                dpr={[1, 2]} // Handle high-DPI screens, but cap at 2 for performance
                gl={{ antialias: true, alpha: true }}
            >
                {/* 
                  Lighting Strategy:
                  - Ambient: Base visibility
                  - Directional (Green): Main "Energy" light source
                  - Point (Blue): Secondary fill for depth
                 */}
                <ambientLight intensity={0.2} />
                <directionalLight position={[10, 5, 5]} intensity={2} color="#4ade80" />
                <pointLight position={[-10, -5, -5]} intensity={1} color="#3b82f6" />

                <Earth />
                <EnergyParticles count={300} />
            </Canvas>
        </div>
    );
}
