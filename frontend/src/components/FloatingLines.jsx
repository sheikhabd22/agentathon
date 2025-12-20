import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { CatmullRomLine } from '@react-three/drei';
import * as THREE from 'three';

const WaveLine = ({
    index,
    total,
    distance,
    yOffset,
    speed,
    bendStrength,
    color
}) => {
    const lineRef = useRef();

    // Create points for the curve
    const points = useMemo(() => {
        const pts = [];
        const width = 20; // Width of the wave
        const segments = 20;

        for (let i = 0; i <= segments; i++) {
            const x = (i / segments) * width - (width / 2);
            // Determine Z based on index to space them out in depth
            const z = (index - total / 2) * distance;
            pts.push(new THREE.Vector3(x, 0, z));
        }
        return pts;
    }, [index, total, distance]);

    // Curve setup
    const curve = useMemo(() => new THREE.CatmullRomCurve3(points), [points]);

    useFrame(({ clock }) => {
        if (!lineRef.current) return;

        const t = clock.getElapsedTime() * speed;
        const geometry = lineRef.current.geometry;

        // Animate the 'y' position of points to simulate a wave
        // We update the geometry points directly if possible or transform the mesh
        // For CatmullRomLine, it might be expensive to recalc curve every frame.
        // Instead, let's just use a simple sine wave on a Line or just animate the container.
        // But to get a true "bend" effect, we might need vertex manipulation.

        // Simpler approach for "Floating Lines":
        // Just rotate slightly or move up/down.

        // Let's rely on the curve doing a static wave for now but animated position?
        // Actually, "FloatingLines" usually implies keyframe animation of the points.

        // For performance and simplicity in this mockup:
        // We will just oscillate the whole line group or individual lines.
    });

    return (
        <group position={[0, yOffset, 0]}>
            <CatmullRomLine
                ref={lineRef}
                points={points}
                curveType="catmullrom"
                tension={0.5}
                color={color}
                lineWidth={1}
                dashed={false}
                opacity={0.3}
                transparent
            />
        </group>
    );
};


const AnimatedWave = ({
    count,
    distance,
    yPos,
    bendStrength,
    color,
    speedFactor
}) => {
    const groupRef = useRef();

    useFrame(({ clock, mouse }) => {
        const t = clock.getElapsedTime();
        if (groupRef.current) {
            // Gentle undulation
            groupRef.current.position.y = yPos + Math.sin(t * speedFactor) * 0.5;

            // Interaction
            const targetRotX = mouse.y * 0.1;
            const targetRotY = mouse.x * 0.1;

            groupRef.current.rotation.x += (targetRotX - groupRef.current.rotation.x) * 0.05;
            groupRef.current.rotation.y += (targetRotY - groupRef.current.rotation.y) * 0.05;
        }
    });

    return (
        <group ref={groupRef}>
            {Array.from({ length: count }).map((_, i) => (
                <WaveLine
                    key={i}
                    index={i}
                    total={count}
                    distance={distance}
                    yOffset={0}
                    speed={speedFactor}
                    bendStrength={bendStrength}
                    color={color}
                />
            ))}
        </group>
    );
};

const FloatingLines = ({
    enabledWaves = ['top', 'middle', 'bottom'],
    lineCount = [10, 15, 20],
    lineDistance = [0.5, 0.3, 0.2],
    bendRadius = 5.0,
    bendStrength = -0.5,
    interactive = true,
    parallax = true
}) => {
    // Normalize props if they are single values
    const counts = Array.isArray(lineCount) ? lineCount : [lineCount, lineCount, lineCount];
    const distances = Array.isArray(lineDistance) ? lineDistance : [lineDistance, lineDistance, lineDistance];

    return (
        <Canvas camera={{ position: [0, 0, 15], fov: 45 }} style={{ background: 'transparent' }}>
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} />

            {enabledWaves.includes('top') && (
                <AnimatedWave
                    count={counts[0]}
                    distance={distances[0]}
                    yPos={4}
                    bendStrength={bendStrength}
                    color="#e8f0fe" // Light Blue
                    speedFactor={0.4}
                />
            )}

            {enabledWaves.includes('middle') && (
                <AnimatedWave
                    count={counts[1]}
                    distance={distances[1]}
                    yPos={0}
                    bendStrength={bendStrength}
                    color="#1a73e8" // Primary Blue
                    speedFactor={0.6}
                />
            )}

            {enabledWaves.includes('bottom') && (
                <AnimatedWave
                    count={counts[2]}
                    distance={distances[2]}
                    yPos={-4}
                    bendStrength={bendStrength}
                    color="#1967d2" // Darker Blue
                    speedFactor={0.5}
                />
            )}
        </Canvas>
    );
};

export default FloatingLines;
