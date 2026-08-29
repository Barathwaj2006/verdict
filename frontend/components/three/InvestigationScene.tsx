"use client";
import { useRef, useMemo, useEffect, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Float, Line, Html } from '@react-three/drei';
import * as THREE from 'three';
import { InvestigationViewState } from '../../hooks/useInvestigationState';

function useReducedMotion() {
  const [reducedMotion, setReducedMotion] = useState(false);
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReducedMotion(mediaQuery.matches);
    const handler = () => setReducedMotion(mediaQuery.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);
  return reducedMotion;
}

export function AgentNode3D({ position, color, label, isActive, scale = 1, reducedMotion = false }: { position: [number, number, number], color: string, label: string, isActive: boolean, scale?: number, reducedMotion?: boolean }) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current && isActive && !reducedMotion) {
      meshRef.current.rotation.y += 0.02;
      meshRef.current.rotation.x += 0.01;
      const pulse = 1 + Math.sin(state.clock.elapsedTime * 4) * 0.1;
      meshRef.current.scale.setScalar(scale * pulse);
    } else if (meshRef.current) {
      meshRef.current.rotation.y = 0;
      meshRef.current.rotation.x = 0;
      meshRef.current.scale.setScalar(scale);
    }
  });

  return (
    <group position={position}>
      <Float speed={reducedMotion ? 0 : 2} rotationIntensity={reducedMotion ? 0 : 0.2} floatIntensity={reducedMotion ? 0 : 0.5}>
        <mesh ref={meshRef}>
          <octahedronGeometry args={[1, 0]} />
          <meshStandardMaterial color={color} wireframe={!isActive} emissive={isActive ? color : '#000000'} emissiveIntensity={isActive ? 0.5 : 0} />
        </mesh>
      </Float>
      <Html position={[0, -1.5, 0]} center className="pointer-events-none">
        <div className={`px-2 py-1 rounded bg-black/80 backdrop-blur border text-xs font-mono text-center whitespace-nowrap transition-colors ${isActive ? 'border-white text-white' : 'border-neutral-800 text-neutral-400'}`}>
          {label}
        </div>
      </Html>
    </group>
  );
}

export function Connection3D({ start, end, isActive, color = "#444444" }: { start: [number, number, number], end: [number, number, number], isActive: boolean, color?: string }) {
  const points = useMemo(() => [new THREE.Vector3(...start), new THREE.Vector3(...end)], [start, end]);
  return (
    <Line
      points={points}
      color={isActive ? color : "#222222"}
      lineWidth={isActive ? 2 : 1}
      dashed={!isActive}
      dashSize={0.2}
      dashScale={1}
      gapSize={0.1}
      transparent
      opacity={0.5}
    />
  );
}

export default function InvestigationScene({ state }: { state: InvestigationViewState }) {
  const groupRef = useRef<THREE.Group>(null);
  const reducedMotion = useReducedMotion();

  useFrame(({ clock }) => {
    if (groupRef.current && !reducedMotion) {
      groupRef.current.rotation.y = Math.sin(clock.elapsedTime * 0.1) * 0.1;
    }
  });

  const leadPos: [number, number, number] = [0, 4, 0];
  const skepticPos: [number, number, number] = [-3, -2, 0];
  const verifierPos: [number, number, number] = [3, -2, 0];

  const researcherCount = Math.max(state.missions.length, 1);
  const spread = Math.min(researcherCount * 2.5, 10);
  
  return (
    <group ref={groupRef}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      
      {/* LEAD */}
      <AgentNode3D 
        position={leadPos} 
        color="#3b82f6" 
        label="LEAD AGENT" 
        isActive={!state.isComplete && state.activeAgents.size === 0} 
        scale={1.2}
        reducedMotion={reducedMotion}
      />

      {/* RESEARCHERS */}
      {state.missions.length === 0 ? (
        <AgentNode3D position={[0, 1, 0]} color="#525252" label="Awaiting Missions..." isActive={false} reducedMotion={reducedMotion} />
      ) : (
        state.missions.map((m, i) => {
          const x = -spread/2 + (spread / Math.max(researcherCount - 1, 1)) * i;
          const pos: [number, number, number] = [x, 1, (Math.abs(x) * 0.2)];
          return (
            <group key={i}>
              <Connection3D start={leadPos} end={pos} isActive={m.status === 'running' || m.status === 'completed'} color="#22c55e" />
              <AgentNode3D 
                position={pos} 
                color={m.status === 'completed' ? "#15803d" : "#22c55e"} 
                label={m.role.substring(0, 15) + (m.role.length > 15 ? '...' : '')} 
                isActive={m.status === 'running'} 
                scale={0.8}
                reducedMotion={reducedMotion}
              />
              <Connection3D start={pos} end={skepticPos} isActive={state.challenges.length > 0} color="#f97316" />
            </group>
          );
        })
      )}

      {/* SKEPTIC */}
      {state.challenges.length > 0 && (
        <>
          <AgentNode3D position={skepticPos} color="#f97316" label={`SKEPTIC (${state.challenges.length})`} isActive={state.activeAgents.has('Skeptic')} reducedMotion={reducedMotion} />
          <Connection3D start={skepticPos} end={verifierPos} isActive={state.activeAgents.has('Verifier') || state.verifications.length > 0} color="#a855f7" />
        </>
      )}

      {/* VERIFIER */}
      {(state.activeAgents.has('Verifier') || state.verifications.length > 0) && (
        <>
          <AgentNode3D position={verifierPos} color="#a855f7" label={`VERIFIER (${state.verifications.length})`} isActive={state.activeAgents.has('Verifier')} reducedMotion={reducedMotion} />
          <Connection3D start={verifierPos} end={leadPos} isActive={state.activeAgents.size === 0 && state.round > 1} color="#3b82f6" />
        </>
      )}
      
      {/* PARTICLES for ambiance */}
      {!reducedMotion && (
        <points>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" count={100} array={new Float32Array(300).map(() => (Math.random() - 0.5) * 20)} itemSize={3} />
          </bufferGeometry>
          <pointsMaterial size={0.05} color="#444444" transparent opacity={0.5} />
        </points>
      )}
    </group>
  );
}
